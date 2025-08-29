"""
Script para probar la API de predicción de ventas
"""

import requests
import json
import time

# URL base de la API
BASE_URL = "http://localhost:8000"

def test_health():
    """Probar endpoint de salud"""
    print("🏥 Probando endpoint de salud...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_root():
    """Probar endpoint raíz"""
    print("\n🏠 Probando endpoint raíz...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_example():
    """Probar endpoint de ejemplo"""
    print("\n📝 Probando endpoint de ejemplo...")
    try:
        response = requests.get(f"{BASE_URL}/example")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_prediction():
    """Probar predicción individual"""
    print("\n🔮 Probando predicción individual...")
    
    # Datos de prueba
    test_data = {
        "tienda_id": 1,
        "empleados": 20,
        "publicidad": 5000,
        "ubicacion": "urbana"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/predict",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        print(f"Request: {json.dumps(test_data, indent=2)}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_batch_prediction():
    """Probar predicción en lote"""
    print("\n📦 Probando predicción en lote...")
    
    # Datos de prueba en lote
    test_data = {
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
            },
            {
                "tienda_id": 3,
                "empleados": 25,
                "publicidad": 7000,
                "ubicacion": "suburbana"
            }
        ]
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/predict_batch",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        print(f"Request: {json.dumps(test_data, indent=2)}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_model_info():
    """Probar información del modelo"""
    print("\n📊 Probando información del modelo...")
    try:
        response = requests.get(f"{BASE_URL}/model-info")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_feature_importance():
    """Probar importancia de características"""
    print("\n⚖️ Probando importancia de características...")
    try:
        response = requests.get(f"{BASE_URL}/feature-importance")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Ejecutar todas las pruebas"""
    print("🧪 INICIANDO PRUEBAS DE LA API")
    print("=" * 50)
    
    # Esperar un momento para que la API se inicie
    print("⏳ Esperando que la API esté lista...")
    time.sleep(2)
    
    tests = [
        ("Health Check", test_health),
        ("Root Endpoint", test_root),
        ("Example Endpoint", test_example),
        ("Model Info", test_model_info),
        ("Feature Importance", test_feature_importance),
        ("Single Prediction", test_prediction),
        ("Batch Prediction", test_batch_prediction)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"🧪 {test_name}")
        print(f"{'='*50}")
        
        success = test_func()
        results.append((test_name, success))
        
        if success:
            print(f"✅ {test_name} - EXITOSO")
        else:
            print(f"❌ {test_name} - FALLÓ")
    
    # Resumen de resultados
    print(f"\n{'='*50}")
    print("📊 RESUMEN DE PRUEBAS")
    print(f"{'='*50}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASÓ" if success else "❌ FALLÓ"
        print(f"{test_name}: {status}")
    
    print(f"\n🎯 Resultado: {passed}/{total} pruebas exitosas")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron! La API está funcionando correctamente.")
    else:
        print("⚠️ Algunas pruebas fallaron. Revisa los errores arriba.")

if __name__ == "__main__":
    main()
