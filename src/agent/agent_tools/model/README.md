# Model Configuration
You can configure the model that powers your agent using the `model_config` module.
- You can change the model that is used using the `BASE_URL` and `MODEL` constants. By default your agent will use Dobby 8b Unhinged, but the framework supports all OpenAI API compatible LLM endpoints.
- You can configure the model that is used using the `TEMPERATURE`, `MAX_TOKENS` and `SYSTEM_PROMPT` constants, however the default values are likely suitable for most agents.