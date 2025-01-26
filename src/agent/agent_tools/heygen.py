import requests
import json
import logging

logger = logging.getLogger(__name__)

class Heygen:
    """
    A class for interacting with the HeyGen API to generate avatar videos.

    Attributes:
        api_key (str): The API key for authenticating with the HeyGen service.
        api_url (str): The base URL for the HeyGen API.

    Methods:
        generate_video(text): Generates a video with the given text using the HeyGen API.
    """

    def __init__(self, api_key):
        """
        Initializes the Heygen class with the necessary parameters.

        Args:
            api_key (str): API key for authenticating with the HeyGen service.
        """
        self.api_key = api_key
        self.api_url = "https://api.heygen.com/v2/video/generate"

    def generate_video(self, text):
        """
        Generates a video with the given text using the HeyGen API.

        Args:
            text (str): The text to be spoken in the video.

        Returns:
            str: The URL of the generated video, or None if an error occurred.
        """
        headers = {
            'X-Api-Key': self.api_key,
            'Content-Type': 'application/json'
        }
        payload = {
            "video_inputs": [
                {
                    "character": {
                        "type": "avatar",
                        "avatar_id": "6cddbc1309404805bf4f7bea6c0457d3",
                        "avatar_style": "normal"
                    },
                    "voice": {
                        "type": "text",
                        "input_text": text,
                        "voice_id": "MjgyM2Y2NDdkMWY5NDVjODgwNzZkMTZiNTkwZDBkNTYtMTcyNzQxNDAwNg==",
                        "speed": 1.1
                    }
                }
            ],
            "dimension": {
                "width": 1080,
                "height": 1920
            }
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=payload)
            response.raise_for_status()  # Raise an exception for bad status codes
            video_url = response.json().get("data", {}).get("video_url")
            if video_url:
                logger.info(f"Generated video URL: {video_url}")
                return video_url
            else:
                logger.error("Video URL not found in the response.")
                return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Error generating video: {e}")
            return None
