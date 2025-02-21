import discord
import logging
from .discord_config import DiscordConfig


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.basicConfig(format="%(levelname)s: %(message)s")

class Discord(discord.Client):
    def __init__(
            self,
            token,
            model):
        self.model = model

        self.config = DiscordConfig()
    
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        super().run(token, log_level=logging.WARNING)


    async def on_ready(self):
        logging.info(f"Connected to discord bot {self.user.name} with id {self.user.id}.")


    async def on_message(self, message):
        logging.info(f"Message received: {message.content}")
        if message.author == self.user:
            return

        prompt = f"{self.config.RESPONSE_PROMPT} {message.content}"
        try:
            # Generate response using model
            response = self.model.query(prompt)
            logging.info(f"Response: {response}")
        
            # Post response
            logging.info("Sending response...")
            await message.channel.send(response)

        except Exception as e:
            logging.exception(f"Error responding to message {message.id}. {e}")

    