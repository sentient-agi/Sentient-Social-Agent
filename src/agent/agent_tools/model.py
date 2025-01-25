import json
import logging
import openai
from datetime import datetime
from langchain_core.prompts import PromptTemplate


class Model:
    """
    A class for interfacing with a model using the OpenAI API.

    Attributes:
        model (str): The name of the model to use.
        api_key (str): API key used for authentication.
        temperature (float): Temperature setting for response randomness 
            (default 0.0).
        max_tokens (int or None): Maximum number of tokens for the response
            (default None).
        system_prompt (str): A predefined system message or prompt to guide
            model behavior (default is "default").
        date_context (str): A string representing the current date, used in the
            system prompt.
        client (openai.OpenAI): An instance of the OpenAI client configured
            with the provided API key and base URL.

    Methods:
        query(query, contexts): Queries the model and returns the full response
            as a string.
    """


    def __init__(
            self,
            api_key,
            url,
            model,
            temperature=0.0,
            max_tokens=None,
            system_prompt="default"):
        """
        Initializes the Model class with the necessary parameters.

        Args:
            api_key (str): API key for authenticating with the OpenAI service.
            url (str): URL for the OpenAI API.
            model (str): The model name.
            temperature (float, optional): Temperature setting for response 
                randomness (default 0.0).
            max_tokens (int, optional): Maximum number of tokens for the 
                response (default None).
            system_prompt (str, optional): A custom system prompt for guiding 
                model behavior (default "default").

        Initializes the model, sets up the OpenAI client, and configures the 
        system prompt.
        """
        # Assign values to object properties
        self.model = model
        self.api_key = api_key
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.date_context = datetime.now().strftime("%Y-%m-%d")

        # Set up model API
        self.client = openai.OpenAI(
            base_url=url,
            api_key=self.api_key,
        )

        # Set up system prompt
        if system_prompt == "default":
            system_prompt_search = PromptTemplate(
                input_variables=["date_today"],
                template="You are a helpful assistant that can answer questions and provide information."
                )
            self.system_prompt = system_prompt_search.format(date_today=self.date_context)
        else:
            self.system_prompt = system_prompt


    def __query_async(self, query):
        """Sends query to model and yields the response in chunks."""
        if self.model in ["o1-preview", "o1-mini"]:
            messages = [
                {"role": "user",
                 "content": f"System Instruction: {self.system_prompt} \n Instruction:{query}"}
            ]
        else:
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": query}
            ]

        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=True,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )

            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content

        except Exception as e:
            logging.warning(f"Error during get_answer_fireworks call: {e}")
            yield "data:" + json.dumps(
                {"type": "error",
                 "data": "We are currently experiencing some issues. Please try again later."}) + "\n\n"


    def query(self, query):
        """
        Sends query to model and returns the complete response as a string.

        This method calls the `__query_async` method, concatenates all of the 
        chunks that it yields, and returns the full response as a string.
        """
        chunks = []
        for chunk in self.__query_async(query=query):
            chunks.append(chunk)
        response = "".join(chunks)
        return response