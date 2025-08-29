import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configurar matplotlib para mostrar gráficos
plt.style.use('default')
sns.set_palette("husl")

# Leer el dataset
print("Leyendo el dataset...")
df = pd.read_csv('ventas_tiendas (4).csv')

# Información básica del dataset
print("\n=== INFORMACIÓN BÁSICA DEL DATASET ===")
print(f"Dimensiones del dataset: {df.shape}")
print(f"Columnas: {list(df.columns)}")
print(f"Tipos de datos:\n{df.dtypes}")

# Primeras filas
print("\n=== PRIMERAS 10 FILAS ===")
print(df.head(10))

# Información estadística
print("\n=== ESTADÍSTICAS DESCRIPTIVAS ===")
print(df.describe())

# Verificar valores nulos
print("\n=== VALORES NULOS ===")
print(df.isnull().sum())

# Información de memoria
print(f"\n=== USO DE MEMORIA ===")
print(f"Memoria utilizada: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

# Guardar información en un archivo
with open('dataset_info.txt', 'w', encoding='utf-8') as f:
    f.write("INFORMACIÓN DEL DATASET VENTAS_TIENDAS\n")
    f.write("=" * 50 + "\n")
    f.write(f"Dimensiones: {df.shape}\n")
    f.write(f"Columnas: {list(df.columns)}\n")
    f.write(f"Tipos de datos:\n{df.dtypes}\n")
    f.write(f"Valores nulos:\n{df.isnull().sum()}\n")
    f.write(f"Estadísticas descriptivas:\n{df.describe()}\n")

print("\nInformación guardada en 'dataset_info.txt'")
