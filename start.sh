#!/bin/bash

# Ensure the script is executable
chmod +x start.sh

# Set Streamlit to run on all interfaces and not open a browser
# The --server.port is set to 8501 to match the EXPOSE instruction in the Dockerfile
streamlit run app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true
