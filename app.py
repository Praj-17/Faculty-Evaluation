import os
import streamlit as st
import logging
from logging.handlers import RotatingFileHandler

from src.geminirunner import GeminiRunner

# Configure logging
LOG_FILE_PATH = "logs/app.log"
os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[
        RotatingFileHandler(LOG_FILE_PATH, maxBytes=1_000_000, backupCount=3),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize GeminiRunner
gemini = GeminiRunner()

def main():
    """
    Main function to render the Streamlit dashboard.
    """
    st.title("University Class Evaluation Dashboard")
    st.write("Upload your Zoom class transcripts and ask questions about them.")

    # Sidebar for instructions or extra controls
    st.sidebar.title("Controls")

    # Step 1: File Upload
    transcripts = st.file_uploader(
        label="Upload multiple text files",
        accept_multiple_files=True,
        type=["txt"]
    )

    # Load all transcripts into a single string context
    context = ""
    if transcripts:
        for transcript_file in transcripts:
            try:
                file_content = transcript_file.read().decode("utf-8")
                context += file_content + "\n"
            except Exception as e:
                logger.error(f"Failed to read file: {transcript_file.name}. Error: {str(e)}")
                st.error(f"Failed to read file {transcript_file.name}")

    # Step 2: User Question
    user_query = st.text_input("Ask a question about the classes/transcripts:")

    # Step 3: Get Answer
    if st.button("Get Answer"):
        if not context.strip():
            st.error("Please upload transcript files first.")
        elif not user_query.strip():
            st.error("Please enter a question.")
        else:
            logger.info(f"User asked: {user_query}")
            with st.spinner("Contacting Gemini model..."):
                answer = gemini.ask_gemini(query=user_query, context=context)
            st.write("**Answer:**", answer)
            logger.info("Answer displayed to user.")

if __name__ == "__main__":
    main()
