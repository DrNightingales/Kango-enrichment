"""
Script, which updates CSV with readings and translations
"""
import csv
import json
import pykakasi
import random as rnd
from dsl_search import find_translations
from querry_tatoeba_links_db import querry
from argparse import ArgumentParser as AP


# Parser for command line argumnets
parser = AP(
    description="Add hiragana readings and translations to a list of Kango ")
parser.add_argument("input", help="Specify an input CSV file")
parser.add_argument("output", help="Specify an output file")
parser.add_argument("-d", "--delimiter",
                    help="A delimeter in the CSV file, default=|")
parser.add_argument("-o", "--opening-tag",
                    help="An opening tag/set of tags for a custom dsl dictianry")
parser.add_argument("-c", "--closing-tag",
                    help="A closing tag/set of tags for a custom dsl dictianry")
parser.add_argument(
    "-f", "--file", help="DSL dictionary file (new regex will be required)")
tatoeba_group = parser.add_mutually_exclusive_group(required=False)
tatoeba_group.add_argument(
    '-t', '--tatoeba', dest='tatoeba', action='store_true')
tatoeba_group.add_argument('-T', '--no-tatoeba',
                           dest='tatoeba', action='store_false')

parser.set_defaults(file="japan2.dsl",
                    opening_tag="[m1]", closing_tag="[/m]", delimiter="|", tatoeba=True)


args = parser.parse_args()

if args.file != "japan2.dsl":
    pattern = input("Enter please a new regex(leave empty for default): ")
else:
    pattern = None


kks = pykakasi.kakasi()  # Japanese syntactic analizer
kks.setMode("J", "H")  # Japanese (kanji included) -> hiragana
converter = kks.getConverter()


def retrieve_examples(kango):
    """
    Retrieves examples from a DB compiled from takaka's corpus/tatoeba project
    Returns a dictionary, with the length no more, than 10
    """
    examples = querry(kango)  # Getting unparsed dictionary

    if len(examples) > 10:  # Cutting the length of the dictionary
        examples_keys = rnd.choices(tuple(examples.keys()), k=10)
        examples = {
            k: examples[k] for k in examples_keys
        }

    parsed_examples = dict()
    # Removing specific syntax
    for example in tuple(examples.items()):
        stack = []
        sentence = []
        append_status = True
        ignore_next = False
        for literal in example[0]:
            if literal == " ":
                sentence.extend(stack)
                stack = []
            elif literal == "(" or literal == "[":
                append_status = False
            elif literal == "{":
                stack = []
            elif literal == "|":
                ignore_next = True
            elif literal == ")" or literal == "]":
                append_status = True
            else:
                if append_status and literal != "~" and not ignore_next and literal != "}":
                    stack.append(literal)
                ignore_next = False
        sentence.extend(stack)
        parsed_examples["".join(sentence)] = example[1]
    return parsed_examples


def write_a_file(mode="x"):
    """
    A function to write a file in a specified format
    """
    with open(args.output, mode) as f:
        if args.tatoeba:
            json.dump(kango_list, f, ensure_ascii=False)
        else:
            writer = csv.DictWriter(f, fldnames, delimiter=args.delimiter)
            for row in kango_list:
                writer.writerow(row)


with open(args.input, "r") as f:
    reader = csv.DictReader(f, delimiter=args.delimiter)
    fldnames = reader.fieldnames
    kango_list = [row for row in reader]

for row in kango_list:
    if not row["reading"]:
        row["reading"] = converter.do(row["kango"])

    if not row["translation"]:
        trans = find_translations(
            args.file, row["kango"], pattern, args.opening_tag, args.closing_tag)
        if not trans:
            row["translation"] = None
        elif len(trans) > 1:
            row["translation"] = ", ".join(trans)
        elif len(trans) == 1:
            row["translation"] = trans[0]
        else:
            row["translation"] = None
    if args.tatoeba:
        row["examples"] = retrieve_examples(row["kango"])
try:
    write_a_file()
except FileExistsError as e:
    resp = input(
        f"The file {args.output} exists and will be overwritten\nProceed? [y/N]: ")
    if resp.lower() in ("y", "yes"):
        write_a_file("w")
