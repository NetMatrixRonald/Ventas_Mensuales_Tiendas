"""
API REST para Predicción de Ventas - CRISP-DM
Fase 6: Despliegue en Render
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import pandas as pd
import numpy as np
import joblib
import os
from typing import List, Dict, Any, Optional
import uvicorn

# Configurar FastAPI
app = FastAPI(
    title="API de Predicción de Ventas Mensuales",
    description="API para predecir ventas mensuales por tienda usando Regresión Lineal siguiendo metodología CRISP-DM",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Variables globales para el modelo
model = None
scaler = None
label_encoders = None
model_info = None
feature_cols = None

# Esquemas Pydantic
class PredictionRequest(BaseModel):
    """Esquema para las solicitudes de predicción individual"""
    tienda_id: int = Field(..., description="ID de la tienda", ge=1, le=100)
    empleados: float = Field(..., description="Número de empleados", ge=1, le=50)
    publicidad: float = Field(..., description="Gasto en publicidad", ge=0, le=20000)
    ubicacion: str = Field(..., description="Tipo de ubicación", pattern="^(rural|suburbana|urbana)$")
    
    class Config:
        schema_extra = {
            "example": {
                "tienda_id": 1,
                "empleados": 20,
                "publicidad": 5000,
                "ubicacion": "urbana"
            }
        }

class BatchPredictionRequest(BaseModel):
    """Esquema para predicciones en lote"""
    data: List[Dict[str, Any]] = Field(..., description="Lista de datos para predicción")
    
    class Config:
        schema_extra = {
            "example": {
                "data": [
                    {
                        "tienda_id": 1,
                        "empleados": 20,
                        "publicidad": 5000,
                        "ubicacion": "urbana"
                    },
                    {
                        "tienda_id": 2,
                        "empleados": 15,
                        "publicidad": 3000,
                        "ubicacion": "rural"
                    }
                ]
            }
        }

class PredictionResponse(BaseModel):
    """Esquema para las respuestas de predicción"""
    prediction: float
    confidence: float
    model_info: Dict[str, Any]

class BatchPredictionResponse(BaseModel):
    """Esquema para respuestas de predicción en lote"""
    predictions: List[float]
    model_info: Dict[str, Any]

class HealthResponse(BaseModel):
    """Esquema para el endpoint de salud"""
    status: str
    model_loaded: bool
    model_type: str
    version: str

def load_model():
    """Cargar modelo y preprocesadores"""
    global model, scaler, label_encoders, model_info, feature_cols
    
    try:
        # Cargar modelo
        model = joblib.load('models/model.pkl')
        
        # Cargar preprocesadores
        scaler = joblib.load('models/scaler.pkl')
        label_encoders = joblib.load('models/label_encoders.pkl')
        
        # Cargar información del modelo
        model_info = joblib.load('models/model_info.pkl')
        feature_cols = model_info['processed_data_info']['feature_cols']
        
        print("✅ Modelo y preprocesadores cargados exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error al cargar el modelo: {e}")
        return False

def preprocess_input(data: Dict[str, Any]) -> np.ndarray:
    """Preprocesar datos de entrada"""
    # Crear DataFrame
    df = pd.DataFrame([data])
    
    # Codificar ubicación
    if 'ubicacion' in df.columns:
        df['ubicacion'] = label_encoders['ubicacion'].transform(df['ubicacion'])
    
    # Reordenar columnas según el orden del entrenamiento
    df = df[feature_cols]
    
    # Escalar características
    df_scaled = scaler.transform(df)
    
    return df_scaled

@app.on_event("startup")
async def startup_event():
    """Evento de inicio de la aplicación"""
    print("🚀 Iniciando API de Predicción de Ventas...")
    if not load_model():
        print("⚠️ No se pudo cargar el modelo. La API funcionará en modo limitado.")

@app.get("/", response_model=Dict[str, Any])
async def root():
    """Endpoint raíz con información del modelo"""
    return {
        "message": "API de Predicción de Ventas Mensuales por Tienda",
        "version": "1.0.0",
        "model_type": model_info['model_type'] if model_info else "No disponible",
        "features": len(feature_cols) if feature_cols else 0,
        "methodology": "CRISP-DM",
        "algorithm": "Regresión Lineal",
        "docs": "/docs",
        "health": "/health",
        "example": "/example"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Verificar el estado del servicio"""
    return HealthResponse(
        status="healthy" if model is not None else "unhealthy",
        model_loaded=model is not None,
        model_type=model_info['model_type'] if model_info else "No disponible",
        version="1.0.0"
    )

