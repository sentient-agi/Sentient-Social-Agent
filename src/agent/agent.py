import ast
import datetime
import os
import logging
from dotenv import load_dotenv
from pprint import pformat
from .agent_tools.heygen import Heygen
from .agent_tools.model import Model
from .agent_tools.twitter import Twitter
from .agent_config.config import Config

logger = logging.getLogger(__name__)
logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)

class Agent:
    # Agent will respond to tweets from these users
    KEY_USERS = ["testfollower001"]

    # Agent will post this number of respones per run
    RESPONSES_PER_RUN = 5

    def __init__(self):
        # Load environment variables
        load_dotenv()

        # Initialize config
        self.config = Config()

        # Initialize model
        self.model = Model(
            api_key=os.getenv("MODEL_API_KEY"),
            url=os.getenv("MODEL_URL"),
            model=os.getenv("MODEL_NAME")
        )

        # Initialize twitter handler
        self.twitter = Twitter(
            api_key=os.getenv("TWITTER_API_KEY"),
            api_secret=os.getenv("TWITTER_API_SECRET"),
            access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
            access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
            bearer_token=os.getenv("TWITTER_BEARER_TOKEN")
        )

        # Initialize heygen
        self.heygen = Heygen(
            api_key=os.getenv("HEYGEN_API_KEY")
        )


    def __construct_data_prompt(self):
        return self.config.data_prompt + pformat(self.data)


    def __construct_post_prompt(self, processed_data):
        return self.config.purpose_prompt + self.config.post_prompt + processed_data


    def __construct_repsonse_prompt(self, conversation):
        return self.config.purpose_prompt + self.config.reply_prompt + pformat(conversation)
    

    def __process_data(self):
        prompt = self.__construct_data_prompt()
        return self.model.query(prompt)


    def __get_threads(self, conversation_ids):
        """Fetches all tweets in conversations"""

        logging.debug(f"Conversation_ids: {conversation_ids}")
        logging.info(f"Fetching tweets in relevant threads...")

        relevant_conversations = self.twitter.get_relevant_conversations(conversation_ids=conversation_ids)

        logging.info(f"Found {len(relevant_conversations)} relevant threads")
        if relevant_conversations:
            logging.info(pformat(relevant_conversations))
        return relevant_conversations


    def __get_relevant_conversations(self, hours=2):
        """Fetches all conversations involving key_users in past `hours`"""

        logging.debug(f"Key users: {self.KEY_USERS}")
        logging.info(f"Fetching relevant conversations from past {hours}hrs...")

        start_time = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=hours)
        relevant_conversations = self.twitter.get_relevant_conversations(
            key_users=self.KEY_USERS,
            start_time=start_time)

        logging.info(f"Found {len(relevant_conversations)} relevant conversations")
        if relevant_conversations:
            logging.info(pformat(relevant_conversations))
        return relevant_conversations


    def __respond_to_conversation(self, conversation):
        """Uses model to respond to conversation"""

        first_tweet = conversation[0]
        last_tweet = conversation[-1]
        conversation_id = first_tweet["conversation_id"]
        logging.info(f"Responding to conversation {conversation_id}...")

        prompt = self.__construct_repsonse_prompt(conversation)
        try:
            # Generate response using model and remove quotation marks
            response = self.model.query(prompt)[1:-1]
            logging.info(f"Response: {response}")
        
            # Post response
            logging.info("Posting response...")
            self.twitter.post_tweet(response, last_tweet["id"])
            
        except Exception as e:
            logging.warning(f"Error processing conversation {conversation_id}: {e}")
        

    def respond_to_key_users(self):
        """Responds to tweets by key users"""

        logging.info("Responding to key users...")
        relevant_conversations = self.__get_relevant_conversations()

        if not relevant_conversations:
            logging.info("No conversations to respond to.")
            return
        
        threads = self.__get_threads(relevant_conversations.keys())
        
        response_count = 0
        for conversation in relevant_conversations.values():
            # Ensure that agent does not repsond to too many tweets
            if response_count >= self.RESPONSES_PER_RUN:
                break
            
            conversation_id = conversation[0]["conversation_id"]
            thread = threads.get(conversation_id, False)

            if thread:
                sorted_thread = sorted(thread, key=lambda k: k["created_at"])
                first_tweet = sorted_thread[0]
                # If the thread was started by a key user or by an agent 
                # respond to it
                if ((first_tweet["author"] in self.KEY_USERS) or
                    (first_tweet["author"] == self.twitter.user_id)):
                    self.__respond_to_conversation(sorted_thread)
                    response_count+=1
                else:
                    logging.info(f"Skipping conversation {conversation_id}. Thread was not started by key user or agent.")
                    continue
            else:
                self.__respond_to_conversation(conversation)
                response_count+=1

        logging.info("Successfully responded to relevant conversations.")


    def post_tweet(self):
        """Post new tweets"""
        
        logging.info("Generating new tweets...")

        # Process data
        # processed_data = self.__process_data()

        # Construct prompt
        logging.info("efore")
        # prompt = self.__construct_post_prompt(processed_data)
        prompt = "Make a tweet about taking over the digital world"
        # return;

        try:
            # Generate response using model
            response = self.model.query(prompt)
            logging.debug(f"Model response: {response}")
            tweets = [s.strip('"') for s in response.split('\n') if s.strip()]
            logging.info(f"Generated tweets: {tweets}")
        
            # Generate and post the tweets as a twitter thread with videos
            logging.info("Generating and posting tweets with videos...")
            
            # Post the first tweet
            video_url = self.heygen.generate_video(tweets[0])
            media_id = self.twitter.upload_video(video_url)
            twitter_response = self.twitter.post_tweet(
                post_text=tweets[0],
                media_id=media_id
            )
            in_reply_to_tweet_id = twitter_response[1]

            # Post the rest of the tweets in the thread
            for tweet in tweets[1:]:
                video_url = self.heygen.generate_video(tweet)
                media_id = self.twitter.upload_video(video_url)
                twitter_response = self.twitter.post_tweet(
                    post_text=tweet,
                    in_reply_to_tweet_id=in_reply_to_tweet_id,
                    media_id=media_id
                )
                in_reply_to_tweet_id = twitter_response[1]

        except Exception as e:
            logging.warning(f"Error generating or posting tweet: {e}")


def main():
    try:
        logging.info("Agent starting up...")
        agent = Agent()
        # agent.respond_to_key_users()
        agent.post_tweet()
        logging.info("Agent shutting down...")
    except KeyboardInterrupt:
        logging.info("Agent shutting down...")


if __name__ == "__main__":
    main()
