import json
# from tqdm import tqdm
import re
import torch
import sys
import os
import bgesimien as bgesim
# import sbertsimien as sbertsim
import posfilter as posfilter
import bertInsert as bertInsert
import numpy as np
import logging
import io
import time
import mysplit
import argparse
from typing import Any, List, Optional
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED

simimodel = bgesim


# get the origin term without []
def getOriginSentenceLst(sentencelst):
    originSentence = []
    for word in sentencelst:
        if word.startswith("[|term:") and word.endswith("|]") and len(word) > 2:
            originSentence.append(word[7:-2])
        else:
            originSentence.append(word)
    return originSentence

# get origin sentence without mark
def getOriginSentence(marked_Sentence):
    originSentence = re.sub(r'\[\|term:(.*?)\|\]', r'\1', marked_Sentence)
    return originSentence

# split sentence into words
def splitSentence(sentence):
    return mysplit.splitSentence(sentence)

def get_max_index(arr):
    arr = np.array(arr) 
    max_index = np.argmax(arr)  
    return int(max_index)

def chooseMostSimilarMeaningMuntantBge(originsentence, mutantsentences):
    similaritylst = simimodel.getSimilarity([originsentence], mutantsentences)    

    indexofmeaning = get_max_index(similaritylst)
    return [mutantsentences[indexofmeaning], indexofmeaning, similaritylst]

# meaning added to sentence
def addedmeaning(meaning):
    # delete the ., at the end of meaning
    meaning = meaning.strip()
    # meaning = meaning[:-1] if meaning.endswith(".") else meaning
    # meaning = meaning[:-1] if meaning.endswith(",") else meaning
    return "("+meaning+")"

def lst2str(lst):
    return " ".join(lst)

def judge_term_in_brackets(sentence, term_char_bg, term_char_ed):
    branket_sign = 0
    in_branket = False
    for i in range(len(sentence)):
        if sentence[i] == "(":
            branket_sign += 1
        elif sentence[i] == ")":
            branket_sign -= 1
        elif sentence[i] == "（":
            branket_sign += 1
        elif sentence[i] == "）":
            branket_sign -= 1
        elif sentence[i] == "[":
            branket_sign += 1
        elif sentence[i] == "]":
            branket_sign -= 1
        # if any char in term is in brackets, don't take the mutant
        if i >= term_char_bg and i < term_char_ed:
            if branket_sign > 0:
                in_branket = True
                break
        if i >= term_char_ed:
            break
    return in_branket


def append_jsonl_line(file_obj, item: Any):
    file_obj.write(json.dumps(item, ensure_ascii=False) + '\n')


def count_file_lines(file_path: str) -> int:
    if not os.path.exists(file_path):
        return 0
    with open(file_path, 'r', encoding='utf-8') as file:
        return sum(1 for _ in file)


def truncate_jsonl_lines(file_path: str, keep_lines: int):
    if not os.path.exists(file_path):
        return
    keep_lines = max(0, keep_lines)
    with open(file_path, 'r', encoding='utf-8') as file:
        kept = []
        for idx, line in enumerate(file):
            if idx >= keep_lines:
                break
            kept.append(line)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(kept)


def align_resume_rows(insert_path: str, general_path: str, bert_path: str, logger: logging.Logger) -> int:
    counts = {
        insert_path: count_file_lines(insert_path),
        general_path: count_file_lines(general_path),
        bert_path: count_file_lines(bert_path),
    }
    resume_rows = min(counts.values())
    if len(set(counts.values())) > 1:
        logger.info("output line counts are inconsistent, aligning to min rows=%s", resume_rows)
        for path in counts:
            truncate_jsonl_lines(path, resume_rows)
    return resume_rows


