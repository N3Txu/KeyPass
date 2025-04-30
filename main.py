import sys
import os
import uvicorn

# Añadir el path del proyecto al PYTHONPATH
base_dir = os.path.dirname(__file__)
project_path = base_dir  # Añadir directorio raíz al PYTHONPATH
sys.path.insert(0, project_path)

from crypto_app.src.API import app  # Ahora esto funcionará correctamente

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
