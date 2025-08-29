"""
Script para verificar que los archivos del modelo se pueden cargar correctamente
"""

import joblib
import os

def verify_model_files():
    """Verificar que todos los archivos del modelo existen y se pueden cargar"""
    print("🔍 Verificando archivos del modelo...")
    
    model_files = [
        'models/model.pkl',
        'models/scaler.pkl',
        'models/label_encoders.pkl',
        'models/model_info.pkl'
    ]
    
    for file_path in model_files:
        print(f"\n📁 Verificando: {file_path}")
        
        # Verificar si el archivo existe
        if not os.path.exists(file_path):
            print(f"❌ Archivo no encontrado: {file_path}")
            continue
        
        # Verificar tamaño del archivo
        file_size = os.path.getsize(file_path)
        print(f"✅ Archivo existe - Tamaño: {file_size} bytes")
        
        # Intentar cargar el archivo
        try:
            loaded_data = joblib.load(file_path)
            print(f"✅ Archivo cargado exitosamente")
            
            # Mostrar información adicional según el tipo de archivo
            if 'model.pkl' in file_path:
                print(f"   Tipo: {type(loaded_data)}")
                if hasattr(loaded_data, 'coef_'):
                    print(f"   Coeficientes: {len(loaded_data.coef_)}")
            
            elif 'model_info.pkl' in file_path:
                print(f"   Claves: {list(loaded_data.keys())}")
                
        except Exception as e:
            print(f"❌ Error al cargar: {e}")
    
    print("\n" + "="*50)
    print("🎯 Verificación completada")

if __name__ == "__main__":
    verify_model_files()