def mutantSentencePhrase(Sentence, terms, meanings, alternativeforms_all, synonyms_all, translations_all, debug_stats: Optional[Counter] = None):
    textlst = splitSentence(Sentence)
    originSentenceLst = getOriginSentenceLst(textlst)
    originSentence = getOriginSentence(Sentence)
    termMuntants = []
    poslstabsolute = []
    poslablst = []
    term_marker_found = False

    # if sentence length is over 50 tokens, don't take the mutant
    if len(originSentence.split()) > 50:
        if debug_stats is not None:
            debug_stats["skip_sentence_too_long"] += 1
        return termMuntants


    for i in range(len(textlst)):

        # generate mutants for each term
        if textlst[i].startswith("[|term:") and textlst[i].endswith("|]"):
            term_marker_found = True
            if debug_stats is not None:
                debug_stats["term_marker_seen"] += 1
            
            # print(textlst[i])
            termMuntant = dict()
            term = textlst[i][7:-2]
            
            
            realterm = term
            
            term_char_bg = Sentence.find(textlst[i])
            term_char_ed = term_char_bg + len(term)
            # if term is in brackets, don't take the mutant
            if judge_term_in_brackets(originSentence, term_char_bg, term_char_ed):
                if debug_stats is not None:
                    debug_stats["skip_term_in_brackets"] += 1
                continue

            # if term exists in terms over 1 time, continue
            if originSentence.lower().count(term.lower()) > 1:
                if debug_stats is not None:
                    debug_stats["skip_term_repeat_in_sentence"] += 1
                continue

            # if term in terms, use term, else use term.lower()
            if term in terms:
                realterm = term
            elif term.lower() in terms:
                realterm = term.lower()
            else:
                if debug_stats is not None:
                    debug_stats["skip_term_not_in_meaningdict"] += 1
                continue



            termMuntant["term"] = realterm
            # phrase term differs from word term in that length of phrase term is more than 1, so we need to record the real index of phrase in sentence

            termMuntant["index"] = sum([len(item.split()) for item in originSentenceLst[:i]])

            if poslstabsolute == []:
                poslstabsolute = posfilter.getSentencePosTags(lst2str(originSentenceLst).split())

            if poslablst == []:
                poslablst = posfilter.getSentencePosTags(originSentenceLst)
            
            # if the term is not a noun, proper noun, or pronoun, don't take the mutant
            if not posfilter.isNounProNoun(poslablst, i):
                if debug_stats is not None:
                    debug_stats["skip_pos_not_noun_pronoun"] += 1
                continue

            candiposlst = posfilter.getPosByIndex(poslablst, i)

            termmeanings = [meaning for meaning in meanings[terms.index(realterm)] if meaning["pos"] in candiposlst]
            alternativeforms = alternativeforms_all[terms.index(realterm)]
            synonyms = synonyms_all[terms.index(realterm)]
            translations = translations_all[terms.index(realterm)]
            if termmeanings == []:
                termmeanings = meanings[terms.index(realterm)]
            if termmeanings == []:
                if debug_stats is not None:
                    debug_stats["skip_no_meaning_candidates"] += 1
                continue
            # insertMutantSentences = []

            candidates = []
            for termmeaning in termmeanings: 
                insertedmeaning = addedmeaning(termmeaning["meaning"])
                candidates.append(Sentence.replace(textlst[i], term+" "+insertedmeaning))

            mostSimilarMutant,indexofmeaning,similarity = chooseMostSimilarMeaningMuntantBge(getOriginSentence(Sentence), candidates)
            
            # termMuntant["indexofmeaning"] = indexofmeaning

            # Mutant1 : insert term meaning into sentence
            tgtmeaning = termmeanings[indexofmeaning]["meaning"]
            insertedmeaning = addedmeaning(tgtmeaning)
            termMuntant["infInsertMutant"] = originSentence.replace(term, term+" "+insertedmeaning)
            termMuntant["infInsertMeaning"] = tgtmeaning
            termMuntant["term_translations"] = translations
            termMuntant["term_synonyms"] = synonyms
            termMuntant["term_alternativeforms"] = alternativeforms

            # print(originSentenceLst)
            # Mutant2 : replace term words with [MASK] and predict, only for phrase
            # to keep the grammar, we only replace term words of "noun"
            allowed_pos_set = {"NN", "NNS", "NNP", "NNPS"}
            term_range = [termMuntant["index"], termMuntant["index"]+len(realterm.split())]
            indexInPos = posfilter.getIndexInPos(poslstabsolute, allowed_pos_set, term_range)
            # relative location of term words in term
            relative_index = [index-term_range[0] for index in indexInPos]
            if relative_index == []:
                # don't take the mutant3
                if debug_stats is not None:
                    debug_stats["skip_bert_no_replaceable_noun_token"] += 1
                termMuntants.append(termMuntant)
                continue
            try:
                bertorigin, bertmutants = bertInsert.get_insert_mutants(originSentenceLst, i, relative_index, originSentence)
            except:
                if debug_stats is not None:
                    debug_stats["skip_bert_exception"] += 1
                termMuntants.append(termMuntant)
                continue

            # if bertmutants == []:, don't take the mutant 3
            if bertmutants == []:
                if debug_stats is not None:
                    debug_stats["skip_bert_empty_candidates"] += 1
                termMuntants.append(termMuntant)
                continue 

            termMuntant["bertorigin"] = bertorigin
            # termMuntant["relative_index"] = poslstabsolute

            # if changed mutant is an alternative form or synonym of term, don't take the mutant
            filtered_bertmutants = []
            mutanted_terms = []
            lower_alternativeforms = [item.lower() for item in alternativeforms]
            lower_synonyms = [item.lower() for item in synonyms]
            avoid_forms = lower_alternativeforms + lower_synonyms
            avoid_forms = list(set(avoid_forms))
            for bertmutant in bertmutants:
                mutanted_term = bertmutant[2]
                if mutanted_term.lower() in lower_alternativeforms or mutanted_term.lower() in lower_synonyms:
                    continue
                for avoid_form in avoid_forms:
                    if avoid_form in mutanted_term.lower() or mutanted_term.lower() in avoid_form:
                        continue
                else:
                    filtered_bertmutants.append(bertmutant)
                    mutanted_terms.append(mutanted_term)
            bertmutants = filtered_bertmutants
            if debug_stats is not None:
                if len(bertmutants) == 0:
                    debug_stats["skip_bert_all_filtered_by_synonym_or_substring"] += 1
                else:
                    debug_stats["bert_nonempty_after_filter"] += 1
            termMuntant['mutanted_terms'] = mutanted_terms
            termMuntant['filtered_terms'] = alternativeforms + synonyms
            termMuntant["bertmutants"] = bertmutants

            termMuntants.append(termMuntant)
            if debug_stats is not None:
                debug_stats["term_mutant_generated"] += 1
    if debug_stats is not None:
        if not term_marker_found:
            debug_stats["skip_sentence_no_term_marker"] += 1
        if len(termMuntants) == 0:
            debug_stats["sentence_no_mutant_items"] += 1
        else:
            debug_stats["sentence_with_mutant_items"] += 1
    return termMuntants

