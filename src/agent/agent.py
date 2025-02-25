import logging
import os
import threading
import importlib
import pkgutil
from . import agent_tools
from dotenv import load_dotenv
from .agent_config import AgentConfig

logger = logging.getLogger(__name__)
logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)

class Agent:
    def __init__(self):
        logger.info("[AGENT] Initializing agent...")
        
        # Load environment variables
        load_dotenv()

        # Load config
        self.config = AgentConfig()

        # Initialize model (done separately because it's used by other tools)
        from .agent_tools.model.model import Model
        self.model = Model(
            api_key=os.getenv("MODEL_API_KEY")
        )

        # Load and initialize tools
        self.tools = {}
        self.__load_tools()


    def __load_tools(self):
        """Automatically load all tools from the agent_tools directory."""
        
        logger.info(f"[AGENT] Loading agent tools...")
        for _, name, _ in pkgutil.iter_modules(agent_tools.__path__):
            # Skip model module because it's handled separately
            if name == 'model':
                continue

            try:
                logger.info(f"[AGENT] Loading {name} tool...")
                # Import module
                module = importlib.import_module(f".agent_tools.{name}.{name}", package=__package__)
                
                # Get main class (assumed to be capitalized version of the module name)
                tool_class = getattr(module, name.capitalize())
                
                # Check if tool is enabled in agent config
                if getattr(self.config, f"{name.upper()}_ENABLED", False):
                    # Get required environment variables
                    env_vars = {
                        key.replace(f"{name.upper()}_", "").lower(): os.getenv(key)
                        for key in os.environ
                        if key.startswith(f"{name.upper()}_")
                    }
                    
                    # Initialize tool with environment variables and model
                    self.tools[name] = tool_class(**env_vars, model=self.model)
                    logger.info(f"[AGENT] Loaded {name} tool.")
            except Exception as e:
                logger.error(f"[AGENT] Failed to load {name} tool. Error: {str(e)}.")


    def run(self):
        """Run the agent and all enabled tools."""

        logger.info("[AGENT] Running agent...")

        # Start each tool in a separate thread
        threads = []
        logger.info(f"[AGENT] Running agent tools...")
        for name, tool in self.tools.items():
            try:
                thread = threading.Thread(target=tool.run)
                thread.start()
                threads.append(thread)
                logger.info(f"[AGENT] Running {name} tool...")
            except Exception as e:
                logger.error(f"[AGENT] Failed to run {name} tool. Error: {str(e)}.")

        # Wait for all threads to finish
        for thread in threads:
            thread.join()