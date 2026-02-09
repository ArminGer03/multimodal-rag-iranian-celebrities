import requests
import time
import json
from typing import Optional, List, Dict


class MetisAIChat:
    def __init__(self, api_key: str = "tpsg-e9jwaBWRJr5BZKZY2dCpOo9pO8Q4aZ5",
                 bot_id: str = "9ca06edb-72ba-4e7b-9e51-6e41276a2c4c", base_url: str = "https://api.metisai.ir/api/v1"):
        self.api_key = api_key
        self.bot_id = bot_id
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.session_id = None

    def _create_session(self) -> str:
        """Create a new chat session"""
        url = f"{self.base_url}/chat/session"
        payload = {"botId": self.bot_id}
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()["id"]

    def get_face_description(
            self,
            image_urls: List[str],
            max_retries: int = 3,
            retry_delay: float = 1.0
    ) -> Optional[str]:
        """
        Get face description in Persian for a given image URL

        Args:
            image_url: URL of the image to analyze
            max_retries: Maximum number of retry attempts
            retry_delay: Delay between retries in seconds

        Returns:
            The bot's response content or None if all retries fail
        """
        # Persian prompt with clear instructions
        prompt = """
        Please analyze this facial image and provide a description in Persian following these rules:
        1. The description must be concise and a maximum of two sentences.
        2. Mention the main facial features such as face shape, nose, eyes, eyebrows, hair, mustache, beard and skin.
        3. If an approximate age is detectable, mention it.
        4. If the image is unclear or of low quality and the face cannot be recognized, just say "UNCLEAR" (without quotes).

        Example of valid description: 
        "مردی با صورت بیضی شکل، بینی مستقیم، چشمان قهوه‌ای متوسط، ابروهای پرپشت، موهای مشکی و ریش کوتاه. به نظر می‌رسد در دهه سوم زندگی باشد."

        Example of unclear image response:
        "UNCLEAR"
        """

        for attempt in range(max_retries + 1):
            try:
                # Create new session for each image
                self.session_id = self._create_session()

                url = f"{self.base_url}/chat/session/{self.session_id}/message"
                payload = {
                    "message": {
                        "content": prompt,
                        "type": "USER",
                        "attachments": [
                            {
                                "content": image_url,
                                "contentType": "IMAGE"
                            } for image_url in image_urls
                        ]
                    }
                }

                response = requests.post(url, headers=self.headers, json=payload)
                response.raise_for_status()

                # Extract the response content
                response_data = response.json()
                # The exact structure might need adjustment based on API response format
                if 'content' in response_data:
                    return response_data['content']
                else:
                    print(f"Unexpected response format: {response_data}")
                    return None

            except requests.exceptions.RequestException as e:
                if attempt == max_retries:
                    print(f"Failed after {max_retries} retries. Last error: {str(e)}")
                    return None

                print(f"Attempt {attempt + 1} failed. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                # Exponential backoff
                retry_delay *= 2

        return None
