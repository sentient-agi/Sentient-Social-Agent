import os

class Config:
    """
    A class to manage and load configuration data, specifically prompts, from local text files.

    Attributes:
        purpose_prompt (str): The content of the purpose prompt file.
        data_prompt (str): The content of the data prompt file.
        post_prompt (str): The content of the post prompt file.
        reply_prompt (str): The content of the reply prompt file.

    Methods:
        __init__: Initializes the config by loading all prompt files into memory.
    """
    # Construct relevant paths (OS agnostic)
    THIS_DIR = os.path.dirname(os.path.abspath(__file__))
    PURPOSE_PROMPT_PATH = os.path.join(THIS_DIR, "prompts", "purpose_prompt.txt")
    DATA_PROMPT_PATH = os.path.join(THIS_DIR, "prompts", "data_prompt.txt")
    POST_PROMPT_PATH = os.path.join(THIS_DIR, "prompts", "post_prompt.txt")
    REPLY_PROMPT_PATH = os.path.join(THIS_DIR, "prompts", "reply_prompt.txt")

    def __init__(self):
        """Initializes the config class by loading all pompts from their respective files."""
        with open(self.PURPOSE_PROMPT_PATH, 'r') as f:
            self.purpose_prompt = f.read()

        with open(self.DATA_PROMPT_PATH, 'r') as f:
            self.data_prompt = f.read()

        with open(self.POST_PROMPT_PATH, 'r') as f:
            self.post_prompt = f.read()

        with open(self.REPLY_PROMPT_PATH, 'r') as f:
            self.reply_prompt = f.read()
       