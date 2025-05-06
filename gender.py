import csv

with open('tweets_labelled.csv', 'r', encoding='UTF-8') as file:
    csvreader = csv.reader(file)
    header = next(csvreader)
    names = []
    for row in csvreader:
        if row[4] == "pronoun":
            names.append(row[2])

import nomquamgender as nqg
model = nqg.NBGC()

male = 0
female = 0
unknown = 0
for name in names:
    result = model.classify(name)[0]
    if result == "gm":
        male += 1
    elif result == "gf":
        female += 1
    elif result == "-":
        unknown += 1

print("Male", male, "Female", female, "Unknown", unknown)

#pronoun construction
#male: 43 female: 6

#non pronoun construction
#male:627 female:197 unknown 1275
# 
#all
# male: female: 