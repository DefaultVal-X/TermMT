#!/bin/bash
# 加载环境变量
if [ -f ../.env ]; then
    export $(cat ../.env | grep -v '#' | xargs)
fi

for area in "Subtitles" "Science" "Laws" "News" "Thesis"
do
    current_time="detect"
    scripts_path=../scripts/translate
    # 使用 mbart（本地）和 bing（有密钥），跳过 google（需要 JSON 认证）
    for model in "mbart" "bing"
    do
        for trans_file in "originSentences.txt" "phrase_infoinsertmutants.txt" "phrase_bertinsertmutants.txt"
        do

            python ${scripts_path}/translate.py \
                --area $area \
                --time $current_time \
                --model $model \
                --trans_file $trans_file
        done
    done
done