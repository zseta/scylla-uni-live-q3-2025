#!/bin/bash

# Activate virtual environment
source env/bin/activate

# Run both commands
(python server.py & streamlit run app.py & wait)