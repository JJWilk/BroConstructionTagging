import csv
from transformers import pipeline


with open('tweets_labelled.csv', 'r', encoding='UTF-8') as file:
    csvreader = csv.reader(file)
    header = next(csvreader)
    rows = []
    for row in csvreader:
        rows.append(row)

only_text = [row[1] for row in rows]
sentiment_pipeline = pipeline(model="finiteautomata/bertweet-base-sentiment-analysis")
result = sentiment_pipeline(only_text)

with open('tweets_labelled_sentiment.csv', 'w', newline='', encoding='UTF-8') as file:
    writer = csv.writer(file)
    i = 0
    for row in rows:
        label = result[i]['label']
        row.append(label)
        writer.writerow(row)
        i += 1
    