def _build_sentence_outputs(originSentence, refer_trans, term_level, terms, meanings, alternativeforms_all, synonyms_all, translations_all):
    local_stats = Counter()
    local_stats["sentence_pairs_total"] += 1
    try:
        mutantItems = mutantSentencePhrase(originSentence, terms, meanings, alternativeforms_all, synonyms_all, translations_all, local_stats)
    except Exception as e:
        local_stats["sentence_exception"] += 1
        local_stats[f"sentence_exception_{type(e).__name__}"] += 1
        mutantItems = []

    if mutantItems == []:
        local_stats["sentence_dropped_empty_mutants"] += 1
        return None, None, None, local_stats

    local_stats["sentence_kept_non_empty_mutants"] += 1
    insertMutants = []
    bertInsertMutants = []
    for mutantItem in mutantItems:
        if "infInsertMutant" in mutantItem:
            insertMutants.append(mutantItem["infInsertMutant"])
        if term_level == "phrase" and "bertmutants" in mutantItem and len(mutantItem["bertmutants"]) != 0:
            bertInsertMutants.append({
                "bertorigin": mutantItem["bertorigin"],
                "term_origin": mutantItem["term"],
                "bertmutants": str(mutantItem["bertmutants"]),
                "mutanted_terms": str(mutantItem["mutanted_terms"]),
                "filtered_terms": str(mutantItem["filtered_terms"])
            })

    generalMutant = {"mutantItems": mutantItems, "marked_sentence": originSentence, "refer_trans": refer_trans}
    return insertMutants, generalMutant, bertInsertMutants, local_stats


