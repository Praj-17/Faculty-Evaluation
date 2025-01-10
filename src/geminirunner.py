import os
import logging
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

logger = logging.getLogger(__name__)

class GeminiRunner:
    """
    A class that interacts with the Gemini model for text-based question-answering.
    """

    def __init__(self):
        """
        Initializes the GeminiRunner with environment variables.
        """
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.api_url = os.getenv("GEMINI_API_URL")

        if not self.api_key or not self.api_url:
            logger.warning("Gemini model configuration is missing or incomplete.")

    def ask_gemini(self, query: str, context: str) -> str:
        """
        Sends a query to the Gemini model API with the provided context and returns the answer.
        
        :param query: The user question.
        :param context: The text context from the uploaded transcripts.
        :return: The answer from the Gemini model.
        """
        logger.info("Preparing request to Gemini model.")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        payload = {
            "prompt": f"Context: {context}\nQuestion: {query}\nAnswer:",
            "max_tokens": 1000,
            # Additional parameters depending on the Gemini model's API
        }

        try:
            logger.debug(f"Sending request to Gemini at {self.api_url} with query: {query}")
            response = requests.post(self.api_url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            answer_json = response.json()
            # Adjust this according to the actual Gemini API's response structure
            answer = answer_json.get("answer", "").strip()
            logger.info("Received valid response from Gemini.")
            return answer
        except requests.exceptions.RequestException as e:
            logger.error("Error communicating with Gemini API: %s", e)
            return "Sorry, there was an error contacting the Gemini model. Please try again."
