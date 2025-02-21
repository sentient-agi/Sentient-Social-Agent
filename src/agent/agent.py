import logging
import os
from dotenv import load_dotenv
from .agent_tools.model.model import Model
from .agent_tools.twitter.twitter import Twitter
from .agent_tools.discord.discord import Discord
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
            logging.info("Twitter client starting up...")
            self.twitter = Twitter(
                api_key=os.getenv("TWITTER_API_KEY"),
                api_secret=os.getenv("TWITTER_API_SECRET"),
                access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
                access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
                bearer_token=os.getenv("TWITTER_BEARER_TOKEN"),
                model=self.model
            )

        # Initialize discord client if discord is enabled
        if self.config.DISCORD_ENABLED:
            logging.info("Discord client starting up...")
            self.discord = Discord(
                token=os.getenv("DISCORD_TOKEN"),
                model = self.model
            )


def main():
    try:
        logging.info("Agent starting up...")
        agent = Agent()
    except KeyboardInterrupt:
        logging.info("Agent shutting down...")


if __name__ == "__main__":
    main()
