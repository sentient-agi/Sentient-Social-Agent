class TwitterConfig:
    def __init__(self):
        # Agent will respond to tweets from these users every time that it runs
        self.KEY_USERS = []

        # Agent will respond to tweets from key users containing this key 
        # phrase every time that it runs
        self.KEY_PHRASE = None

        # If true agent will quote tweet key user's tweets every time that it 
        # runs (instead of responding to tweets) (will ignore quote tweets)
        self.QUOTE_MODE = False
        
        # If true agent will post a tweet every time that it runs
        self.POST_MODE = False

        # Prompt that is provided to model to generate a post
        self.POST_PROMPT = "Generate a post for my twitter using less than 280 characters. Do not use hashtags."

        # Prompt that is provided to model, along with twitter conversation, to
        # generate a response
        self.RESPONSE_PROMPT = "Respond to this twitter conversation using less than 280 characters. Do not use hashtags."

        # Agent will post this number of respones per run
        self.RESPONSES_PER_RUN = 1
       
        # Agent will run this number of times per day
        self.RUNS_PER_DAY = 12