import discord
import os
from dotenv import load_dotenv

env_path = os.path.join(os.path.abspath(os.curdir), '.env')
load_dotenv(dotenv_path=env_path)

class MyClient(discord.Client):
    async def on_ready(self):
        print(f"Connected to discord bot {self.user.name} with id {self.user.id}.")

try:
    print("Connecting to discord...")

    # Check that all credentials are present
    token = os.getenv("DISCORD_TOKEN", None)
    if not token:
        raise Exception("Please add your discord token to the .env file.")

    # Initialize discord client
    intents = discord.Intents.default()
    intents.message_content = True

    client = MyClient(intents=intents)
    client.run(token, log_handler=None)

    print()
    print("Disconnecting from discord...")
except KeyboardInterrupt:
    client.close()
    print()
    print("Disconnecting from model...")