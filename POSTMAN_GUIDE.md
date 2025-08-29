# 🚀 Guía para Probar la API en Postman - Render

## 📋 Prerrequisitos

- ✅ API desplegada exitosamente en Render
- ✅ URL de tu API (ejemplo: `https://tu-app.onrender.com`)
- ✅ Postman instalado en tu computadora
- ✅ Conexión a internet

## 🔧 Configuración Inicial en Postman

### 1. **Crear una Nueva Colección**

1. Abre Postman
2. Haz clic en "New" → "Collection"
3. Nombra la colección: `Ventas Prediction API`
4. Descripción: `API de Predicción de Ventas Mensuales por Tienda`

### 2. **Configurar Variables de Entorno**

1. Haz clic en "Environments" → "New"
2. Nombre: `Ventas API - Render`
3. Agrega las siguientes variables:

| Variable | Initial Value | Current Value |
|----------|---------------|---------------|
| `base_url` | `https://tu-app.onrender.com` | `https://tu-app.onrender.com` |
| `api_key` | (dejar vacío) | (dejar vacío) |

4. Haz clic en "Save"

## 🌐 Endpoints para Probar

### 1. **GET - Información del Modelo**
- **URL:** `{{base_url}}/`
- **Método:** GET
- **Descripción:** Obtener información básica del modelo

**Headers:**
```
Content-Type: application/json
```

**Respuesta Esperada:**
```json
{
  "message": "API de Predicción de Ventas Mensuales por Tienda",
  "version": "1.0.0",
  "model_type": "LinearRegression",
  "features": 4,
  "methodology": "CRISP-DM",
  "algorithm": "Regresión Lineal",
  "docs": "/docs",
  "health": "/health",
  "example": "/example"
}
```

### 2. **GET - Estado del Servicio**
- **URL:** `{{base_url}}/health`
- **Método:** GET
- **Descripción:** Verificar si el servicio está funcionando

