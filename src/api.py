"""
API REST para Predicción de Ventas - CRISP-DM
Fase 6: Despliegue
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import numpy as np
import joblib
import os
from typing import List, Dict, Any
import uvicorn

# Configurar FastAPI
app = FastAPI(
    title="API de Predicción de Ventas Mensuales",
    description="API para predecir ventas mensuales por tienda usando Regresión Lineal",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Modelo y preprocesadores
model = None
scaler = None
label_encoders = None
model_info = None
feature_cols = None

class PredictionRequest(BaseModel):
    """Esquema para las solicitudes de predicción"""
    # Los campos se definirán dinámicamente basándose en las características del modelo
    
class PredictionResponse(BaseModel):
    """Esquema para las respuestas de predicción"""
    prediction: float
    confidence: float
    model_info: Dict[str, Any]

class HealthResponse(BaseModel):
    """Esquema para el endpoint de salud"""
    status: str
    model_loaded: bool
    model_type: str

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
        "message": "API de Predicción de Ventas Mensuales",
        "version": "1.0.0",
        "model_type": model_info['model_type'] if model_info else "No disponible",
        "features": len(feature_cols) if feature_cols else 0,
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Verificar el estado del servicio"""
    return HealthResponse(
        status="healthy" if model is not None else "unhealthy",
        model_loaded=model is not None,
        model_type=model_info['model_type'] if model_info else "No disponible"
    )

@app.post("/predict", response_model=PredictionResponse)
async def predict_ventas(request: Dict[str, Any]):
    """Realizar predicción de ventas"""
    if model is None:
        raise HTTPException(status_code=503, detail="Modelo no disponible")
    
    try:
        # Convertir request a DataFrame
        input_data = pd.DataFrame([request])
        
        # Preprocesar datos
        processed_data = preprocess_input(input_data)
        
        # Realizar predicción
        prediction = model.predict(processed_data)[0]
        
        # Calcular confianza (basada en la varianza del modelo)
        confidence = 0.85  # Valor fijo por simplicidad
        
        return PredictionResponse(
            prediction=float(prediction),
            confidence=confidence,
            model_info={
                "model_type": model_info['model_type'],
                "features_used": len(feature_cols),
                "feature_names": list(feature_cols)
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en la predicción: {str(e)}")

@app.post("/predict_batch", response_model=List[PredictionResponse])
async def predict_ventas_batch(requests: List[Dict[str, Any]]):
    """Realizar predicciones en lote"""
    if model is None:
        raise HTTPException(status_code=503, detail="Modelo no disponible")
    
    try:
        results = []
        
        for request in requests:
            # Convertir request a DataFrame
            input_data = pd.DataFrame([request])
            
            # Preprocesar datos
            processed_data = preprocess_input(input_data)
            
            # Realizar predicción
            prediction = model.predict(processed_data)[0]
            
            # Calcular confianza
            confidence = 0.85
            
            results.append(PredictionResponse(
                prediction=float(prediction),
                confidence=confidence,
                model_info={
                    "model_type": model_info['model_type'],
                    "features_used": len(feature_cols),
                    "feature_names": list(feature_cols)
                }
            ))
        
        return results
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en las predicciones: {str(e)}")

@app.get("/model-info", response_model=Dict[str, Any])
async def get_model_info():
    """Obtener información detallada del modelo"""
    if model_info is None:
        raise HTTPException(status_code=503, detail="Información del modelo no disponible")
    
    return {
        "model_type": model_info['model_type'],
        "features": list(feature_cols) if feature_cols else [],
        "feature_importance": model_info['feature_importance'].to_dict('records') if 'feature_importance' in model_info else [],
        "target_variable": model_info['processed_data_info']['target_col'],
        "model_loaded": model is not None
    }

@app.get("/feature-importance", response_model=Dict[str, Any])
async def get_feature_importance():
    """Obtener importancia de características"""
    if model_info is None or 'feature_importance' not in model_info:
        raise HTTPException(status_code=503, detail="Información de importancia no disponible")
    
    importance_df = model_info['feature_importance']
    
    return {
        "feature_importance": importance_df.to_dict('records'),
        "top_features": importance_df.head(10).to_dict('records'),
        "total_features": len(importance_df)
    }

def preprocess_input(input_data: pd.DataFrame) -> np.ndarray:
    """Preprocesar datos de entrada"""
    try:
        # Asegurar que todas las columnas necesarias estén presentes
        missing_cols = set(feature_cols) - set(input_data.columns)
        if missing_cols:
            # Rellenar columnas faltantes con valores por defecto
            for col in missing_cols:
                input_data[col] = 0
        
        # Reordenar columnas según el orden del entrenamiento
        input_data = input_data[feature_cols]
        
        # Aplicar codificación de variables categóricas
        for col, encoder in label_encoders.items():
            if col in input_data.columns:
                # Manejar valores no vistos durante el entrenamiento
                unique_values = encoder.classes_
                input_data[col] = input_data[col].apply(
                    lambda x: x if x in unique_values else unique_values[0]
                )
                input_data[col] = encoder.transform(input_data[col])
        
        # Aplicar escalado
        scaled_data = scaler.transform(input_data)
        
        return scaled_data
        
    except Exception as e:
        raise ValueError(f"Error en el preprocesamiento: {str(e)}")

# Ejemplo de uso
@app.get("/example", response_model=Dict[str, Any])
async def get_example():
    """Obtener ejemplo de datos de entrada"""
    if feature_cols is None:
        raise HTTPException(status_code=503, detail="Información del modelo no disponible")
    
    # Crear ejemplo con valores por defecto
    example_data = {}
    for col in feature_cols:
        if col in label_encoders:
            # Para variables categóricas, usar el primer valor
            example_data[col] = label_encoders[col].classes_[0]
        else:
            # Para variables numéricas, usar 0
            example_data[col] = 0
    
    return {
        "example_input": example_data,
        "description": "Ejemplo de datos de entrada para predicción",
        "note": "Ajusta los valores según tus datos reales"
    }

if __name__ == "__main__":
    # Ejecutar la aplicación
    uvicorn.run(app, host="0.0.0.0", port=8000)
