"""
Módulo de Entrenamiento del Modelo - CRISP-DM
Fase 4: Modelado
Fase 5: Evaluación
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score, KFold
import joblib
import warnings
warnings.filterwarnings('ignore')

class ModelTrainer:
    def __init__(self, model_path='models/processed_data.pkl'):
        self.model_path = model_path
        self.model = None
        self.processed_data = None
        self.feature_importance = None
        
    def load_processed_data(self):
        """Cargar datos procesados"""
        print("=== FASE 4: MODELADO ===")
        
        try:
            self.processed_data = joblib.load(self.model_path)
            print("✅ Datos procesados cargados exitosamente")
            
            X_train = self.processed_data['X_train']
            X_test = self.processed_data['X_test']
            y_train = self.processed_data['y_train']
            y_test = self.processed_data['y_test']
            feature_cols = self.processed_data['feature_cols']
            target_col = self.processed_data['target_col']
            
            print(f"📊 Datos de entrenamiento: {X_train.shape}")
            print(f"📊 Datos de prueba: {X_test.shape}")
            print(f"🎯 Variable objetivo: {target_col}")
            print(f"🔢 Características: {len(feature_cols)}")
            
            return X_train, X_test, y_train, y_test, feature_cols, target_col
            
        except Exception as e:
            print(f"❌ Error al cargar datos procesados: {e}")
            return None, None, None, None, None, None
    
    def train_linear_regression(self, X_train, y_train):
        """Entrenar modelo de regresión lineal"""
        print("\n🤖 Entrenando modelo de Regresión Lineal...")
        
        # Crear y entrenar modelo
        self.model = LinearRegression()
        self.model.fit(X_train, y_train)
        
        print("✅ Modelo entrenado exitosamente")
        
        # Obtener coeficientes
        feature_cols = self.processed_data['feature_cols']
        coefficients = pd.DataFrame({
            'feature': feature_cols,
            'coefficient': self.model.coef_
        }).sort_values('coefficient', key=abs, ascending=False)
        
        print("\n📊 Coeficientes del modelo (top 10):")
        print(coefficients.head(10))
        
        self.feature_importance = coefficients
        
        return self.model
    
    def evaluate_model(self, X_train, X_test, y_train, y_test):
        """Evaluación del modelo - Fase 5: Evaluación"""
        print("\n=== FASE 5: EVALUACIÓN ===")
        
        # Predicciones
        y_train_pred = self.model.predict(X_train)
        y_test_pred = self.model.predict(X_test)
        
        # Métricas de evaluación
        print("\n📈 Métricas de Evaluación:")
        print("-" * 50)
        
        # R² Score
        r2_train = r2_score(y_train, y_train_pred)
        r2_test = r2_score(y_test, y_test_pred)
        print(f"R² Score - Entrenamiento: {r2_train:.4f}")
        print(f"R² Score - Prueba: {r2_test:.4f}")
        
        # Mean Absolute Error
        mae_train = mean_absolute_error(y_train, y_train_pred)
        mae_test = mean_absolute_error(y_test, y_test_pred)
        print(f"MAE - Entrenamiento: {mae_train:.4f}")
        print(f"MAE - Prueba: {mae_test:.4f}")
        
        # Root Mean Squared Error
        rmse_train = np.sqrt(mean_squared_error(y_train, y_train_pred))
        rmse_test = np.sqrt(mean_squared_error(y_test, y_test_pred))
        print(f"RMSE - Entrenamiento: {rmse_train:.4f}")
        print(f"RMSE - Prueba: {rmse_test:.4f}")
        
        # Cross-validation
        print("\n🔄 Validación Cruzada (5-fold):")
        cv_scores = cross_val_score(self.model, X_train, y_train, cv=5, scoring='r2')
        print(f"R² CV Scores: {cv_scores}")
        print(f"R² CV Mean: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
        
        # Guardar métricas
        metrics = {
            'r2_train': r2_train,
            'r2_test': r2_test,
            'mae_train': mae_train,
            'mae_test': mae_test,
            'rmse_train': rmse_train,
            'rmse_test': rmse_test,
            'cv_scores': cv_scores,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std()
        }
        
        return metrics, y_train_pred, y_test_pred
    
    def analyze_residuals(self, y_train, y_test, y_train_pred, y_test_pred):
        """Análisis de residuos"""
        print("\n📊 Análisis de Residuos...")
        
        # Calcular residuos
        residuals_train = y_train - y_train_pred
        residuals_test = y_test - y_test_pred
        
        # Crear gráficos de residuos
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. Residuos vs Predicciones (Train)
        axes[0, 0].scatter(y_train_pred, residuals_train, alpha=0.6, color='blue')
        axes[0, 0].axhline(y=0, color='red', linestyle='--')
        axes[0, 0].set_xlabel('Predicciones')
        axes[0, 0].set_ylabel('Residuos')
        axes[0, 0].set_title('Residuos vs Predicciones (Entrenamiento)')
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Residuos vs Predicciones (Test)
        axes[0, 1].scatter(y_test_pred, residuals_test, alpha=0.6, color='green')
        axes[0, 1].axhline(y=0, color='red', linestyle='--')
        axes[0, 1].set_xlabel('Predicciones')
        axes[0, 1].set_ylabel('Residuos')
        axes[0, 1].set_title('Residuos vs Predicciones (Prueba)')
        axes[0, 1].grid(True, alpha=0.3)
        
        # 3. Histograma de residuos (Train)
        axes[1, 0].hist(residuals_train, bins=30, alpha=0.7, color='blue', edgecolor='black')
        axes[1, 0].set_xlabel('Residuos')
        axes[1, 0].set_ylabel('Frecuencia')
        axes[1, 0].set_title('Distribución de Residuos (Entrenamiento)')
        axes[1, 0].grid(True, alpha=0.3)
        
        # 4. Q-Q Plot de residuos (Test)
        from scipy import stats
        stats.probplot(residuals_test, dist="norm", plot=axes[1, 1])
        axes[1, 1].set_title('Q-Q Plot de Residuos (Prueba)')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('residuals_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("📈 Gráficos de residuos guardados en 'residuals_analysis.png'")
        
        # Estadísticas de residuos
        print(f"\n📊 Estadísticas de Residuos (Prueba):")
        print(f"Media: {np.mean(residuals_test):.4f}")
        print(f"Desviación estándar: {np.std(residuals_test):.4f}")
        print(f"Mínimo: {np.min(residuals_test):.4f}")
        print(f"Máximo: {np.max(residuals_test):.4f}")
    
    def plot_feature_importance(self):
        """Visualizar importancia de características"""
        print("\n📊 Visualizando importancia de características...")
        
        if self.feature_importance is not None:
            plt.figure(figsize=(12, 8))
            
            # Top 15 características más importantes
            top_features = self.feature_importance.head(15)
            
            colors = ['red' if x < 0 else 'blue' for x in top_features['coefficient']]
            
            plt.barh(range(len(top_features)), top_features['coefficient'], color=colors, alpha=0.7)
            plt.yticks(range(len(top_features)), top_features['feature'])
            plt.xlabel('Coeficiente')
            plt.title('Importancia de Características (Coeficientes del Modelo)')
            plt.grid(True, alpha=0.3)
            
            # Añadir líneas de referencia
            plt.axvline(x=0, color='black', linestyle='-', alpha=0.5)
            
            plt.tight_layout()
            plt.savefig('feature_importance.png', dpi=300, bbox_inches='tight')
            plt.close()
            
            print("📈 Gráfico de importancia guardado en 'feature_importance.png'")
    
    def plot_predictions_vs_actual(self, y_train, y_test, y_train_pred, y_test_pred):
        """Gráfico de predicciones vs valores reales"""
        print("\n📈 Visualizando predicciones vs valores reales...")
        
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        # Entrenamiento
        axes[0].scatter(y_train, y_train_pred, alpha=0.6, color='blue')
        axes[0].plot([y_train.min(), y_train.max()], [y_train.min(), y_train.max()], 'r--', lw=2)
        axes[0].set_xlabel('Valores Reales')
        axes[0].set_ylabel('Predicciones')
        axes[0].set_title('Predicciones vs Reales (Entrenamiento)')
        axes[0].grid(True, alpha=0.3)
        
        # Prueba
        axes[1].scatter(y_test, y_test_pred, alpha=0.6, color='green')
        axes[1].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
        axes[1].set_xlabel('Valores Reales')
        axes[1].set_ylabel('Predicciones')
        axes[1].set_title('Predicciones vs Reales (Prueba)')
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('predictions_vs_actual.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("📈 Gráfico de predicciones guardado en 'predictions_vs_actual.png'")
    
    def save_model(self):
        """Guardar modelo entrenado"""
        print("\n💾 Guardando modelo...")
        
        # Guardar modelo
        joblib.dump(self.model, 'models/model.pkl')
        print("✅ Modelo guardado en 'models/model.pkl'")
        
        # Guardar scaler y encoders
        scaler = self.processed_data['scaler']
        label_encoders = self.processed_data['label_encoders']
        
        joblib.dump(scaler, 'models/scaler.pkl')
        joblib.dump(label_encoders, 'models/label_encoders.pkl')
        print("✅ Scaler y encoders guardados")
        
        # Guardar información del modelo
        model_info = {
            'model_type': 'LinearRegression',
            'feature_importance': self.feature_importance,
            'processed_data_info': {
                'feature_cols': self.processed_data['feature_cols'],
                'target_col': self.processed_data['target_col']
            }
        }
        
        joblib.dump(model_info, 'models/model_info.pkl')
        print("✅ Información del modelo guardada")
        
        return True
    
    def run_training_pipeline(self):
        """Ejecutar pipeline completo de entrenamiento"""
        print("🚀 INICIANDO PIPELINE DE ENTRENAMIENTO CRISP-DM")
        print("=" * 60)
        
        # Cargar datos
        data = self.load_processed_data()
        if data[0] is None:
            return False
        
        X_train, X_test, y_train, y_test, feature_cols, target_col = data
        
        # Entrenar modelo
        self.train_linear_regression(X_train, y_train)
        
        # Evaluar modelo
        metrics, y_train_pred, y_test_pred = self.evaluate_model(X_train, X_test, y_train, y_test)
        
        # Análisis adicionales
        self.analyze_residuals(y_train, y_test, y_train_pred, y_test_pred)
        self.plot_feature_importance()
        self.plot_predictions_vs_actual(y_train, y_test, y_train_pred, y_test_pred)
        
        # Guardar modelo
        self.save_model()
        
        # Resumen final
        print("\n" + "=" * 60)
        print("✅ PIPELINE DE ENTRENAMIENTO COMPLETADO")
        print("=" * 60)
        print(f"🎯 Modelo: Regresión Lineal")
        print(f"📊 R² Score (Prueba): {metrics['r2_test']:.4f}")
        print(f"📊 MAE (Prueba): {metrics['mae_test']:.4f}")
        print(f"📊 RMSE (Prueba): {metrics['rmse_test']:.4f}")
        print(f"🔄 CV R² Score: {metrics['cv_mean']:.4f} (+/- {metrics['cv_std'] * 2:.4f})")
        
        if metrics['r2_test'] > 0.7:
            print("🎉 ¡Excelente! El modelo tiene un buen rendimiento (R² > 0.7)")
        elif metrics['r2_test'] > 0.5:
            print("👍 Buen rendimiento del modelo (R² > 0.5)")
        else:
            print("⚠️ El modelo podría necesitar mejoras (R² < 0.5)")
        
        return True

if __name__ == "__main__":
    # Crear instancia y ejecutar pipeline
    trainer = ModelTrainer()
    trainer.run_training_pipeline()
