class ModelConfig:
    def __init__(self):
        # Model provider URL
        self.BASE_URL = "https://api.fireworks.ai/inference/v1" 

        # Identifier for specific model that should be used
        self.MODEL = "accounts/sentientfoundation/models/dobby-unhinged-llama-3-3-70b-new"

        # Temperature setting for response randomness
        self.TEMPERATURE = 0.0

        # Maximum number of tokens for responses
        self.MAX_TOKENS = None
       
        # A system message or prompt to guide model behavior
        self.SYSTEM_PROMPT = "default"