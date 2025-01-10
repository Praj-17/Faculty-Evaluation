# Use the official Python image as a base
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements first for efficient caching
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . /app/

# Expose Streamlit's default port
EXPOSE 8501

# Set environment variables (optional, or you can rely on .env)
# ENV GEMINI_API_KEY=your_key
# ENV GEMINI_API_URL=your_gemini_url

# Run Streamlit
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
