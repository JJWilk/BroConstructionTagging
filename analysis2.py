import csv
import spacy
from transformers import pipeline
nlp = spacy.load("en_core_web_sm")
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

with open('tweets.csv', 'r', encoding='UTF-8') as file:
    csvreader = csv.reader(file)
    header = next(csvreader)
    rows = []
    for row in csvreader:
        rows.append(row)

with open('bro.txt', 'r') as file:
    bros = file.readlines()

def classify_bro(sentence):
    doc = nlp(sentence)
    for token in doc:
        if token.text.lower() == "bro":
            if token.dep_ == "nsubj" and not any(child.dep_ in {"amod", "poss", "det"} for child in token.children):
                return "pronoun"
            if any(child.dep_ in {"amod", "poss", "det"} for child in token.children) or token.head.dep_ in {"poss"}:
                return "conventional"
    return "unknown"

def classify_bro_zero_shot(sentence):
    labels = ["bro is used as a pronoun, as in bro is wild", "bro is used conventionally, as in my little bro is cool"]
    result = classifier(sentence, candidate_labels=labels)
    if result["labels"][0] == labels[0]:
        return "pronoun"
    return "conventional"

with open('tweets_labelled.csv', 'w', newline='', encoding='UTF-8') as file:
    writer = csv.writer(file)

    for row in rows:
        result = classify_bro(row[1])
        if result == "unknown":
            result = "conventional"
        row.append(result)
        writer.writerow(row)

print('DONE :)')