@app.post("/predict", response_model=PredictionResponse)
async def predict_ventas(request: PredictionRequest):
    """Realizar predicción de ventas individual"""
    if model is None:
        raise HTTPException(status_code=503, detail="Modelo no disponible")
    
    try:
        # Preprocesar datos
        data_dict = request.dict()
        X = preprocess_input(data_dict)
        
        # Realizar predicción
        prediction = model.predict(X)[0]
        
        # Calcular confianza (basada en R² del modelo)
        confidence = model_info['metrics']['r2_test'] if model_info else 0.57
        
        return PredictionResponse(
            prediction=float(prediction),
            confidence=float(confidence),
            model_info={
                "model_type": model_info['model_type'],
                "r2_score": model_info['metrics']['r2_test'],
                "rmse": model_info['metrics']['rmse_test']
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en la predicción: {str(e)}")

@app.post("/predict_batch", response_model=BatchPredictionResponse)
async def predict_ventas_batch(request: BatchPredictionRequest):
    """Realizar predicciones en lote"""
    if model is None:
        raise HTTPException(status_code=503, detail="Modelo no disponible")
    
    try:
        predictions = []
        
        for data in request.data:
            # Preprocesar datos
            X = preprocess_input(data)
            
            # Realizar predicción
            prediction = model.predict(X)[0]
            predictions.append(float(prediction))
        
        return BatchPredictionResponse(
            predictions=predictions,
            model_info={
                "model_type": model_info['model_type'],
                "r2_score": model_info['metrics']['r2_test'],
                "rmse": model_info['metrics']['rmse_test'],
                "batch_size": len(predictions)
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en la predicción en lote: {str(e)}")

@app.get("/model-info", response_model=Dict[str, Any])
async def get_model_info():
    """Obtener información detallada del modelo"""
    if model_info is None:
        raise HTTPException(status_code=503, detail="Información del modelo no disponible")
    
    return {
        "model_type": model_info['model_type'],
        "features": feature_cols,
        "metrics": model_info['metrics'],
        "training_info": model_info['training_info'],
        "data_info": model_info['processed_data_info']
    }

@app.get("/feature-importance", response_model=Dict[str, Any])
async def get_feature_importance():
    """Obtener importancia de características"""
    if model_info is None or 'feature_importance' not in model_info:
        raise HTTPException(status_code=503, detail="Información de importancia no disponible")
    
    return {
        "feature_importance": model_info['feature_importance'].to_dict('records'),
        "model_type": model_info['model_type']
    }

@app.get("/example", response_model=Dict[str, Any])
async def get_example():
    """Obtener ejemplo de datos de entrada"""
    return {
        "example_request": {
            "tienda_id": 1,
            "empleados": 20,
            "publicidad": 5000,
            "ubicacion": "urbana"
        },
        "example_response": {
            "prediction": 45000.0,
            "confidence": 0.57,
            "model_info": {
                "model_type": "LinearRegression",
                "r2_score": 0.57,
                "rmse": 10739.31
            }
        },
        "valid_locations": ["rural", "suburbana", "urbana"],
        "valid_ranges": {
            "tienda_id": [1, 100],
            "empleados": [1, 50],
            "publicidad": [0, 20000]
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
