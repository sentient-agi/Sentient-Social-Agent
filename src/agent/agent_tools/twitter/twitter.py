import datetime
import logging
import tweepy
from pprint import pformat
from .twitter_config import TwitterConfig

logger = logging.getLogger(__name__)
logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)

class Twitter:
    """A class for interfacing with the Twitter API using Tweepy.

    Attributes:
        client (tweepy.Client): The authenticated Tweepy client instance for
            interacting with the Twitter API.
        user_id (str): The ID of the authenticated Twitter user.
    
    Methods:
        get_relevant_conversations(key_users, conversation_ids, start_time):
            Retrieves tweets from specified users or with particular 
            conversation ids and groups them by conversation ID.

        post_tweet(post_text, in_reply_to_tweet_id):
            Posts a new tweet. If `in_reply_to_tweet_id` is not `None` then it 
            posts a reply to the tweet specific by `in_reply_to_tweet_id`.
    """


    def __init__(
            self,
            api_key,
            api_secret,
            access_token,
            access_token_secret,
            bearer_token,
            model):
        """
        Initializes the Twitter class with with the necessary parameters.

        Args:
            api_key (str): The API key for OAuth 1.0a authentication.
            api_secret (str): The API secret for OAuth 1.0a authentication.
            access_token (str): The access token for OAuth 1.0a authentication.
            access_token_secret (str): The access token secret for OAuth 1.0a
                authentication.
            bearer_token (str, optional): The Bearer token for OAuth 2.0
                authentication.

        Sets up the Tweepy client for both OAuth 1.0a and OAuth 2.0 
        authentication and retrieves the authenticated user's ID.
        """
        self.v2api = tweepy.Client(
            bearer_token=bearer_token,
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
            return_type = dict
        )
        self.user_id = self.v2api.get_me()["data"]["id"]

        self.model = model
        self.config = TwitterConfig()
        
        if not self.config.KEY_USERS:
            raise Exception("You need to configure your twitter agent's key users") 


    def __build_search_query_users(self, key_users):
        """Returns a twitter search query for tweets from a list of users"""
        return "(from:" + " OR from:".join(key_users) + ")"


    def __build_search_query_key_phrase(self):
        """Returns a twitter search query for tweets containing key phrase"""
        return f' "{self.config.KEY_PHRASE}"'
    

    def __build_search_query_ignore_retweets(self):
        """Returns a twitter search query that ignores retweets"""
        return " -is:retweet"
    

    def __build_search_query_ignore_quotes(self):
        """Returns a twitter search query that ignores quotes"""
        return " -is:quote"


    def __search_for_relevant_conversations(self, start_time=None):
        """
        Gets tweets from key users or from specific conversations.
        
        Returns tweets grouped by conversation_id.
        """

        # Build search query
        query = self.__build_search_query_users(self.config.KEY_USERS)
        query += self.__build_search_query_ignore_retweets()
        if self.config.KEY_PHRASE:
            query += self.__build_search_query_key_phrase()
        if self.config.QUOTE_MODE:
            query += self.__build_search_query_ignore_quotes()
        logging.debug(f"Twitter search query: {query}")

        # Search for tweets
        response = self.v2api.search_recent_tweets(
            query=query,
            start_time=start_time,
            tweet_fields=["created_at","author_id","conversation_id", "public_metrics"],
            expansions=["author_id","referenced_tweets.id"]
        )
        logging.debug(f"Twitter search results: {response}")

        if not response.get("data", False):
            return {}

        # Create authors lookup dict
        authors = {user["id"]: user["username"] for user in response["includes"]["users"]}
        logging.debug(f"Authors look up dictionary: {authors}")

        # Create tweets lookup dict
        tweets = {tweet["id"]: tweet for tweet in response["data"]}
        logging.debug(f"Tweets look up dictionary: {tweets}")

        conversations = {}
        for tweet in tweets.values():
            author_id = tweet["author_id"]
            conversation_id = tweet["conversation_id"]

            # We only want to consider replies that are part of a thread started
            # by the author
            referenced_tweets = tweet.get("referenced_tweets", [])
            if referenced_tweets:
                # Check that tweet is a reply
                reply = referenced_tweets[0]["type"] == "replied_to"
                # Check that tweet is a reply to another tweet in tweets
                replied_to = tweets.get(referenced_tweets[0]["id"], False)
                # Check that the tweet is a reply to a tweet by the same author
                if reply and ((not replied_to) or (not replied_to["author_id"] == author_id)):
                    continue

            # If there is no entry corresponding to author then intialize
            # object
            authors_conversations = conversations.get(author_id, {})

            # If there is no entry corresponding to conversation then intialize
            # array
            conversation = authors_conversations.get(conversation_id, [])
            
            # Add tweet to conversation
            conversation.append(
                {
                    "id": tweet["id"],
                    "text": tweet["text"],
                    "author_id": tweet["author_id"],
                    "author": authors[tweet["author_id"]],
                    "created_at": tweet["created_at"],
                    "conversation_id": tweet["conversation_id"],
                    "referenced_tweets": referenced_tweets,
                    "public_metrics": tweet["public_metrics"]
                }
            )

            # Sort tweets in conversation from oldest to newest
            sorted_conversation = sorted(conversation, key=lambda k: k["created_at"])

            # Update conversations dictionary
            authors_conversations[conversation_id] = sorted_conversation
            conversations[author_id] = authors_conversations

        return conversations


    def __get_relevant_conversations(self, hours=168):
        """Fetches all conversations involving key_users in past `hours`"""

        logging.debug(f"Key users: {self.config.KEY_USERS}")
        logging.info(f"Fetching relevant conversations from past {hours}hrs...")

        start_time = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=hours)
        relevant_conversations = self.__search_for_relevant_conversations(start_time=start_time)

        logging.info("Relevant conversations:")
        if relevant_conversations:
            logging.info(pformat(relevant_conversations))
        return relevant_conversations


    def __respond_to_conversation(self, conversation, response):
        """Uses model to respond to conversation"""

        logging.debug(pformat(conversation))

        first_tweet_id = conversation[0]["id"]
        last_tweet_id = conversation[-1]["id"]
        reply_tweet_id = last_tweet_id if not self.config.QUOTE_MODE else None
        quote_tweet_id = first_tweet_id if self.config.QUOTE_MODE else None

        self.post_tweet(response, reply_tweet_id, quote_tweet_id)


    def respond_to_key_users(self):
        """Responds to tweets by key users"""

        logging.info("Responding to key users...")
        relevant_conversations = self.__get_relevant_conversations()
        response_count = 0

        # Terminate if there are no relevant conversations
        if not relevant_conversations:
            logging.info("No conversations to respond to.")
            return
        
        for user_conversations in relevant_conversations.values():
            for conversation in user_conversations.values():
                # Terminate if bot has already responded to max no of tweets
                if response_count >= self.config.RESPONSES_PER_RUN:
                    logging.info(f"Responded to max responses.")
                    break

                conversation_id = conversation[0]["conversation_id"]
                logging.info(f"Responding to conversation {conversation_id}...")

                prompt = f"{self.config.RESPONSE_PROMPT} {conversation}"
                try:
                    # Generate response using model and remove quotation marks
                    response = self.model.query(prompt)
                    logging.info(f"Response: {response}")
                
                    # Post response
                    logging.info("Posting response...")
                    self.__respond_to_conversation(conversation, response)
                    response_count += 1

                except Exception as e:
                    logging.exception(f"Error responding to conversation {conversation_id}. {e}")
                
        logging.info("Successfully responded to relevant conversations.")


    def post_tweet(self, post_text, in_reply_to_tweet_id=None, quote_tweet_id=None):
        """Posts a new tweet or a reply to the specified tweet."""
        try:
            response = self.v2api.create_tweet(
                in_reply_to_tweet_id=in_reply_to_tweet_id,
                quote_tweet_id=quote_tweet_id,
                text=post_text
            )
            return (True, response["data"]["id"])
        except Exception as e:
            print(f"Error posting reply: {e}")
            return (False, None)