import os
import logging
from dotenv import load_dotenv

# Import from SimplerLLM
from SimplerLLM.language.llm import LLM, LLMProvider

load_dotenv()
logger = logging.getLogger(__name__)

class GeminiRunner:
    """
    A class that interacts with an LLM using the SimplerLLM library.
    By default, this is configured for Google Gemini, but it can be adapted
    to any provider (OpenAI, Anthropic, etc.) using environment variables.
    """

    def __init__(self):
        """
        Initializes the GeminiRunner (or general LLM runner) with environment variables.
        Defaults to Gemini if no environment variables are set.
        """
        # You can store these in .env or supply them directly via environment
        provider_str = os.getenv("LLM_PROVIDER", "GEMINI").upper()
        model_name = os.getenv("LLM_MODEL_NAME", "gemini-pro")

        # Convert provider string to the LLMProvider Enum
        # e.g. "GEMINI" -> LLMProvider.GEMINI
        #      "OPENAI" -> LLMProvider.OPENAI
        #      "ANTHROPIC" -> LLMProvider.ANTHROPIC
        try:
            self.provider = LLMProvider[provider_str]
        except KeyError:
            logger.warning(
                f"Invalid LLM_PROVIDER '{provider_str}' in environment. "
                "Falling back to LLMProvider.GEMINI."
            )
            self.provider = LLMProvider.GEMINI

        logger.info(
            f"LLM Runner initialized with provider: {self.provider.name}, "
            f"model: {model_name}"
        )

        # Create the LLM instance
        self.llm_instance = LLM.create(provider=self.provider, model_name=model_name)

    def ask_gemini(self, query: str, context: str) -> str:
        """
        Generates a response from the LLM (Gemini by default) given a user query and context.
        
        :param query: The user’s question.
        :param context: The accumulated transcripts from uploaded files.
        :return: The LLM-generated answer as a string.
        """
        logger.info("Preparing prompt for LLM.")
        prompt = f"Context:\n{context}\n\nUser Question:\n{query}\n\nAnswer:"

        try:
            logger.debug(f"Sending prompt to LLM provider: {self.provider.name}")
            response = self.llm_instance.generate_response(prompt=prompt)
            logger.info("Successfully received response from LLM.")
            return response.strip()
        except Exception as e:
            logger.error("Error generating response with LLM: %s", e)
            return "Sorry, there was an error with the LLM. Please try again."
