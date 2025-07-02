# Use a Python base image with Debian underneath
FROM python:3.10-slim

# Install Tesseract OCR and required system packages
RUN apt-get update && \
    apt-get install -y tesseract-ocr libtesseract-dev libleptonica-dev poppler-utils && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your app will run on
EXPOSE 8000

# Run FastAPI app using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
