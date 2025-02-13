import os
import logging
from dotenv import load_dotenv
from .agent_tools.model.model import Model
from .agent_tools.twitter.twitter import Twitter
from .agent_config import AgentConfig

logger = logging.getLogger(__name__)
logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)

class Agent:
    def __init__(self):
        # Load environment variables
        load_dotenv()

        # Load config
        self.config = AgentConfig()

        # Initialize model
        self.model = Model(
            api_key=os.getenv("MODEL_API_KEY")
        )

        # Initialize twitter client if twitter is enabled
        if self.config.TWITTER_ENABLED:
            self.twitter = Twitter(
                api_key=os.getenv("TWITTER_API_KEY"),
                api_secret=os.getenv("TWITTER_API_SECRET"),
                access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
                access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
                bearer_token=os.getenv("TWITTER_BEARER_TOKEN"),
                model = self.model
            )


def main():
    try:
        logging.info("Agent starting up...")
        agent = Agent()
        agent.twitter.respond_to_key_users()
        logging.info("Agent shutting down...")
    except KeyboardInterrupt:
        logging.info("Agent shutting down...")


if __name__ == "__main__":
    main()
