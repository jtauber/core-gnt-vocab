#!/usr/bin/env python3

import glob

for in_filename in glob.glob("lemma_*.txt"):
    out_filename = in_filename.replace(".txt", ".tsv")

    with open(in_filename) as f_in, open(out_filename, "w") as f_out:
        print("lemma", "count", "gloss", sep="\t", file=f_out)
        for line in f_in:
            lemma, count, gloss = line.strip().split(maxsplit=2)
            print(lemma, count.strip("[]"), gloss, sep="\t", file=f_out)


for in_filename in glob.glob("form_*.txt"):
    out_filename = in_filename.replace(".txt", ".tsv")

    with open(in_filename) as f_in, open(out_filename, "w") as f_out:
        print("form", "count", "lemma", "gloss", sep="\t", file=f_out)
        for line in f_in:
            form, count, lemma, gloss = line.strip().split(maxsplit=3)
            print(form, count.strip("[]"), lemma, gloss, sep="\t", file=f_out)
