"""
Archivo principal para Render
Importa y ejecuta la API desde el directorio api/
"""

import sys
import os

# Agregar el directorio api al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'api'))

# Importar la aplicación FastAPI
from api.main import app

if __name__ == "__main__":
    import uvicorn
    # Ejecutar la API
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000)),
        reload=False
    )
