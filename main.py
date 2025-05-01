import sys
import os
import uvicorn

# Añadir /crypto_app/src al PYTHONPATH dinámicamente
base_dir = os.path.dirname(__file__)
src_path = os.path.join(base_dir, 'crypto_app', 'src')
sys.path.insert(0, src_path)

from API import app  # API.py está en /crypto_app/src

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
