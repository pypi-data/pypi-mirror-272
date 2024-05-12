from alpaca.trading.client import TradingClient
import os
from dotenv import load_dotenv


# For lazy instantiation
class TradingClientSingleton:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            load_dotenv()  # You can set a path to the .env file
            api_key_id = os.getenv('API_KEY_ID')
            secret_key = os.getenv('SECRET_KEY')
            cls._instance = TradingClient(api_key_id, secret_key, paper=True)
        return cls._instance
