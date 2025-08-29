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
        print("✅ Modelo cargado exitosamente")
        
        # Cargar preprocesadores
        scaler = joblib.load('models/scaler.pkl')
        print("✅ Scaler cargado exitosamente")
        
        label_encoders = joblib.load('models/label_encoders.pkl')
        print("✅ Label encoders cargados exitosamente")
        
        # Cargar información del modelo
        model_info = joblib.load('models/model_info.pkl')
        print("✅ Model info cargado exitosamente")
        
        # Verificar estructura de model_info
        if isinstance(model_info, dict):
            if 'processed_data_info' in model_info and 'feature_cols' in model_info['processed_data_info']:
                feature_cols = model_info['processed_data_info']['feature_cols']
                print(f"✅ Feature cols cargadas: {feature_cols}")
            else:
                # Valores por defecto si no están disponibles
                feature_cols = ['tienda_id', 'empleados', 'publicidad', 'ubicacion']
                print("⚠️ Usando feature cols por defecto")
        else:
            # Si model_info no es un diccionario, usar valores por defecto
            feature_cols = ['tienda_id', 'empleados', 'publicidad', 'ubicacion']
            print("⚠️ Model info no es un diccionario, usando valores por defecto")
        
        print("✅ Modelo y preprocesadores cargados exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error al cargar el modelo: {e}")
        # Inicializar con valores por defecto
        model = None
        scaler = None
        label_encoders = None
        model_info = None
        feature_cols = ['tienda_id', 'empleados', 'publicidad', 'ubicacion']
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
        confidence = 0.57  # Valor por defecto
        if model_info and 'metrics' in model_info and 'r2_test' in model_info['metrics']:
            confidence = model_info['metrics']['r2_test']
        
        # Preparar información del modelo con validaciones
        model_type = "LinearRegression"
        r2_score = 0.57
        rmse = 10739.31
        
        if model_info:
            if 'model_type' in model_info:
                model_type = model_info['model_type']
            if 'metrics' in model_info:
                if 'r2_test' in model_info['metrics']:
                    r2_score = model_info['metrics']['r2_test']
                if 'rmse_test' in model_info['metrics']:
                    rmse = model_info['metrics']['rmse_test']
        
        return PredictionResponse(
            prediction=float(prediction),
            confidence=float(confidence),
            model_info={
                "model_type": model_type,
                "r2_score": r2_score,
                "rmse": rmse
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
        
        # Preparar información del modelo con validaciones
        model_type = "LinearRegression"
        r2_score = 0.57
        rmse = 10739.31
        
        if model_info:
            if 'model_type' in model_info:
                model_type = model_info['model_type']
            if 'metrics' in model_info:
                if 'r2_test' in model_info['metrics']:
                    r2_score = model_info['metrics']['r2_test']
                if 'rmse_test' in model_info['metrics']:
                    rmse = model_info['metrics']['rmse_test']
        
        return BatchPredictionResponse(
            predictions=predictions,
            model_info={
                "model_type": model_type,
                "r2_score": r2_score,
                "rmse": rmse,
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
    
    # Preparar respuesta con validaciones
    response = {
        "model_type": "LinearRegression",
        "features": feature_cols or ['tienda_id', 'empleados', 'publicidad', 'ubicacion'],
        "metrics": {
            "r2_train": 0.5893,
            "r2_test": 0.5732,
            "mae_train": 8516.5747,
            "mae_test": 8532.4092,
            "rmse_train": 10721.5931,
            "rmse_test": 10739.3127
        },
        "training_info": {
            "cv_scores": [0.58555319, 0.5819458, 0.61389409, 0.56689647, 0.59305461],
            "cv_mean": 0.5883,
            "cv_std": 0.0308
        },
        "data_info": {
            "train_size": 8000,
            "test_size": 2000,
            "feature_cols": feature_cols or ['tienda_id', 'empleados', 'publicidad', 'ubicacion'],
            "target_col": "ventas"
        }
    }
    
    # Actualizar con datos reales si están disponibles
    if isinstance(model_info, dict):
        if 'model_type' in model_info:
            response["model_type"] = model_info['model_type']
        if 'metrics' in model_info:
            response["metrics"] = model_info['metrics']
        if 'training_info' in model_info:
            response["training_info"] = model_info['training_info']
        if 'processed_data_info' in model_info:
            response["data_info"] = model_info['processed_data_info']
    
    return response

@app.get("/feature-importance", response_model=Dict[str, Any])
async def get_feature_importance():
    """Obtener importancia de características"""
    # Valores por defecto
    default_importance = [
        {"feature": "empleados", "coefficient": 11583.705021},
        {"feature": "ubicacion", "coefficient": 5364.847664},
        {"feature": "publicidad", "coefficient": 1482.179605},
        {"feature": "tienda_id", "coefficient": 89.109364}
    ]
    
    model_type = "LinearRegression"
    
    # Actualizar con datos reales si están disponibles
    if model_info is not None and isinstance(model_info, dict):
        if 'model_type' in model_info:
            model_type = model_info['model_type']
        if 'feature_importance' in model_info:
            try:
                if hasattr(model_info['feature_importance'], 'to_dict'):
                    default_importance = model_info['feature_importance'].to_dict('records')
                elif isinstance(model_info['feature_importance'], list):
                    default_importance = model_info['feature_importance']
            except:
                pass  # Usar valores por defecto si hay error
    
    return {
        "feature_importance": default_importance,
        "model_type": model_type
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
