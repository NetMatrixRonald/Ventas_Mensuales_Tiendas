"""
Script para ejecutar el pipeline completo CRISP-DM
Predicción de Ventas Mensuales por Tienda
"""

import os
import sys
import subprocess
import time

def run_command(command, description):
    """Ejecutar comando y mostrar progreso"""
    print(f"\n{'='*60}")
    print(f"🚀 {description}")
    print(f"{'='*60}")
    print(f"Comando: {command}")
    print("-" * 60)
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print("✅ Comando ejecutado exitosamente")
        if result.stdout:
            print("Salida:")
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al ejecutar comando: {e}")
        if e.stdout:
            print("Salida estándar:")
            print(e.stdout)
        if e.stderr:
            print("Error:")
            print(e.stderr)
        return False

def main():
    """Ejecutar pipeline completo CRISP-DM"""
    print("🎯 PIPELINE COMPLETO CRISP-DM - PREDICCIÓN DE VENTAS")
    print("=" * 80)
    print("Este script ejecutará todas las fases del proyecto:")
    print("1. Comprensión del Negocio (Business Understanding)")
    print("2. Comprensión de los Datos (Data Understanding)")
    print("3. Preparación de los Datos (Data Preparation)")
    print("4. Modelado (Modeling)")
    print("5. Evaluación (Evaluation)")
    print("6. Despliegue (Deployment)")
    print("=" * 80)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists("data/ventas_tiendas (4).csv"):
        print("❌ Error: No se encontró el archivo de datos en data/ventas_tiendas (4).csv")
        print("Asegúrate de estar en el directorio raíz del proyecto")
        return False
    
    # Crear directorio models si no existe
    os.makedirs("models", exist_ok=True)
    
    # Fase 1: Comprensión del Negocio
    print("\n📋 FASE 1: COMPRENSIÓN DEL NEGOCIO")
    print("Objetivo: Predecir ventas mensuales por tienda")
    print("Algoritmo: Regresión Lineal")
    print("Criterios de éxito: R² > 0.7")
    
    # Fase 2-3: Comprensión y Preparación de Datos
    print("\n📊 FASE 2-3: COMPRENSIÓN Y PREPARACIÓN DE DATOS")
    success = run_command(
        "python src/data_preprocessing.py",
        "Ejecutando preprocesamiento de datos (Fases 2-3)"
    )
    
    if not success:
        print("❌ Error en el preprocesamiento de datos")
        return False
    
    # Fase 4-5: Modelado y Evaluación
    print("\n🤖 FASE 4-5: MODELADO Y EVALUACIÓN")
    success = run_command(
        "python src/model_training.py",
        "Entrenando y evaluando modelo (Fases 4-5)"
    )
    
    if not success:
        print("❌ Error en el entrenamiento del modelo")
        return False
    
    # Verificar que se crearon los archivos del modelo
    model_files = [
        "models/model.pkl",
        "models/scaler.pkl", 
        "models/label_encoders.pkl",
        "models/model_info.pkl"
    ]
    
    print("\n🔍 Verificando archivos del modelo...")
    for file_path in model_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - No encontrado")
            return False
    
    # Fase 6: Despliegue
    print("\n🌐 FASE 6: DESPLIEGUE")
    print("La API está lista para ser desplegada en Render")
    print("\nPara ejecutar localmente:")
    print("python main.py")
    print("\nPara desplegar en Render:")
    print("1. Subir el código a GitHub")
    print("2. Conectar el repositorio a Render")
    print("3. Configurar Build Command: pip install -r requirements.txt")
    print("4. Configurar Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT")
    
    # Mostrar información de la API
    print("\n📋 INFORMACIÓN DE LA API:")
    print("Endpoints disponibles:")
    print("- GET /: Información del modelo")
    print("- GET /health: Estado del servicio")
    print("- POST /predict: Predicción individual")
    print("- POST /predict_batch: Predicciones en lote")
    print("- GET /model-info: Información detallada del modelo")
    print("- GET /feature-importance: Importancia de características")
    print("- GET /example: Ejemplo de datos de entrada")
    print("- GET /docs: Documentación automática (Swagger)")
    print("- GET /redoc: Documentación alternativa (ReDoc)")
    
    print("\n🎉 ¡PIPELINE CRISP-DM COMPLETADO EXITOSAMENTE!")
    print("=" * 80)
    
    return True

if __name__ == "__main__":
    start_time = time.time()
    success = main()
    end_time = time.time()
    
    if success:
        print(f"\n⏱️ Tiempo total de ejecución: {end_time - start_time:.2f} segundos")
        print("✅ Proyecto listo para producción")
    else:
        print(f"\n⏱️ Tiempo de ejecución: {end_time - start_time:.2f} segundos")
        print("❌ El pipeline no se completó correctamente")
        sys.exit(1)
