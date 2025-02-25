import os
from dotenv import load_dotenv
from .model import Model

env_path = os.path.join(os.path.abspath(os.curdir), '.env')
load_dotenv(dotenv_path=env_path)

try:
    print("Connecting to model...")
    
    api_key=os.getenv("MODEL_API_KEY", None)
    if not api_key:
        raise Exception("Please add your fireworks api key to the .env file.")

    model = Model(
        api_key=os.getenv("MODEL_API_KEY", None)
    )
    print("To exit just type 'exit' and press enter.")
    while True:
        query = input("Query model: ")
        if query == "exit":
            print()
            print("Disconnecting from model...")
            break
        print(f"Response: {model.query(query)}")
except KeyboardInterrupt:
    print()
    print("Disconnecting from model...")