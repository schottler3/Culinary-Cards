import sys
from pathlib import Path

# Add the project root to Python's path
sys.path.append(str(Path(__file__).parent))

from CulinaryCards import app

if __name__ == "__main__":
    app.run(debug=True)