# Resumen del Proyecto - Predicción de Ventas Mensuales por Tienda

## 🎯 Objetivo del Proyecto

Este proyecto implementa un sistema completo de predicción de ventas mensuales por tienda utilizando **Regresión Lineal** y siguiendo la metodología **CRISP-DM**. El proyecto incluye:

- ✅ Análisis exploratorio de datos
- ✅ Preprocesamiento y limpieza de datos
- ✅ Entrenamiento de modelo de regresión lineal
- ✅ Evaluación y validación del modelo
- ✅ API REST con FastAPI
- ✅ Archivos PKL para el modelo
- ✅ Documentación completa para despliegue en Render

## 📊 Métricas del Modelo

- **Algoritmo:** Regresión Lineal
- **R² Score:** 0.5732
- **RMSE:** 10739.31
- **MAE:** 8532.41
- **Validación Cruzada:** 0.5883 (±0.0308)

## 📁 Estructura del Proyecto

```
├── data/
│   └── ventas_tiendas (4).csv          # Dataset original (10,000 registros)
├── models/
│   ├── model.pkl                       # Modelo entrenado
│   ├── scaler.pkl                      # Escalador de características
│   ├── label_encoders.pkl              # Codificadores de etiquetas
│   ├── model_info.pkl                  # Información del modelo
│   └── processed_data.pkl              # Datos procesados
├── src/
│   ├── data_preprocessing.py           # Preprocesamiento CRISP-DM Fases 2-3
│   ├── model_training.py               # Entrenamiento CRISP-DM Fases 4-5
│   └── api.py                          # API original
├── api/
│   ├── main.py                         # API FastAPI para Render
│   └── requirements.txt                # Dependencias de la API
├── notebooks/                          # Jupyter notebooks
├── requirements.txt                    # Dependencias principales
├── render.yaml                         # Configuración de Render
├── DEPLOYMENT.md                       # Guía de despliegue
├── test_api.py                         # Script de pruebas
├── simple_api.py                       # API simplificada
├── verify_model.py                     # Verificación de archivos
└── README.md                           # Documentación principal
```

## 🔧 Archivos PKL Generados

### 1. `models/model.pkl`
- **Tipo:** LinearRegression
- **Tamaño:** 921 bytes
- **Coeficientes:** 4 características
- **Contenido:** Modelo entrenado de regresión lineal

### 2. `models/scaler.pkl`
- **Tipo:** StandardScaler
- **Tamaño:** 1015 bytes
- **Función:** Escalado de características numéricas

### 3. `models/label_encoders.pkl`
- **Tipo:** LabelEncoder
- **Tamaño:** 517 bytes
- **Función:** Codificación de variable categórica 'ubicacion'

### 4. `models/model_info.pkl`
- **Tipo:** Diccionario con información del modelo
- **Tamaño:** 1456 bytes
- **Contenido:** Métricas, características, información de entrenamiento

### 5. `models/processed_data.pkl`
- **Tipo:** Datos procesados
- **Tamaño:** 706KB
- **Contenido:** Datos de entrenamiento y prueba procesados

## 🌐 API FastAPI

### Endpoints Disponibles

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/` | GET | Información del modelo |
| `/health` | GET | Estado del servicio |
| `/docs` | GET | Documentación Swagger |
| `/redoc` | GET | Documentación ReDoc |
| `/example` | GET | Ejemplo de uso |
| `/predict` | POST | Predicción individual |
| `/predict_batch` | POST | Predicciones en lote |
| `/model-info` | GET | Información del modelo |
| `/feature-importance` | GET | Importancia de características |

### Ejemplo de Uso

```bash
# Predicción individual
curl -X POST "https://tu-app.onrender.com/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "tienda_id": 1,
       "empleados": 20,
       "publicidad": 5000,
       "ubicacion": "urbana"
     }'

