#!/usr/bin/env python3
"""
Script de diagnóstico para verificar el estado de los archivos del modelo
"""

import os
import joblib
import pandas as pd
import numpy as np

def check_model_files():
    """Verificar el estado de los archivos del modelo"""
    print("🔍 Diagnóstico de archivos del modelo")
    print("=" * 50)
    
    # Verificar si existe el directorio models
    if not os.path.exists('models'):
        print("❌ Directorio 'models' no encontrado")
        return False
    
    print("✅ Directorio 'models' encontrado")
    
    # Listar archivos en el directorio models
    files = os.listdir('models')
    print(f"📁 Archivos en models/: {files}")
    
    # Verificar archivos específicos
    required_files = ['model.pkl', 'scaler.pkl', 'label_encoders.pkl', 'model_info.pkl']
    
    for file in required_files:
        file_path = os.path.join('models', file)
        if os.path.exists(file_path):
            print(f"✅ {file} encontrado")
            # Verificar tamaño del archivo
            size = os.path.getsize(file_path)
            print(f"   📏 Tamaño: {size:,} bytes")
        else:
            print(f"❌ {file} NO encontrado")
    
    return True

def test_model_loading():
    """Probar la carga de los archivos del modelo"""
    print("\n🧪 Probando carga de archivos")
    print("=" * 50)
    
    try:
        # Cargar modelo
        print("📦 Cargando modelo...")
        model = joblib.load('models/model.pkl')
        print(f"✅ Modelo cargado: {type(model)}")
        
        # Cargar scaler
        print("📦 Cargando scaler...")
        scaler = joblib.load('models/scaler.pkl')
        print(f"✅ Scaler cargado: {type(scaler)}")
        
        # Cargar label encoders
        print("📦 Cargando label encoders...")
        label_encoders = joblib.load('models/label_encoders.pkl')
        print(f"✅ Label encoders cargado: {type(label_encoders)}")
        
        # Cargar model info
        print("📦 Cargando model info...")
        model_info = joblib.load('models/model_info.pkl')
        print(f"✅ Model info cargado: {type(model_info)}")
        
        # Analizar estructura de model_info
        print("\n📊 Análisis de model_info:")
        if isinstance(model_info, dict):
            print("✅ model_info es un diccionario")
            print(f"   🔑 Claves disponibles: {list(model_info.keys())}")
            
            if 'processed_data_info' in model_info:
                print("✅ 'processed_data_info' encontrado")
                if 'feature_cols' in model_info['processed_data_info']:
                    print(f"✅ 'feature_cols' encontrado: {model_info['processed_data_info']['feature_cols']}")
                else:
                    print("❌ 'feature_cols' NO encontrado en processed_data_info")
            else:
                print("❌ 'processed_data_info' NO encontrado")
            
            if 'metrics' in model_info:
                print("✅ 'metrics' encontrado")
                print(f"   🔑 Claves en metrics: {list(model_info['metrics'].keys())}")
            else:
                print("❌ 'metrics' NO encontrado")
                
        else:
            print(f"❌ model_info NO es un diccionario, es: {type(model_info)}")
            print(f"   📄 Contenido: {model_info}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al cargar archivos: {e}")
        return False

def test_prediction():
    """Probar una predicción simple"""
    print("\n🎯 Probando predicción")
    print("=" * 50)
    
    try:
        # Cargar componentes
        model = joblib.load('models/model.pkl')
        scaler = joblib.load('models/scaler.pkl')
        label_encoders = joblib.load('models/label_encoders.pkl')
        model_info = joblib.load('models/model_info.pkl')
        
        # Datos de prueba
        test_data = {
            'tienda_id': 1,
            'empleados': 20,
            'publicidad': 5000,
            'ubicacion': 'urbana'
        }
        
        print(f"📝 Datos de prueba: {test_data}")
        
        # Crear DataFrame
        df = pd.DataFrame([test_data])
        print(f"📊 DataFrame creado: {df.shape}")
        
        # Codificar ubicación
        if 'ubicacion' in df.columns:
            df['ubicacion'] = label_encoders['ubicacion'].transform(df['ubicacion'])
            print("✅ Ubicación codificada")
        
        # Obtener feature cols
        if isinstance(model_info, dict) and 'processed_data_info' in model_info:
            feature_cols = model_info['processed_data_info']['feature_cols']
        else:
            feature_cols = ['tienda_id', 'empleados', 'publicidad', 'ubicacion']
        
        print(f"🔧 Feature cols: {feature_cols}")
        
        # Reordenar columnas
        df = df[feature_cols]
        print(f"📊 DataFrame reordenado: {df.shape}")
        
        # Escalar características
        df_scaled = scaler.transform(df)
        print(f"📊 Datos escalados: {df_scaled.shape}")
        
        # Realizar predicción
        prediction = model.predict(df_scaled)[0]
        print(f"🎯 Predicción: {prediction}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en predicción: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Iniciando diagnóstico del modelo")
    print("=" * 60)
    
    # Verificar archivos
    files_ok = check_model_files()
    
    if files_ok:
        # Probar carga
        loading_ok = test_model_loading()
        
        if loading_ok:
            # Probar predicción
            prediction_ok = test_prediction()
            
            if prediction_ok:
                print("\n🎉 ¡Todo funciona correctamente!")
            else:
                print("\n⚠️ Hay problemas con la predicción")
        else:
            print("\n⚠️ Hay problemas con la carga de archivos")
    else:
        print("\n⚠️ Hay problemas con los archivos del modelo")
    
    print("\n" + "=" * 60)
    print("🏁 Diagnóstico completado")
