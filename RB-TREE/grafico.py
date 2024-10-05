import numpy as np
import matplotlib.pyplot as plt

# Cargar los datos desde un archivo .txt
# Se asume que el archivo tiene dos columnas: N y comparaciones
data = np.loadtxt('tiempo.txt', skiprows=1)  # Saltamos la primera fila que contiene los títulos de las columnas

N = data[:, 0]  # Primera columna - Número de claves
comparaciones = data[:, 1]  # Segunda columna - Comparaciones

# Crear el gráfico
plt.figure(figsize=(8, 6))
plt.plot(N, comparaciones, 'ro-', label='Número de comparaciones')  # Puntos y línea roja

# Opcional: Añadir barras de error
error = np.random.uniform(0.5, 1.5, size=len(N))  # Generar algunos errores de ejemplo (esto debería ser ajustado según tus datos)
plt.errorbar(N, comparaciones, yerr=error, fmt='o', ecolor='black', capsize=5, linestyle='None')

# Etiquetas y título
plt.xlabel('number of keys N', fontsize=14)
plt.ylabel('compares', fontsize=14)
plt.title('Número de operaciones por cantidad de datos', fontsize=16)

# Mostrar la figura
plt.grid(True)
plt.legend()
plt.show()
