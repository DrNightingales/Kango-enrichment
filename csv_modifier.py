"""
Script, which updates CSV with readings and translations
"""
import csv
import pykakasi
from dsl_search import find_translations

from argparse import ArgumentParser as AP

# Parser for command line argumnets
parser = AP(
    description="Add hiragana readings and translations to a list of Kango ")
parser.add_argument("input", help="Specify an input CSV file")
parser.add_argument("output", help="Specify an output CSV file")
parser.add_argument("-d", "--delimiter",
                    help="A delimeter in the CSV file, default=|")
parser.add_argument("-o", "--opening-tag",
                    help="An opening tag/set of tags for a custom dsl dictianry")
parser.add_argument("-c", "--closing-tag",
                    help="A closing tag/set of tags for a custom dsl dictianry")
parser.add_argument(
    "-f", "--file", help="DSL dictionary file (new regex will be required)")
parser.set_defaults(file="japan2.dsl",
                    opening_tag="[m1]", closing_tag="[/m]", delimiter="|")


args = parser.parse_args()

if args.file != "japan2.dsl":
    pattern = input("Enter please a new regex(leave empty for default): ")
else:
    pattern = None


kks = pykakasi.kakasi()  # Japanese syntactic analizer
kks.setMode("J", "H")  # Japanese (kanji included) -> hiragana
converter = kks.getConverter()


def write_a_file(mode="x"):
    with open(args.output, mode) as f:
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

    if not row["trans"]:
        trans = find_translations(
            args.file, row["kango"], pattern, args.opening_tag, args.closing_tag)
        if not trans:
            row["trans"] = None
        elif len(trans) > 1:
            row["trans"] = ", ".join(trans)
        elif len(trans) == 1:
            row["trans"] = trans[0]
        else:
            row["trans"] = None
try:
    write_a_file()
except FileExistsError as e:
    resp = input(
        f"The file {args.output} exists and will be overwritten\nProceed? [y/N]: ")
    if resp.lower() in ("y", "yes"):
        write_a_file("w")
