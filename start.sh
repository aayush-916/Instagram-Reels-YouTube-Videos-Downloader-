#!/bin/bash

# Install the required Python packages
pip install -r requirements.txt

# Install Playwright browsers
python -m playwright install

# Start the Flask app
python app.py
