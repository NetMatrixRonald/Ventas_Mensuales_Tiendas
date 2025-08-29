"""
API Simplificada para Pruebas
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import numpy as np
import joblib
import uvicorn

# Configurar FastAPI
app = FastAPI(
    title="API de Predicción de Ventas - Versión Simple",
    description="API simplificada para pruebas",
    version="1.0.0"
)

# Variables globales
model = None
scaler = None
label_encoders = None
feature_cols = None

class PredictionRequest(BaseModel):
    tienda_id: int
    empleados: float
    publicidad: float
    ubicacion: str

def load_model():
    """Cargar modelo y preprocesadores"""
    global model, scaler, label_encoders, feature_cols
    
    try:
        print("🔄 Cargando modelo...")
        
        # Cargar modelo
        model = joblib.load('models/model.pkl')
        print("✅ Modelo cargado")
        
        # Cargar preprocesadores
        scaler = joblib.load('models/scaler.pkl')
        label_encoders = joblib.load('models/label_encoders.pkl')
        print("✅ Preprocesadores cargados")
        
        # Cargar información del modelo
        model_info = joblib.load('models/model_info.pkl')
        feature_cols = model_info['processed_data_info']['feature_cols']
        print("✅ Información del modelo cargada")
        
        print("🎉 Todos los archivos cargados exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error al cargar el modelo: {e}")
        return False

@app.on_event("startup")
async def startup_event():
    """Evento de inicio de la aplicación"""
    print("🚀 Iniciando API de Predicción de Ventas...")
    load_model()

@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "message": "API de Predicción de Ventas - Versión Simple",
        "status": "running",
        "model_loaded": model is not None
    }

@app.get("/health")
async def health():
    """Endpoint de salud"""
    return {
        "status": "healthy" if model is not None else "unhealthy",
        "model_loaded": model is not None
    }

@app.post("/predict")
async def predict(request: PredictionRequest):
    """Realizar predicción"""
    if model is None:
        raise HTTPException(status_code=503, detail="Modelo no disponible")
    
    try:
        # Crear DataFrame
        data = {
            'tienda_id': request.tienda_id,
            'empleados': request.empleados,
            'publicidad': request.publicidad,
            'ubicacion': request.ubicacion
        }
        df = pd.DataFrame([data])
        
        # Codificar ubicación
        df['ubicacion'] = label_encoders['ubicacion'].transform(df['ubicacion'])
        
        # Reordenar columnas
        df = df[feature_cols]
        
        # Escalar características
        X = scaler.transform(df)
        
        # Realizar predicción
        prediction = model.predict(X)[0]
        
        return {
            "prediction": float(prediction),
            "input_data": data
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en la predicción: {str(e)}")

if __name__ == "__main__":
    print("🚀 Iniciando API simple...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
