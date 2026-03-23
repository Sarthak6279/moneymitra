# This file is a wrapper for Streamlit Cloud deployment
# The actual app code is in app/main.py

import sys
from pathlib import Path

# Add the app directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "app"))

# Import and run the main app
from main import *
