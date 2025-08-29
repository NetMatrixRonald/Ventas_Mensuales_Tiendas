# Predicción de Ventas Mensuales por Tienda

## Descripción del Proyecto

Este proyecto implementa un sistema de predicción de ventas mensuales por tienda utilizando regresión lineal, siguiendo la metodología CRISP-DM (Cross-Industry Standard Process for Data Mining).

## Estructura del Proyecto

```
├── data/
│   └── ventas_tiendas (4).csv
├── src/
│   ├── data_preprocessing.py
│   ├── model_training.py
│   ├── model_evaluation.py
│   └── utils.py
├── models/
│   └── (archivos .pkl del modelo entrenado)
├── notebooks/
│   └── exploratory_analysis.ipynb
├── api/
│   ├── main.py
│   └── requirements.txt
├── requirements.txt
└── README.md
```

## Metodología CRISP-DM

### 1. Comprensión del Negocio (Business Understanding)
- **Objetivo**: Predecir las ventas mensuales de las tiendas
- **Criterios de éxito**: Modelo con R² > 0.7 y RMSE bajo
- **Variables objetivo**: ventas

### 2. Comprensión de los Datos (Data Understanding)
- **Dataset**: ventas_tiendas.csv
- **Variables**:
  - tienda_id: Identificador de la tienda
  - empleados: Número de empleados
  - publicidad: Gasto en publicidad
  - ubicacion: Tipo de ubicación (rural, suburbana, urbana)
  - ventas: Ventas mensuales (variable objetivo)

### 3. Preparación de los Datos (Data Preparation)
- Limpieza de datos faltantes
- Codificación de variables categóricas
- Escalado de variables numéricas
- División train/test

### 4. Modelado (Modeling)
- Regresión Lineal
- Validación cruzada
- Optimización de hiperparámetros

### 5. Evaluación (Evaluation)
- Métricas: R², RMSE, MAE
- Validación del modelo
- Análisis de residuos

### 6. Despliegue (Deployment)
- API REST con FastAPI
- Despliegue en Render
- Documentación de la API

## Instalación y Uso

### Requisitos
```bash
pip install -r requirements.txt
```

### Entrenamiento del Modelo
```bash
python src/model_training.py
```

### Ejecutar la API
```bash
cd api
uvicorn main:app --reload
```

### Uso de la API
```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"tienda_id": 1, "empleados": 20, "publicidad": 5000, "ubicacion": "urbana"}'
```

## Despliegue en Render

1. Conectar el repositorio a Render
2. Configurar como Web Service
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`

## Autor
Desarrollado para el curso de Machine Learning del SENA