**Respuesta Esperada:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_type": "LinearRegression",
  "version": "1.0.0"
}
```

### 3. **GET - Ejemplo de Uso**
- **URL:** `{{base_url}}/example`
- **Método:** GET
- **Descripción:** Obtener ejemplo de datos de entrada

**Respuesta Esperada:**
```json
{
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
```

### 4. **POST - Predicción Individual**
- **URL:** `{{base_url}}/predict`
- **Método:** POST
- **Descripción:** Realizar predicción de ventas para una tienda

**Headers:**
```
Content-Type: application/json
```

**Body (raw JSON):**
```json
{
  "tienda_id": 1,
  "empleados": 20,
  "publicidad": 5000,
  "ubicacion": "urbana"
}
```

**Respuesta Esperada:**
```json
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

### 5. **POST - Predicciones en Lote**
- **URL:** `{{base_url}}/predict_batch`
- **Método:** POST
- **Descripción:** Realizar predicciones para múltiples tiendas

**Headers:**
```
Content-Type: application/json
```

**Body (raw JSON):**
```json
{
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
```

**Respuesta Esperada:**
```json
{
  "predictions": [45000.0, 35000.0, 55000.0],
  "model_info": {
    "model_type": "LinearRegression",
    "r2_score": 0.57,
    "rmse": 10739.31,
    "batch_size": 3
  }
}
```

### 6. **GET - Información Detallada del Modelo**
- **URL:** `{{base_url}}/model-info`
- **Método:** GET
- **Descripción:** Obtener información técnica del modelo

**Respuesta Esperada:**
```json
{
  "model_type": "LinearRegression",
  "features": ["tienda_id", "empleados", "publicidad", "ubicacion"],
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
    "feature_cols": ["tienda_id", "empleados", "publicidad", "ubicacion"],
    "target_col": "ventas"
  }
}
```

### 7. **GET - Importancia de Características**
- **URL:** `{{base_url}}/feature-importance`
- **Método:** GET
- **Descripción:** Ver la importancia de cada característica

**Respuesta Esperada:**
```json
{
  "feature_importance": [
    {
      "feature": "empleados",
      "coefficient": 11583.705021
    },
    {
      "feature": "ubicacion",
      "coefficient": 5364.847664
    },
    {
      "feature": "publicidad",
      "coefficient": 1482.179605
    },
    {
      "feature": "tienda_id",
      "coefficient": 89.109364
    }
  ],
  "model_type": "LinearRegression"
}
```

## 🧪 Casos de Prueba Recomendados

### **Caso 1: Tienda Urbana con Muchos Empleados**
```json
{
  "tienda_id": 10,
  "empleados": 30,
  "publicidad": 8000,
  "ubicacion": "urbana"
}
```

### **Caso 2: Tienda Rural Pequeña**
```json
{
  "tienda_id": 25,
  "empleados": 5,
  "publicidad": 1000,
  "ubicacion": "rural"
}
```

### **Caso 3: Tienda Suburbana Mediana**
```json
{
  "tienda_id": 50,
  "empleados": 15,
  "publicidad": 4000,
  "ubicacion": "suburbana"
}
```

### **Caso 4: Datos Extremos (Para Validación)**
```json
{
  "tienda_id": 100,
  "empleados": 50,
  "publicidad": 20000,
  "ubicacion": "urbana"
}
```

## ⚠️ Casos de Error para Probar

### **Error 1: Ubicación Inválida**
```json
{
  "tienda_id": 1,
  "empleados": 20,
  "publicidad": 5000,
  "ubicacion": "centro"
}
```
**Respuesta Esperada:** Error 422 - Validation Error

### **Error 2: Datos Faltantes**
```json
{
  "tienda_id": 1,
  "empleados": 20,
  "publicidad": 5000
}
```
**Respuesta Esperada:** Error 422 - Validation Error

### **Error 3: Valores Fuera de Rango**
```json
{
  "tienda_id": 1,
  "empleados": 100,
  "publicidad": 50000,
  "ubicacion": "urbana"
}
```
**Respuesta Esperada:** Error 422 - Validation Error

## 📊 Automatización con Postman

### **1. Crear Tests Automáticos**

Para cada request, puedes agregar tests en la pestaña "Tests":

```javascript
// Test para predicción individual
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response has prediction", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('prediction');
    pm.expect(jsonData.prediction).to.be.a('number');
});

pm.test("Response has confidence", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('confidence');
    pm.expect(jsonData.confidence).to.be.a('number');
    pm.expect(jsonData.confidence).to.be.above(0);
    pm.expect(jsonData.confidence).to.be.below(1);
});
```

### **2. Variables Dinámicas**

Puedes usar variables para hacer las pruebas más dinámicas:

```json
{
  "tienda_id": {{$randomInt(1, 100)}},
  "empleados": {{$randomInt(1, 50)}},
  "publicidad": {{$randomInt(1000, 15000)}},
  "ubicacion": "{{$randomArrayItem(['rural', 'suburbana', 'urbana'])}}"
}
```

## 🔍 Monitoreo y Logs

### **Verificar Logs en Render:**
1. Ve a tu dashboard en Render
2. Selecciona tu servicio
3. Ve a la pestaña "Logs"
4. Monitorea las requests en tiempo real

### **Métricas a Observar:**
- Tiempo de respuesta
- Códigos de estado HTTP
- Errores de validación
- Errores del modelo

## 📱 Documentación Automática

### **Swagger UI:**
- **URL:** `{{base_url}}/docs`
- **Descripción:** Documentación interactiva de la API

### **ReDoc:**
- **URL:** `{{base_url}}/redoc`
- **Descripción:** Documentación alternativa más limpia

## 🎯 Checklist de Pruebas

- [ ] GET `/` - Información del modelo
- [ ] GET `/health` - Estado del servicio
- [ ] GET `/example` - Ejemplo de uso
- [ ] POST `/predict` - Predicción individual
- [ ] POST `/predict_batch` - Predicciones en lote
- [ ] GET `/model-info` - Información del modelo
- [ ] GET `/feature-importance` - Importancia de características
- [ ] GET `/docs` - Documentación Swagger
- [ ] Casos de error - Validaciones
- [ ] Tests automáticos - Funcionando

## 🚀 Próximos Pasos

1. **Exportar Colección:** Guarda tu colección de Postman
2. **Compartir:** Comparte la colección con tu equipo
3. **Monitorear:** Configura alertas para errores
4. **Optimizar:** Analiza tiempos de respuesta

---

**¡Tu API está lista para ser probada exhaustivamente en Postman! 🎉**
