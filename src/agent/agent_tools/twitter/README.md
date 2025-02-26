# X (Twitter) Configuration
You can configure how your agent behaves on X (Twitter) using the `twitter_config` module.
- You must configure the users with which your agent will interact using the `KEY_USERS` constant. By default your agent will respond to tweets from these key users.
- You must configure how may times your agent posts per run using the `RESPONSES_PER_RUN` constant.
- You can configure your agent to only respond to posts that contain a particular key word or phrase using the `KEY_PHRASE` constant.
- You can enable quote mode using the `QUOTE_MODE` constant. It is disabled by default. If quote mode is enabled your agent will quote tweet all of the key user's tweets that contain the key phrase. If quote mode is enabled your agent will ignore key users' quote tweets.
- You can enable post mode using the `POST_MODE` constant. It is disabled by default. If post mode is enabled your agent will post a tweet every time it runs.
- You can configure the prompt that is provided to the model to generate a post using the `POST_PROMPT` constant.
- You can configure the prompt that is provided to the model to generate a response using the `RESPONSE_PROMPT` constant.