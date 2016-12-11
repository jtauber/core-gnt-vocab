#!/usr/bin/env python3

from collections import defaultdict

from pysblgnt import morphgnt_rows

def format_verse(bcv):
    return {
        "04": "John",
        "23": "1 John",
        "24": "2 John",
        "25": "3 John",
    }[bcv[:2]] + " " + str(int(bcv[2:4])) + "." + str(int(bcv[4:6]))

count_by_lemma = defaultdict(int)
count_by_form = defaultdict(int)
total_item_count = 0

lemma_frequencies_by_verse = defaultdict(list)

for book_num in [4, 23, 24, 25]:
    for row in morphgnt_rows(book_num):
        count_by_lemma[row["lemma"]] += 1
        count_by_form[row["norm"]] += 1
        total_item_count += 1


word_score = {}

cumulative_count = 0

for item, count in sorted(count_by_form.items(), key=lambda element: element[1], reverse=True):
    cumulative_count += count
    word_score[item] = 100 - int(100 * cumulative_count / total_item_count)


word_scores_by_verse = defaultdict(list)
text_by_verse = defaultdict(list)

for book_num in [4, 23, 24, 25]:
 for row in morphgnt_rows(book_num):
    word_scores_by_verse[row["bcv"]].append(word_score[row["norm"]])
    text_by_verse[row["bcv"]].append(row["text"])

def h_index(verse):
    for i, score in enumerate(sorted(word_scores_by_verse[verse], reverse=True)):
        if 100 * (i + 1) / len(word_scores_by_verse[verse]) >= score:
            return score

h_index_by_verse = {}

for verse in word_scores_by_verse:
    h_index_by_verse[verse] = h_index(verse)

for verse, score in sorted(h_index_by_verse.items(), key=lambda element: element[1], reverse=True):
    line1 = []
    line2 = []
    for word, wscore in zip(text_by_verse[verse], word_scores_by_verse[verse]):
        l = max(len(word), len(str(wscore)))
        line1.append(("{:" + str(l) + "s}").format(word))
        line2.append(("{:" + str(l) + "s}").format(str(wscore)))
    print(" ".join(line1))
    print(" ".join(line2))
    print("{} [{}]".format(format_verse(verse), score))
    print()
