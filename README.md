<p align="center">
  <img src="banner.png"/>
</p>

<!-- Github Repo Info -->
<p align="center">
    <!-- Release -->
    <a href="https://github.com/sentient-agi/autonomous-agents/releases">
        <img alt="GitHub release" src="https://img.shields.io/badge/Release-v1.0-green">
    </a>
    <!-- License -->
    <a href="https://github.com/sentient-agi/autonomous-agents/tree/main?tab=Apache-2.0-1-ov-file">
        <img alt="License" src="https://img.shields.io/badge/License-Apache_2.0-red">
    </a>
</p>

<!-- Socials -->
<p align="center">
    <!-- Twitter -->
    <a href="https://twitter.com/SentientAGI">
        <img src="https://img.shields.io/twitter/follow/SentientAGI?style=social" alt="Twitter Follow"/>
    </a>
    <!-- Discord -->
    <a href="https://discord.com/invite/sentientfoundation">
        <img src="https://img.shields.io/discord/:1255126309416206408?style=social&label=Discord&logo=discord" alt="Discord">
    </a>
    <!-- Hugging face -->
    <a href="https://huggingface.co/SentientAGI">
        <img src="https://img.shields.io/badge/Hugging_Face-white?style=sociak&logo=huggingface" alt="Substack Follow"/>
    </a>
</p>

<h1 align="center">Autonomous Agents</h1>

This is a lightweight framework, with minimal dependencies, for building autonomous AI agents for social platforms. Aligned with Sentient's mission, this library is open to community contributions. Create an issue to ask a question or open a PR to add a feature!


## Agent Features&nbsp;&nbsp;🦾
For now the only platform that is supported is X (Twitter). We're going to continuously work on this framework. Discord and Telegram support are the next features in the pipeline. We also plan to add tools to support more sophisticated features, such as data sources and on-chain functionality.
- ✅ Supports any OpenAI API compatible LLM endpoint
- ✅ Supports X (Twitter)
- 🔄 Discord is coming soon...
- 🔄 Telegram is coming soon...
- 🔄 Web3 is coming soon...
- 🔄 Data is coming soon...


## [1/3]&nbsp;&nbsp;Setting Up Agent Credentials&nbsp;&nbsp;🔐

> [!WARNING]
> **We suggest creating a new X account for your agent.**

#### 1. Create secrets file

Create the `.env` file by copying the contents of `.env.example`. This is where you will store all of your agent's credentials.
```
cp .env.example .env
```

#### 2. Get model credentials
Add your Fireworks, or other inference provider, API key to the `.env` file.

#### 3. Get X (Twitter) credentials
In order to interact with the X (Twitter) API, your agent needs developer credentials from the X (Twitter) developer portal [here](https://developer.x.com/en/portal/dashboard).

From the *Dashboard* page, click on the gear icon to access the *Settings* page for your default project.

Set the user authentication settings for your app as follows:
- App permissions: "Read and write"
- Type of App: "Web App, Automated App or Bot"
- Callback URI / Redirect URL: http://localhost:8000
- Website URL: http://example.com

Generate all of the required credentials on the *Keys and tokens* page. Add them to the `.env` file.


## [2/3]&nbsp;&nbsp;Running Agent Locally&nbsp;&nbsp;💻
> [!NOTE]
> **These instructions are for unix-based systems (i.e. MacOS, Linux). Before you proceed, make sure that you have installed `python` and `pip`. If you have not, follow [these](https://packaging.python.org/en/latest/tutorials/installing-packages/) instructions to do so.**

#### 1. Create a Python virtual environment
```
python3 -m venv .venv
```

#### 2. Activate the Python virtual environment
```
source .venv/bin/activate
```

#### 3. Install dependencies
```
pip install -r requirements.txt
```

#### 4. Run your agent
```
python3 -m src.agent.agent
```


## [3/3]&nbsp;&nbsp;Configuring Agent&nbsp;&nbsp;⚙️
All of the tools available to your agent can be found in the `agent_tools` package. Each tool has its own package and in that package there is a configuration module. To configure a tool just change the constants in its configuration module.

#### Model Configuration
You can configure the model that your agent uses in the `model_config` in the `model` package in `agent_tools`.
- **OPTIONAL:** You can change the model that is used using the `BASE_URL` and `MODEL` constants. By default your agent will use Dobby 8b Unhinged, but the framework supports all OpenAI API compatible LLM endpoints.
- **OPTIONAL:** You can configure the model that is used using the `TEMPERATURE`, `MAX_TOKENS` and `SYSTEM_PROMPT` constants, however the default values are likely suitable for most agents.


#### X (Twitter) Configuration
You can configure how your agent behaves on X (Twitter) using the `twitter_config` module in the `twitter` package in `agent_tools`.
- 🚨 **REQUIRED:** You can configure the users with which your agent will interact using the `KEY_USERS` constant. By default your agent will respond to tweets from these key users.
- 🚨 **REQUIRED:** You can configure how may times your agent posts per run using the `RESPONSES_PER_RUN` constant.
- **OPTIONAL:** You can configure your agent to only respond to posts that contain a particular key word or phrase using the `KEY_PHRASE` constant.
- **OPTIONAL:** You can enable quote mode using the `QUOTE_MODE` constant. It is disabled by default. If quote mode is enabled your agent will quote tweet all of the key user's tweets that contain the key phrase. If quote mode is enabled your agent will ignore key users' quote tweets.


## Technical Information&nbsp;&nbsp;🛠️

#### Dobby Fireworks Endpoint
- If you have a fireworks account and API key you can find and use Sentient's models [here](https://fireworks.ai/models?provider=sentientagi).

#### X (Twitter) API
- It is important to consider X (Twitter) API [rate limits](https://docs.x.com/x-api/fundamentals/rate-limits#v2-limits). By default every time the agent runs, one call is made to the [*Recent Search*](https://docs.x.com/x-api/posts/recent-search) endpoint and one call is made to the [*Post a Tweet*](https://docs.x.com/x-api/posts/creation-of-a-post) endpoint per agent tweet.