import sys
import os

# Ensure src is in the PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.API import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
