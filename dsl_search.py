"""
A module, which parses DSL files based on user's regexes 
"""
import argparse
import re


def process_answer(ans, ot, ct):
    """
    A function, which strips all the unnecessary parts from the translations
    ans - a list of translations
    ot - opening tag
    ct - closing tag
    """
    parsed_ans = []
    for entry in ans:
        parsed_entry = entry[1:-1]
        if parsed_entry.startswith(ot):
            parsed_entry = parsed_entry[len(ot):]
        if parsed_entry.endswith(ct):
            parsed_entry = parsed_entry[:-len(ct)]

        parsed_ans.append(parsed_entry)

    return parsed_ans


def find_translations(dsl_filepath, word, field_pattern, opening_tag, closing_tag, encoding="utf-16"):
    """
    Parses the dsl file and returns a list of translations

    dsl_filepath - path to a dsl file (it is better, when it is inside CWD)
    word - we are looking for the entry of this word
    field_pattern - pattern for the entry
    opening_tag - a tag, that opens the field in the entry are looking for 
    closing_tag - a tag, that closes the field
    encoding -  encoding of a DSL file
    """

    with open(dsl_filepath, "r", encoding=encoding) as f:

        if field_pattern:
            pattern = re.compile(field_pattern)
        else:
            pattern = re.compile(r"^"+word+r"$")

        lines = f.readlines()
        for line in lines:
            if re.match(pattern, line):
                n = lines.index(line)+1
                sub_line = lines[n]
                while opening_tag not in sub_line:
                    n += 1
                    sub_line = lines[n]
                meaning = lines[n]
                translations = [meaning]

                while closing_tag not in meaning:
                    n += 1
                    meaning = lines[n]
                    translations.append(meaning)

                return process_answer(translations, opening_tag, closing_tag)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("A simple parser for a DSL dictionary")
    parser.add_argument(
        "-f", "--file", help="DSL dictionary file (new regex will be required)")
    parser.add_argument("word", help="The word to search")
    parser.add_argument("-O", "--opening-tag",
                        help="An opening tag/set of tags for a custom dsl dictianry")
    parser.add_argument("-C", "--closing-tag",
                        help="A closing tag/set of tags for a custom dsl dictianry")
    parser.set_defaults(file="japan2.dsl",
                        opening_tag="[m1]", closing_tag="[/m]")

    ar = parser.parse_args()
    if ar.file != "japan2.dsl":
        pattern = input(
            "Enter please a new regex (leave empty for default): ")
    else:
        pattern = None
    print(find_translations(ar.file, ar.word,
                            pattern, ar.opening_tag, ar.closing_tag))
