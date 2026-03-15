import argparse
import json
import os
import xml.etree.ElementTree as ET


def strip_namespace(tag: str) -> str:
    if "}" in tag:
        return tag.split("}", 1)[1]
    return tag


def find_child(elem: ET.Element, child_name: str):
    for child in elem:
        if strip_namespace(child.tag) == child_name:
            return child
    return None


def find_text(elem: ET.Element, child_name: str):
    child = find_child(elem, child_name)
    if child is None:
        return None
    return child.text


def parse_page(page_elem: ET.Element, include_redirects: bool):
    namespace = find_text(page_elem, "ns")
    if namespace is not None and namespace != "0":
        return None

    title = find_text(page_elem, "title")
    if not title:
        return None

    redirect = find_child(page_elem, "redirect")
    if redirect is not None and not include_redirects:
        return None

    revision = find_child(page_elem, "revision")
    if revision is None:
        return None

    text_elem = find_child(revision, "text")
    if text_elem is None:
        return None

    text = text_elem.text
    if text is None:
        return None

    return {"title": title, "text": text}


def convert_xml_to_jsonl(input_xml: str, output_jsonl: str, include_redirects: bool, max_pages: int):
    os.makedirs(os.path.dirname(output_jsonl), exist_ok=True)

    parsed_count = 0
    written_count = 0

    with open(output_jsonl, "w", encoding="utf-8") as output_file:
        context = ET.iterparse(input_xml, events=("start", "end"))
        _, root = next(context)

        for event, elem in context:
            if event != "end" or strip_namespace(elem.tag) != "page":
                continue

            parsed_count += 1
            page_item = parse_page(elem, include_redirects)
            if page_item is not None:
                output_file.write(json.dumps(page_item, ensure_ascii=False) + "\n")
                written_count += 1

            elem.clear()
            root.clear()

            if max_pages > 0 and parsed_count >= max_pages:
                break

            if parsed_count % 50000 == 0:
                print(f"[xml->jsonl] parsed={parsed_count}, written={written_count}")

    print(f"[xml->jsonl] done: parsed={parsed_count}, written={written_count}, output={output_jsonl}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_xml", type=str, required=True)
    parser.add_argument("--output_jsonl", type=str, required=True)
    parser.add_argument("--include_redirects", action="store_true")
    parser.add_argument("--max_pages", type=int, default=0)
    args = parser.parse_args()

    convert_xml_to_jsonl(
        input_xml=args.input_xml,
        output_jsonl=args.output_jsonl,
        include_redirects=args.include_redirects,
        max_pages=args.max_pages,
    )


if __name__ == "__main__":
    main()
