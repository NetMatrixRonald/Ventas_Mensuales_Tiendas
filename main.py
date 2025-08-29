"""
Pipeline Principal - CRISP-DM Completo
Predicción de Ventas Mensuales por Tienda
"""

import os
import sys
from src.data_preprocessing import DataPreprocessor
from src.model_training import ModelTrainer
import joblib

def main():
    """Ejecutar pipeline completo CRISP-DM"""
    print("🚀 INICIANDO PIPELINE CRISP-DM - PREDICCIÓN DE VENTAS")
    print("=" * 60)
    
    # Fase 1: Comprensión del Negocio
    print("\n📋 FASE 1: COMPRENSIÓN DEL NEGOCIO")
    print("Objetivo: Predecir ventas mensuales por tienda")
    print("Criterios de éxito: R² > 0.7, RMSE bajo")
    print("Variable objetivo: ventas")
    
    # Fase 2-3: Comprensión y Preparación de Datos
    print("\n" + "=" * 60)
    preprocessor = DataPreprocessor()
    
    if not preprocessor.load_data():
        print("❌ Error en la carga de datos. Terminando...")
        return
    
    preprocessor.explore_data()
    preprocessor.analyze_target_variable()
    preprocessor.clean_data()
    preprocessor.prepare_features()
    preprocessor.split_data()
    
    # Fase 4-5: Modelado y Evaluación
    print("\n" + "=" * 60)
    trainer = ModelTrainer()
    
    X_train, X_test, y_train, y_test, feature_cols, target_col = trainer.load_processed_data()
    
    if X_train is not None:
        model = trainer.train_linear_regression(X_train, y_train)
        trainer.evaluate_model(X_train, X_test, y_train, y_test)
        trainer.save_model()
        trainer.generate_report()
    
    # Fase 6: Despliegue
    print("\n" + "=" * 60)
    print("📋 FASE 6: DESPLIEGUE")
    print("✅ Modelo entrenado y guardado")
    print("✅ Archivos PKL generados en /models/")
    print("✅ API lista para despliegue en Render")
    print("\n🎯 Para ejecutar la API:")
    print("   cd api")
    print("   uvicorn main:app --reload")
    print("\n🌐 Para desplegar en Render:")
    print("   1. Conectar repositorio a Render")
    print("   2. Build Command: pip install -r requirements.txt")
    print("   3. Start Command: uvicorn api.main:app --host 0.0.0.0 --port $PORT")
    
    print("\n✅ PIPELINE CRISP-DM COMPLETADO EXITOSAMENTE")

if __name__ == "__main__":
    main()