def make_src(meaningdict, input_path, output_path, term_level, tgtarea, breakpoint=0, num_workers=1):


    # set logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(output_path+"/mutant.log")
    file_handler.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    # tqdm_out = TqdmToLogger(logger, level=logging.INFO)


    meanings = []
    terms = []
    alternativeforms_all = []
    synonyms_all = []
    translations_all = []
    logger.info("*"*80)
    logger.info("Reading meaning dict...")


    # Counting part of speech types
    posset = set()

    with open(meaningdict, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        # create dict
        # for line in tqdm(lines, ncols=80, file=tqdm_out):
        for line in lines:
            meaning = json.loads(line)
            if meaning['meanitems'] == []:
                continue
            meanings.append(meaning['meanitems'])
            terms.append(meaning['term'])
            alternativeforms_all.append(meaning['alternative_forms'])
            synonyms_all.append(meaning['synonyms'])
            translations_all.append(meaning['translations'])
            # Counting part of speech types
            for meanitem in meaning['meanitems']:
                posset.add(meanitem['pos'])
    logger.info("Reading meaning dict done!")
    logger.info("*"*80)

    # open datasets and write mutant sentences
    # areas = ["Education"]#, "Laws", "Microblog", "News", "Science", "Spoken", "Subtitles", "Thesis"]
    areas = [tgtarea]
    for area in areas:
        area_stats = Counter()
        phrase_dataset_path = input_path+"/{0}/{1}mark.txt".format(area, 'phrase')
        insertMutant_path = output_path+"/{0}/insertMutant.jsonl".format(area)
        generalMutant_path = output_path+"/{0}/generalMutant.jsonl".format(area)
        bertInsertMutant_path = output_path+"/{0}/bertInsertMutant.jsonl".format(area)
        if not os.path.exists(output_path):
            os.mkdir(output_path)
        if not os.path.exists(output_path+"/{0}".format(area)):
            os.mkdir(output_path+"/{0}".format(area))

        resume_rows = align_resume_rows(insertMutant_path, generalMutant_path, bertInsertMutant_path, logger)
        resume_line = resume_rows * 2
        start_line = max(breakpoint, resume_line)
        if start_line % 2 != 0:
            start_line += 1

        if start_line > 0:
            logger.info("resuming %s from line=%s (pair=%s)", area, start_line, start_line // 2)

        file_mode = 'a' if start_line > 0 else 'w'
        with open(phrase_dataset_path, 'r', encoding='utf-8') as phrase_dataset:
            with open(insertMutant_path, file_mode, encoding='utf-8') as insert_file, \
                 open(generalMutant_path, file_mode, encoding='utf-8') as general_file, \
                 open(bertInsertMutant_path, file_mode, encoding='utf-8') as bert_file:

                phrase_lines = phrase_dataset.readlines()
                total_pairs = len(phrase_lines) // 2
                pair_indices = list(range(start_line, len(phrase_lines), 2))
                logger.info("start processing {0}...".format(area))
                logger.info("processing window for %s: %s/%s pairs", area, start_line // 2, total_pairs)

                if num_workers <= 1:
                    for i in pair_indices:
                        if i % 2000 == 0:
                            logger.info("processing {0}: {1}/{2}...".format(area, i//2, total_pairs))
                        originSentence = phrase_lines[i].strip()
                        refer_trans = phrase_lines[i+1].strip()
                        insertMutants, generalMutant, bertInsertMutants, local_stats = _build_sentence_outputs(
                            originSentence,
                            refer_trans,
                            term_level,
                            terms,
                            meanings,
                            alternativeforms_all,
                            synonyms_all,
                            translations_all,
                        )
                        area_stats.update(local_stats)
                        if generalMutant is None:
                            continue
                        append_jsonl_line(insert_file, insertMutants)
                        append_jsonl_line(general_file, generalMutant)
                        append_jsonl_line(bert_file, bertInsertMutants)
                else:
                    logger.info("using num_workers=%s for area=%s", num_workers, area)
                    with ThreadPoolExecutor(max_workers=num_workers) as executor:
                        future_to_idx = {}
                        pair_iter = iter(pair_indices)
                        max_in_flight = max(num_workers * 4, num_workers)

                        def _submit_next_pair() -> bool:
                            try:
                                i = next(pair_iter)
                            except StopIteration:
                                return False

                            originSentence = phrase_lines[i].strip()
                            refer_trans = phrase_lines[i+1].strip()
                            future = executor.submit(
                                _build_sentence_outputs,
                                originSentence,
                                refer_trans,
                                term_level,
                                terms,
                                meanings,
                                alternativeforms_all,
                                synonyms_all,
                                translations_all,
                            )
                            future_to_idx[future] = i
                            return True

                        for _ in range(min(max_in_flight, len(pair_indices))):
                            if not _submit_next_pair():
                                break

                        done_count = 0
                        while future_to_idx:
                            done_futures, _ = wait(future_to_idx.keys(), return_when=FIRST_COMPLETED)
                            for future in done_futures:
                                _ = future_to_idx.pop(future)
                                insertMutants, generalMutant, bertInsertMutants, local_stats = future.result()
                                area_stats.update(local_stats)
                                done_count += 1
                                if done_count % 1000 == 0:
                                    logger.info("processing %s: %s/%s...", area, done_count + (start_line // 2), total_pairs)
                                if generalMutant is not None:
                                    append_jsonl_line(insert_file, insertMutants)
                                    append_jsonl_line(general_file, generalMutant)
                                    append_jsonl_line(bert_file, bertInsertMutants)
                                _submit_next_pair()

                insert_file.flush()
                general_file.flush()
                bert_file.flush()
            logger.info("Drop stats for %s:", area)
            for key in sorted(area_stats.keys()):
                logger.info("  %s=%s", key, area_stats[key])

# main
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='make csv file for src')
    parser.add_argument('--meaningdict', type=str, help='meaning dict path')
    parser.add_argument('--input_path', type=str, help='input path')
    parser.add_argument('--output_path', type=str, help='output path')
    parser.add_argument('--term_level', type=str, help='term level')
    parser.add_argument('--tgtarea', type=str, help='target area')
    parser.add_argument('--breakpoint', type=int, help='breakpoint', default=0)
    parser.add_argument('--num_workers', type=int, help='thread workers for sentence processing', default=1)

    args = parser.parse_args()
    
    # read meaning dict
    meaningdict = args.meaningdict
    input_path = args.input_path
    output_path = args.output_path
    term_level = args.term_level
    tgtarea = args.tgtarea
    breakpoint = args.breakpoint
    num_workers = args.num_workers
    make_src(meaningdict, input_path, output_path, term_level, tgtarea, breakpoint, num_workers)
