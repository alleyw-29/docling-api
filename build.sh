#!/usr/bin/env bash
apt-get update
apt-get install -y tesseract-ocr

# Then install your Python deps
pip install -r requirements.txt
