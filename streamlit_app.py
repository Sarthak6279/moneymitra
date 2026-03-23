import runpy
import sys
from pathlib import Path

# Get the path to app/main.py
app_file = Path(__file__).parent / "app" / "main.py"

# Run the app
runpy.run_path(str(app_file), run_name="__main__")
