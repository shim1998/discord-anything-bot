import os
from dotenv import load_dotenv
import tweepy

load_dotenv()

auth = tweepy.OAuth2BearerHandler(os.getenv('BEARER_TOKEN'))
api = tweepy.API(auth)
with open('tweets.txt', 'a', encoding='utf-8') as file:
    for tweet in api.user_timeline(screen_name='GenshinAnything'):
        file.write(tweet.text + '\n')
