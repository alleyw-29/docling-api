# Use a lightweight Debian-based Python image
FROM python:3.10-slim

# Install system dependencies, including Tesseract
RUN apt-get update && \
    apt-get install -y tesseract-ocr libtesseract-dev libleptonica-dev poppler-utils && \
    apt-get clean

# Set the working directory
WORKDIR /app

# Copy your app code into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for FastAPI
EXPOSE 8000

# Run the FastAPI app using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
