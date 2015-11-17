#!/usr/bin/env python3

from collections import defaultdict

from pysblgnt import morphgnt_rows
import yaml


GLOSS_OVERRIDES = {
    "Μωϋσῆς": "Moses",
}


def get_gloss(lemma):
    if lemma in GLOSS_OVERRIDES:
        return GLOSS_OVERRIDES[lemma]

    if "gloss" not in lexical_entries[lemma]:
        print("no gloss for {}".format(lemma))
        quit()
    return lexical_entries[lemma]["gloss"]


# assumes it's in a directory nextdoor
with open("../morphological-lexicon/lexemes.yaml") as f:
    lexical_entries = yaml.load(f)


count_by_lemma = defaultdict(int)
count_by_form = defaultdict(int)
total_item_count = 0

for book_num in range(1, 28):
    for row in morphgnt_rows(book_num):
        count_by_lemma[row["lemma"]] += 1
        count_by_form[row["norm"]] += 1
        total_item_count += 1


def output(f, counts, limit):
    cummulative_count = 0
    items_learnt = 0

    for item, count in sorted(counts.items(), key=lambda element: element[1], reverse=True):
        print("{} [{}] {}".format(item, count, get_gloss(item)), file=f)
        cummulative_count += count
        items_learnt += 1
        if cummulative_count > total_item_count * limit:
            break

with open("lemma_50.txt", "w") as f:
    output(f, count_by_lemma, 0.5)

with open("lemma_80.txt", "w") as f:
    output(f, count_by_lemma, 0.8)
