# Guía de Despliegue en Render

## Descripción del Proyecto

Este proyecto implementa un sistema de predicción de ventas mensuales por tienda utilizando regresión lineal, siguiendo la metodología CRISP-DM. La API está construida con FastAPI y está lista para ser desplegada en Render.

## Estructura del Proyecto para Render

```
├── data/
│   └── ventas_tiendas (4).csv          # Dataset original
├── models/
│   ├── model.pkl                       # Modelo entrenado
│   ├── scaler.pkl                      # Escalador de características
│   ├── label_encoders.pkl              # Codificadores de etiquetas
│   ├── model_info.pkl                  # Información del modelo
│   └── processed_data.pkl              # Datos procesados
├── api/
│   ├── main.py                         # API FastAPI
│   └── requirements.txt                # Dependencias de la API
├── src/
│   ├── data_preprocessing.py           # Preprocesamiento de datos
│   ├── model_training.py               # Entrenamiento del modelo
│   └── api.py                          # API original
├── requirements.txt                    # Dependencias principales
├── render.yaml                         # Configuración de Render
├── test_api.py                         # Script de pruebas
└── README.md                           # Documentación principal
```

## Pasos para Desplegar en Render

### 1. Preparación del Repositorio

1. **Subir el código a GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: API de predicción de ventas"
   git branch -M main
   git remote add origin https://github.com/tu-usuario/ventas-prediction-api.git
   git push -u origin main
   ```

### 2. Configuración en Render

1. **Crear cuenta en Render:**
   - Ve a [render.com](https://render.com)
   - Regístrate con tu cuenta de GitHub

2. **Crear nuevo Web Service:**
   - Haz clic en "New +"
   - Selecciona "Web Service"
   - Conecta tu repositorio de GitHub

3. **Configurar el servicio:**
   - **Name:** `ventas-prediction-api`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

### 3. Variables de Entorno (Opcional)

Si necesitas configurar variables de entorno:
- **PYTHON_VERSION:** `3.9.16`
- **ENVIRONMENT:** `production`

### 4. Despliegue Automático

Una vez configurado:
1. Render detectará automáticamente los cambios en tu repositorio
2. Cada push a la rama principal activará un nuevo despliegue
3. El servicio estará disponible en: `https://tu-app.onrender.com`

## Endpoints de la API

### Endpoints Principales

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

#### Predicción Individual
```bash
curl -X POST "https://tu-app.onrender.com/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "tienda_id": 1,
       "empleados": 20,
       "publicidad": 5000,
       "ubicacion": "urbana"
     }'
```

#### Predicción en Lote
```bash
curl -X POST "https://tu-app.onrender.com/predict_batch" \
     -H "Content-Type: application/json" \
     -d '{
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
     }'
```

## Monitoreo y Logs

### Ver Logs en Render
1. Ve a tu dashboard en Render
2. Selecciona tu servicio
3. Ve a la pestaña "Logs"
4. Monitorea los logs en tiempo real

### Métricas del Modelo
- **R² Score:** 0.5732
- **RMSE:** 10739.31
- **MAE:** 8532.41
- **Algoritmo:** Regresión Lineal

## Solución de Problemas

### Problemas Comunes

1. **Error de dependencias:**
   - Verifica que `requirements.txt` esté en la raíz
   - Asegúrate de que todas las dependencias estén listadas

2. **Error de modelo no encontrado:**
   - Verifica que los archivos `.pkl` estén en `/models/`
   - Asegúrate de que el modelo se haya entrenado correctamente

3. **Error de puerto:**
   - Render usa la variable `$PORT` automáticamente
   - No cambies el comando de inicio

4. **Timeout en el primer despliegue:**
   - El primer despliegue puede tardar más tiempo
   - Los archivos del modelo son grandes y tardan en subir

### Comandos de Debug

```bash
# Verificar estructura del proyecto
ls -la

# Verificar archivos del modelo
ls -la models/

# Probar API localmente
python -m uvicorn main:app --reload

# Ejecutar pruebas
python test_api.py
```

## Actualizaciones del Modelo

Para actualizar el modelo:

1. **Entrenar nuevo modelo:**
   ```bash
   python src/data_preprocessing.py
   python src/model_training.py
   ```

2. **Subir cambios:**
   ```bash
   git add .
   git commit -m "Update model"
   git push
   ```

3. **Render desplegará automáticamente**

## Costos y Límites

- **Plan Gratuito:** 750 horas/mes
- **Sleep Mode:** Después de 15 minutos de inactividad
- **Cold Start:** ~30 segundos para el primer request después del sleep

## Contacto y Soporte

- **Documentación:** `/docs` en tu API desplegada
- **Issues:** GitHub del proyecto
- **Render Support:** [support.render.com](https://support.render.com)

---

**¡Tu API de predicción de ventas está lista para producción! 🚀**
