import spacy
import csv
from collections import Counter

with open("bro.txt", 'r') as f:
    lines = f.readlines()

next_words = []
next_pos = []
nlp = spacy.load("en_core_web_sm")
for line in lines:
    line = line.lower()

    tokens = nlp(line)

    next_w = ""
    flag = False
    for word in tokens:
        next_w = word
        if flag:
            break
        if word.text == "bro":
            flag = True
    next_words.append(next_w.text)
    next_pos.append(next_w.tag_)

count_word = Counter(next_words)
count_pos = Counter(next_pos)
print(count_word)
print(count_pos)