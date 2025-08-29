"""
Script para ejecutar la API de predicción de ventas
"""

import uvicorn
import sys
import os

# Agregar el directorio api al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'api'))

if __name__ == "__main__":
    print("🚀 Iniciando API de Predicción de Ventas...")
    print("📊 Modelo: Regresión Lineal")
    print("🎯 Metodología: CRISP-DM")
    print("🌐 URL: http://localhost:8000")
    print("📚 Documentación: http://localhost:8000/docs")
    print("=" * 50)
    
    # Ejecutar la API
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
