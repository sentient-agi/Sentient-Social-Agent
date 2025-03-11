import time
import logging
from tweepy.errors import TooManyRequests, TwitterServerError

def with_rate_limit_handling(func):
    """Decorator to handle Twitter API rate limits with exponential backoff"""
    def wrapper(*args, **kwargs):
        max_retries = 5
        retry_count = 0
        base_wait_time = 60  # seconds
        
        while True:
            try:
                return func(*args, **kwargs)
            except TooManyRequests as e:
                retry_count += 1
                if retry_count > max_retries:
                    logging.error(f"[TWITTER] Maximum retries exceeded. Giving up after {max_retries} attempts.")
                    raise e
                
                # Calculate wait time with exponential backoff
                wait_time = base_wait_time * (2 ** (retry_count - 1))
                logging.warning(f"[TWITTER] Rate limit reached. Waiting {wait_time} seconds before retry {retry_count}/{max_retries}.")
                time.sleep(wait_time)
            except TwitterServerError as e:
                retry_count += 1
                if retry_count > max_retries:
                    logging.error(f"[TWITTER] Maximum retries exceeded. Giving up after {max_retries} attempts.")
                    raise e
                
                wait_time = base_wait_time
                logging.warning(f"[TWITTER] Twitter server error. Waiting {wait_time} seconds before retry {retry_count}/{max_retries}.")
                time.sleep(wait_time)
    return wrapper