# Respuesta esperada
{
  "prediction": 45000.0,
  "confidence": 0.57,
  "model_info": {
    "model_type": "LinearRegression",
    "r2_score": 0.57,
    "rmse": 10739.31
  }
}
```

## 🚀 Despliegue en Render

### Pasos para Desplegar

1. **Subir a GitHub:**
   ```bash
   git init
   git add .
   git commit -m "API de predicción de ventas - CRISP-DM"
   git branch -M main
   git remote add origin https://github.com/tu-usuario/ventas-prediction-api.git
   git push -u origin main
   ```

2. **Configurar en Render:**
   - Crear cuenta en [render.com](https://render.com)
   - Conectar repositorio de GitHub
   - Configurar como Web Service
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn api.main:app --host 0.0.0.0 --port $PORT`

3. **Variables de Entorno (Opcional):**
   - `PYTHON_VERSION`: `3.9.16`
   - `ENVIRONMENT`: `production`

### Configuración Automática

El archivo `render.yaml` está configurado para despliegue automático:

```yaml
services:
  - type: web
    name: ventas-prediction-api
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn api.main:app --host 0.0.0.0 --port $PORT
```

## 📈 Metodología CRISP-DM Implementada

### ✅ Fase 1: Comprensión del Negocio
- Objetivo: Predecir ventas mensuales por tienda
- Criterios de éxito: R² > 0.5, RMSE bajo
- Variable objetivo: ventas

### ✅ Fase 2: Comprensión de los Datos
- Dataset: 10,000 registros
- Variables: tienda_id, empleados, publicidad, ubicacion, ventas
- Análisis exploratorio completo

### ✅ Fase 3: Preparación de los Datos
- Limpieza de valores nulos (2,000 → 0)
- Manejo de outliers (126 detectados)
- Codificación de variables categóricas
- Escalado de características

### ✅ Fase 4: Modelado
- Algoritmo: Regresión Lineal
- Validación cruzada: 5-fold
- Optimización de hiperparámetros

### ✅ Fase 5: Evaluación
- R² Score: 0.5732
- RMSE: 10739.31
- MAE: 8532.41
- Análisis de residuos

### ✅ Fase 6: Despliegue
- API REST con FastAPI
- Documentación automática
- Listo para producción en Render

## 🧪 Pruebas y Validación

### Scripts de Prueba Incluidos

1. **`test_api.py`** - Pruebas completas de la API
2. **`verify_model.py`** - Verificación de archivos del modelo
3. **`simple_api.py`** - API simplificada para pruebas

### Comandos de Prueba

```bash
# Verificar archivos del modelo
python verify_model.py

# Probar API localmente
python simple_api.py

# Ejecutar pruebas completas
python test_api.py
```

## 📊 Características del Modelo

### Variables de Entrada
- **tienda_id:** ID de la tienda (1-100)
- **empleados:** Número de empleados (1-50)
- **publicidad:** Gasto en publicidad (0-20,000)
- **ubicacion:** Tipo de ubicación (rural, suburbana, urbana)

### Importancia de Características
1. **empleados:** 11583.71 (más importante)
2. **ubicacion:** 5364.85
3. **publicidad:** 1482.18
4. **tienda_id:** 89.11

## 🎉 Estado del Proyecto

### ✅ Completado
- [x] Análisis exploratorio de datos
- [x] Preprocesamiento completo
- [x] Entrenamiento del modelo
- [x] Evaluación y validación
- [x] Generación de archivos PKL
- [x] API REST con FastAPI
- [x] Documentación completa
- [x] Configuración para Render

### 🚀 Listo para Despliegue
- [x] Archivos PKL generados y verificados
- [x] API configurada para Render
- [x] Dependencias especificadas
- [x] Documentación de despliegue
- [x] Scripts de prueba incluidos

## 📞 Soporte y Contacto

- **Documentación:** `/docs` en la API desplegada
- **Issues:** GitHub del proyecto
- **Render Support:** [support.render.com](https://support.render.com)

---

**¡El proyecto está completo y listo para ser desplegado en Render! 🚀**

**Métricas Finales:**
- **R² Score:** 0.5732 ✅
- **RMSE:** 10739.31 ✅
- **Archivos PKL:** 5/5 ✅
- **API Endpoints:** 9/9 ✅
- **Documentación:** 100% ✅
