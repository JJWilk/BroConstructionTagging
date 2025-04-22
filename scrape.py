from twikit import Client, TooManyRequests
import time
from datetime import datetime
import csv
from configparser import ConfigParser
from random import randint
import asyncio

#login
config = ConfigParser()
config.read("config.ini")
username = config['X']['username']
email = config['X']['email']
password = config['X']['password']
client = Client(language='en-US')

#authenticate
async def authenticate():
    # await client.login(auth_info_1=username, auth_info_2=email, password=password)
    # client.save_cookies('cookies.json')
    client.load_cookies('cookies.json')


#get tweets
async def grab_tweets(query, MIN_TWEETS, year):
    tweet_data = []
    tweets = None
    tweet_count = 0
    while tweet_count < MIN_TWEETS:
        if not tweets:
            print("Getting first result for year", year)
            tweets = await client.search_tweet(query, product='Top')
        else:
            wait_time = randint(5, 9)
            print("Waiting", wait_time, "seconds")
            time.sleep(wait_time)
            tweets = await tweets.next()

        for tweet in tweets:
            tweet_count += 1
            tweet_data.append([year, tweet.text, tweet.user.name, tweet.created_at])
    return tweet_data

MIN_TWEETS = 100

#login
asyncio.run(authenticate())

async def make_database():
    tweet_database = {}
    #get 100 tweets for each year, add +1 to the year
    for i in range(24, 25):
        year = str(2000 + i)
        query = "\"bro\" until:" + year + "-12-31 since:"+ year + "-01-01"
        tweets = await grab_tweets(query, MIN_TWEETS, year)
        tweet_database[year] = tweets
    return tweet_database

tweet_database = asyncio.run(make_database())

with open('tweets.csv', 'a', newline='', encoding='UTF-8') as file:
    writer = csv.writer(file)

    for key in tweet_database:
        for entry in tweet_database[key]:
            writer.writerow(entry)

print("Done!")