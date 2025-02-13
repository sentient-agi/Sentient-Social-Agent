class TwitterConfig:
    def __init__(self):
        # Agent will respond to tweets from these users
        self.KEY_USERS=[]

        # Agent will respond to tweets containing this keyword
        self.KEY_PHRASE=None

        # If true agent will quote tweet key user's tweets (instead of 
        # responding to tweets) and will ignore quote tweets
        self.QUOTE_MODE=False
        
        # Prompt that is provided to model, along with twitter conversation, to
        # generate a response
        self.RESPONSE_PROMPT="Respond to this twitter conversation using less than 280 characters. Do not use hashtags."

        # Agent will post this number of respones per run
        self.RESPONSES_PER_RUN=10
       
        # Agent will run this number of times per day
        self.RUNS_PER_DAY = 12