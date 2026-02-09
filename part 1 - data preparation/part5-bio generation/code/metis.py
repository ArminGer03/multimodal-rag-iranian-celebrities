import requests
import time
from typing import Optional


class MetisAIChat:
    def __init__(self, api_key: str = "", bot_id: str = "", base_url: str = "https://api.metisai.ir/api/v1"):
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

    def get_response_with_retry(
            self,
            prompt: str,
            max_retries: int = 3,
            retry_delay: float = 1.0,
            initial_message: bool = True
    ) -> Optional[str]:
        """
        Send a prompt to the bot and get response with retry logic

        Args:
            prompt: The message to send to the bot
            max_retries: Maximum number of retry attempts
            retry_delay: Delay between retries in seconds
            initial_message: Whether this is the first message in a conversation

        Returns:
            The bot's response content or None if all retries fail
        """
        for attempt in range(max_retries + 1):
            try:
                # Create new session if needed or for initial message
                if self.session_id is None or initial_message:
                    self.session_id = self._create_session()

                url = f"{self.base_url}/chat/session/{self.session_id}/message"
                payload = {
                    "message": {
                        "content": prompt,
                        "type": "USER"
                    }
                }

                response = requests.post(url, headers=self.headers, json=payload)
                response.raise_for_status()
                return response.json()

            except requests.exceptions.RequestException as e:
                if attempt == max_retries:
                    print(f"Failed after {max_retries} retries. Last error: {str(e)}")
                    return None

                print(f"Attempt {attempt + 1} failed. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                # Exponential backoff (optional)
                retry_delay *= 2

        return None


# Example usage
if __name__ == "__main__":
    # Configuration

    # Initialize chat client
    chat = MetisAIChat()

    # Get response with retry logic
    prompt = "Hello, how are you?"
    response = chat.get_response_with_retry(prompt, initial_message=True)

    if response:
        print("Bot response:", response)
    else:
        print("Failed to get response from the bot")
