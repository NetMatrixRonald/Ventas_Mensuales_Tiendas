# 🚀 Guía Rápida - Despliegue en Render

## ✅ Proyecto Completado

Tu proyecto de **Predicción de Ventas Mensuales por Tienda** está **100% completo** y listo para desplegar en Render.

## 📊 Resumen del Proyecto

- **Algoritmo:** Regresión Lineal
- **R² Score:** 0.5732
- **Archivos PKL:** 5/5 generados ✅
- **API FastAPI:** 9 endpoints ✅
- **Metodología:** CRISP-DM completa ✅

## 🎯 Pasos para Desplegar en Render

### 1. Subir a GitHub
```bash
git init
git add .
git commit -m "API de predicción de ventas - CRISP-DM completo"
git branch -M main
git remote add origin https://github.com/TU-USUARIO/ventas-prediction-api.git
git push -u origin main
```

### 2. Configurar en Render
1. Ve a [render.com](https://render.com)
2. Regístrate con tu cuenta de GitHub
3. Haz clic en "New +" → "Web Service"
4. Conecta tu repositorio
5. Configura:
   - **Name:** `ventas-prediction-api`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn api.main:app --host 0.0.0.0 --port $PORT`

### 3. ¡Listo!
- Render desplegará automáticamente tu API
- URL: `https://tu-app.onrender.com`
- Documentación: `https://tu-app.onrender.com/docs`

## 🌐 Endpoints de la API

| Endpoint | Descripción |
|----------|-------------|
| `/` | Información del modelo |
| `/health` | Estado del servicio |
| `/docs` | Documentación Swagger |
| `/predict` | Predicción individual |
| `/predict_batch` | Predicciones en lote |

## 📝 Ejemplo de Uso

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

## 📁 Archivos Importantes

- `api/main.py` - API para Render
- `models/` - Archivos PKL del modelo
- `render.yaml` - Configuración automática
- `requirements.txt` - Dependencias

## 🎉 ¡Tu API estará lista en minutos!

Una vez desplegada, podrás:
- ✅ Hacer predicciones de ventas
- ✅ Ver documentación automática
- ✅ Monitorear el servicio
- ✅ Escalar según necesidades

---

**¡Proyecto completado exitosamente! 🚀**
