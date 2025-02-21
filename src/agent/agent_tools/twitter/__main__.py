import os
import tweepy
from dotenv import load_dotenv

env_path = os.path.join(os.path.abspath(os.curdir), '.env')
load_dotenv(dotenv_path=env_path)

print("Connecting to twitter...")

v2api = tweepy.Client(
    bearer_token=os.getenv("TWITTER_BEARER_TOKEN"),
    consumer_key=os.getenv("TWITTER_API_KEY"),
    consumer_secret=os.getenv("TWITTER_API_SECRET"),
    access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
    access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
    return_type = dict
)
user = v2api.get_me()
username = user["data"]["username"]
user_id = user["data"]["id"]

print(f"Connected to twitter user @{username} with id {user_id}.")
