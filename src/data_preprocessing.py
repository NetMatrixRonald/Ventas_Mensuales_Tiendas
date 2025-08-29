"""
Módulo de Preprocesamiento de Datos - CRISP-DM
Fase 2: Comprensión de los Datos
Fase 3: Preparación de los Datos
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

class DataPreprocessor:
    def __init__(self, data_path='data/ventas_tiendas (4).csv'):
        self.data_path = data_path
        self.df = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        
    def load_data(self):
        """Cargar y explorar los datos - Fase 2: Comprensión de los Datos"""
        print("=== FASE 2: COMPRENSIÓN DE LOS DATOS ===")
        
        try:
            self.df = pd.read_csv(self.data_path)
            print(f"✅ Dataset cargado exitosamente")
            print(f"📊 Dimensiones: {self.df.shape}")
            print(f"📋 Columnas: {list(self.df.columns)}")
            
        except Exception as e:
            print(f"❌ Error al cargar el dataset: {e}")
            return False
            
        return True
    
    def explore_data(self):
        """Exploración detallada de los datos"""
        print("\n=== EXPLORACIÓN DE DATOS ===")
        
        # Información básica
        print("\n📈 Información del dataset:")
        print(self.df.info())
        
        # Estadísticas descriptivas
        print("\n📊 Estadísticas descriptivas:")
        print(self.df.describe())
        
        # Valores nulos
        print("\n🔍 Valores nulos por columna:")
        null_counts = self.df.isnull().sum()
        print(null_counts[null_counts > 0] if null_counts.sum() > 0 else "No hay valores nulos")
        
        # Tipos de datos
        print("\n📝 Tipos de datos:")
        print(self.df.dtypes.value_counts())
        
        # Variables categóricas
        categorical_cols = self.df.select_dtypes(include=['object']).columns
        print(f"\n🏷️ Variables categóricas: {list(categorical_cols)}")
        
        # Variables numéricas
        numerical_cols = self.df.select_dtypes(include=[np.number]).columns
        print(f"🔢 Variables numéricas: {list(numerical_cols)}")
        
        return categorical_cols, numerical_cols
    
    def analyze_target_variable(self):
        """Análisis de la variable objetivo (ventas)"""
        print("\n=== ANÁLISIS DE LA VARIABLE OBJETIVO ===")
        
        # Buscar la columna de ventas
        ventas_cols = [col for col in self.df.columns if 'venta' in col.lower() or 'sales' in col.lower()]
        
        if ventas_cols:
            target_col = ventas_cols[0]
            print(f"🎯 Variable objetivo identificada: {target_col}")
            
            # Estadísticas de la variable objetivo
            print(f"\n📊 Estadísticas de {target_col}:")
            print(self.df[target_col].describe())
            
            # Distribución
            plt.figure(figsize=(12, 4))
            
            plt.subplot(1, 2, 1)
            plt.hist(self.df[target_col], bins=30, alpha=0.7, color='skyblue', edgecolor='black')
            plt.title(f'Distribución de {target_col}')
            plt.xlabel(target_col)
            plt.ylabel('Frecuencia')
            
            plt.subplot(1, 2, 2)
            plt.boxplot(self.df[target_col])
            plt.title(f'Boxplot de {target_col}')
            plt.ylabel(target_col)
            
            plt.tight_layout()
            plt.savefig('target_analysis.png', dpi=300, bbox_inches='tight')
            plt.close()
            
            print(f"📈 Gráficos guardados en 'target_analysis.png'")
            
            return target_col
        else:
            print("⚠️ No se encontró una columna de ventas. Revisar el dataset.")
            return None
    
    def clean_data(self):
        """Limpieza de datos - Fase 3: Preparación de los Datos"""
        print("\n=== FASE 3: PREPARACIÓN DE LOS DATOS ===")
        
        # Guardar copia original
        self.df_original = self.df.copy()
        
        # 1. Manejo de valores nulos
        print("\n🧹 Limpieza de valores nulos...")
        null_counts_before = self.df.isnull().sum().sum()
        
        # Para variables numéricas, rellenar con la mediana
        numerical_cols = self.df.select_dtypes(include=[np.number]).columns
        for col in numerical_cols:
            if self.df[col].isnull().sum() > 0:
                median_val = self.df[col].median()
                self.df[col].fillna(median_val, inplace=True)
                print(f"   ✅ {col}: valores nulos rellenados con mediana ({median_val:.2f})")
        
        # Para variables categóricas, rellenar con la moda
        categorical_cols = self.df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            if self.df[col].isnull().sum() > 0:
                mode_val = self.df[col].mode()[0]
                self.df[col].fillna(mode_val, inplace=True)
                print(f"   ✅ {col}: valores nulos rellenados con moda ('{mode_val}')")
        
        null_counts_after = self.df.isnull().sum().sum()
        print(f"   📊 Valores nulos: {null_counts_before} → {null_counts_after}")
        
        # 2. Detección y manejo de outliers
        print("\n🔍 Detección de outliers...")
        outliers_removed = 0
        
        for col in numerical_cols:
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = self.df[(self.df[col] < lower_bound) | (self.df[col] > upper_bound)]
            if len(outliers) > 0:
                print(f"   ⚠️ {col}: {len(outliers)} outliers detectados")
                # Capar outliers en lugar de eliminarlos
                self.df[col] = np.clip(self.df[col], lower_bound, upper_bound)
                outliers_removed += len(outliers)
        
        print(f"   📊 Total outliers manejados: {outliers_removed}")
        
        return True
    
    def encode_categorical_variables(self):
        """Codificación de variables categóricas"""
        print("\n🏷️ Codificación de variables categóricas...")
        
        categorical_cols = self.df.select_dtypes(include=['object']).columns
        
        for col in categorical_cols:
            if col != 'ventas':  # No codificar la variable objetivo si es categórica
                le = LabelEncoder()
                self.df[col] = le.fit_transform(self.df[col])
                self.label_encoders[col] = le
                print(f"   ✅ {col}: codificada con LabelEncoder")
        
        return True
    
    def scale_numerical_features(self, target_col):
        """Escalado de características numéricas"""
        print("\n📏 Escalado de características numéricas...")
        
        # Separar características y objetivo
        feature_cols = [col for col in self.df.columns if col != target_col]
        
        # Escalar características
        features_scaled = self.scaler.fit_transform(self.df[feature_cols])
        self.df_scaled = pd.DataFrame(features_scaled, columns=feature_cols)
        self.df_scaled[target_col] = self.df[target_col]
        
        print(f"   ✅ Características escaladas: {len(feature_cols)} columnas")
        
        return feature_cols
    
    def split_data(self, target_col, test_size=0.2, random_state=42):
        """División de datos en entrenamiento y prueba"""
        print("\n✂️ División de datos en entrenamiento y prueba...")
        
        X = self.df_scaled.drop(columns=[target_col])
        y = self.df_scaled[target_col]
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        
        print(f"   📊 Conjunto de entrenamiento: {X_train.shape}")
        print(f"   📊 Conjunto de prueba: {X_test.shape}")
        
        return X_train, X_test, y_train, y_test
    
    def save_processed_data(self, X_train, X_test, y_train, y_test, feature_cols, target_col):
        """Guardar datos procesados"""
        print("\n💾 Guardando datos procesados...")
        
        # Guardar datos procesados
        processed_data = {
            'X_train': X_train,
            'X_test': X_test,
            'y_train': y_train,
            'y_test': y_test,
            'feature_cols': feature_cols,
            'target_col': target_col,
            'scaler': self.scaler,
            'label_encoders': self.label_encoders
        }
        
        import joblib
        joblib.dump(processed_data, 'models/processed_data.pkl')
        print("   ✅ Datos procesados guardados en 'models/processed_data.pkl'")
        
        return True
    
    def run_preprocessing_pipeline(self):
        """Ejecutar pipeline completo de preprocesamiento"""
        print("🚀 INICIANDO PIPELINE DE PREPROCESAMIENTO CRISP-DM")
        print("=" * 60)
        
        # Fase 2: Comprensión de los Datos
        if not self.load_data():
            return False
        
        categorical_cols, numerical_cols = self.explore_data()
        target_col = self.analyze_target_variable()
        
        if target_col is None:
            print("❌ No se pudo identificar la variable objetivo")
            return False
        
        # Fase 3: Preparación de los Datos
        if not self.clean_data():
            return False
        
        if not self.encode_categorical_variables():
            return False
        
        feature_cols = self.scale_numerical_features(target_col)
        X_train, X_test, y_train, y_test = self.split_data(target_col)
        
        if not self.save_processed_data(X_train, X_test, y_train, y_test, feature_cols, target_col):
            return False
        
        print("\n✅ PIPELINE DE PREPROCESAMIENTO COMPLETADO EXITOSAMENTE")
        print("=" * 60)
        
        return True

if __name__ == "__main__":
    # Crear instancia y ejecutar pipeline
    preprocessor = DataPreprocessor()
    preprocessor.run_preprocessing_pipeline()
