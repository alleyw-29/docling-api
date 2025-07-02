FROM n8nio/n8n:latest

# Switch to root user to install packages
USER root

# Install the Tesseract.js community node globally
RUN npm install -g n8n-nodes-tesseractjs

# Revert back to the default 'node' user
USER node

