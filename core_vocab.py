#!/usr/bin/env python3

from collections import defaultdict

from pysblgnt import morphgnt_rows
import yaml


GLOSS_OVERRIDES = {
    "Μωϋσῆς": "Moses",
    "ἐλεάω": "I have pity, show mercy",
    "πίμπλημι": "I fill, am fulfilled",
    "μήν": "a month; certainly",
    "ὀψία": "evening",
    "πώς": "how",
    "περισσοτέρως": "abundantly",
    "κύκλῳ": "around",
    "ἕλκω": "I drag",
    "γαμίζω": "I give in marriage, marry",
    "ἐραυνάω": "I search, look into",
    "στάδιος": "one eighth of a Roman mile",
    "Ναζαρέθ": "Nazareth",
    "ἱνατί": "why",
    "Μαθθαῖος": "Matthew",
    "μήγε": "not",
    "ἕνεκα": "for the sake of",
    "ἀκριβέστερον": "strictest",
    "διαρρήγνυμι": "I tear, break",
    "δεσμόν": "bond",
    "ἑκατόνταρχος": "a centurion",
    "Ἰσκαριώθ": "Iscariot",
    "ὑπερεκπερισσοῦ": "immeasurably",
    "ἐχθές": "yesterday",
    "εἵνεκεν": "because of",
    "βραχύ": "short",
    "ψίξ": "crumb",
    "ἔνθεν": "from here",
    "ἄχρις": "as far as",
    "ὑπερλίαν": "exceedingly",
    "ἐάνπερ": "if indeed",
    "ἀνάγαιον": "upper room",
    "νηφάλιος": "temperate",
    "ἄγε": "come!",
    "αὔξω": "I increase",
    "Μαθθάτ": "Matthat",
    "ἀνεπίλημπτος": "above reproach",
    "Βηθσαϊδάν": "Bethsaida",
    "σύμφορον": "benefit",
    "ὠτάριον": "ear",
    "Βόες": "Boaz",
    "Ἰωβήδ": "Obed",
    "δεκαοκτώ": "eighteen",
    "Ἀσάφ": "Asaph",
    "Μαθθίας": "Matthias",
    "κρυφαῖος": "hidden, secret",
    "προσαίτης": "beggar",
    "Ναζαρά": "Nazareth",
    # "πυκνά": "often",
    # "Ἄρειος": "Ares",
    # "Πάγος": "Hill",
    # "βασίλειον": "palace",
    # "ταπεινόφρων": "humble",
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
        count_by_form[(row["norm"], row["lemma"])] += 1
        total_item_count += 1


def output(f, counts, limit):
    cumulative_count = 0
    items_learnt = 0
    min_count = 0
    for item, count in sorted(counts.items(), key=lambda element: element[1], reverse=True):
        if count < min_count:
            break
        if isinstance(item, tuple):
            form, lemma = item
            print("{} [{}] {} {}".format(form, count, lemma, get_gloss(lemma)), file=f)
        else:
            print("{} [{}] {}".format(item, count, get_gloss(item)), file=f)
        cumulative_count += count
        items_learnt += 1
        if cumulative_count > total_item_count * limit:
            min_count = count

with open("lemma_50.txt", "w") as f:
    output(f, count_by_lemma, 0.5)

with open("lemma_80.txt", "w") as f:
    output(f, count_by_lemma, 0.8)

with open("lemma_90.txt", "w") as f:
    output(f, count_by_lemma, 0.9)

with open("lemma_95.txt", "w") as f:
    output(f, count_by_lemma, 0.95)

with open("form_50.txt", "w") as f:
    output(f, count_by_form, 0.5)

with open("form_80.txt", "w") as f:
    output(f, count_by_form, 0.8)

with open("form_90.txt", "w") as f:
    output(f, count_by_form, 0.9)
