import os
import tweepy
from dotenv import load_dotenv

env_path = os.path.join(os.path.abspath(os.curdir), '.env')
load_dotenv(dotenv_path=env_path)

print("Connecting to twitter...")

# Check that all credentials are present
bearer_token = os.getenv("TWITTER_BEARER_TOKEN", None)
if not bearer_token:
    raise Exception("Please add your bearer token to the .env file.")

consumer_key = os.getenv("TWITTER_CONSUMER_KEY", None)
if not consumer_key:
    raise Exception("Please add your consumer key to the .env file.")

consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET", None)
if not consumer_secret:
    raise Exception("Please add your consumer secret to the .env file.")

access_token = os.getenv("TWITTER_ACCESS_TOKEN", None)
if not access_token:
    raise Exception("Please add your access token to the .env file.")

access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET", None)
if not access_token_secret:
    raise Exception("Please add your access token secret to the .env file.")

# Initialize twitter client
v2api = tweepy.Client(
    bearer_token=bearer_token,
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret,
    return_type = dict
)
user = v2api.get_me()
username = user["data"]["username"]
user_id = user["data"]["id"]

print(f"Connected to twitter user @{username} with id {user_id}.")
