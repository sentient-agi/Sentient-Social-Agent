import logging
from .agent import Agent

try:
    agent = Agent()
    agent.run()
except KeyboardInterrupt:
    logging.info("[AGENT] Agent shutting down...")
    exit()