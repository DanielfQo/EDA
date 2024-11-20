import kdtree
import matplotlib.pyplot as plt


def leer_puntos_desde_txt(archivo_txt):
    puntos = []
    try:
        with open(archivo_txt, 'r') as file:
            for line in file:
                punto = tuple(map(int, line.strip().split(',')))
                puntos.append(punto)
    except FileNotFoundError:
        print(f"Error: El archivo {archivo_txt} no se encontró.")
    except Exception as e:
        print(f"Error al leer el archivo {archivo_txt}: {e}")
    return puntos


def medir_tiempos_por_k(arbol, archivo_csv, puntos_consulta, k_values):
    tiempos_por_punto = []
    for punto in puntos_consulta:
        tiempos = []
        for k in k_values:
            tiempo = kdtree.medir_tiempo_knn(arbol, archivo_csv, punto, k)
            tiempos.append(tiempo)
        tiempos_por_punto.append(tiempos)
    return tiempos_por_punto


def guardar_tiempos_en_txt(tiempos_por_punto, puntos_consulta, k_values, archivo_salida):
    try:
        with open(archivo_salida, 'w') as file:
            file.write("Punto de consulta, " + ", ".join([f"k={k}" for k in k_values]) + "\n")
            for punto, tiempos in zip(puntos_consulta, tiempos_por_punto):
                punto_str = ', '.join(map(str, punto))
                file.write(f"{punto_str}: " + ", ".join([str(tiempo) for tiempo in tiempos]) + "\n")
    except Exception as e:
        print(f"Error al escribir en el archivo {archivo_salida}: {e}")


def graficar_y_guardar(tiempos_por_punto, k_values, nombre_archivo):
    plt.figure(figsize=(10, 6))
    for i, tiempos in enumerate(tiempos_por_punto):
        plt.plot(k_values, tiempos, label=f'Punto {i+1}')
    plt.xlabel('Número de Vecinos (k)')
    plt.ylabel('Tiempo de Búsqueda (ms)')
    plt.title(f'Tiempo de Búsqueda de KNN para Diferentes Valores de k ({nombre_archivo})')
    plt.legend()
    plt.grid(True)
    plt.ylim(0, max(max(tiempos) for tiempos in tiempos_por_punto) * 1.1)
    plt.savefig(nombre_archivo)
    plt.close()


archivo_txt = './puntos_3d_10.txt'
puntos_consulta = leer_puntos_desde_txt(archivo_txt)

arbol2d = kdtree.KDTREE(dimension=3)

k_values_1 = list(range(100, 901, 100))
k_values_2 = list(range(1000, 9001, 1000))
k_values_3 = list(range(1000, 19001, 1000))

archivo_csv_1 = './pruebas/1000.csv'
tiempos_por_punto_1 = medir_tiempos_por_k(arbol2d, archivo_csv_1, puntos_consulta, k_values_1)
graficar_y_guardar(tiempos_por_punto_1, k_values_1, 'grafica_1.png')
guardar_tiempos_en_txt(tiempos_por_punto_1, puntos_consulta, k_values_1, 'tiempos_por_k_y_punto1.txt')

archivo_csv_2 = './pruebas/10000.csv'
tiempos_por_punto_2 = medir_tiempos_por_k(arbol2d, archivo_csv_2, puntos_consulta, k_values_2)
graficar_y_guardar(tiempos_por_punto_2, k_values_2, 'grafica_2.png')
guardar_tiempos_en_txt(tiempos_por_punto_2, puntos_consulta, k_values_2, 'tiempos_por_k_y_punto2.txt')

archivo_csv_3 = './pruebas/20000.csv'
tiempos_por_punto_3 = medir_tiempos_por_k(arbol2d, archivo_csv_3, puntos_consulta, k_values_3)
graficar_y_guardar(tiempos_por_punto_3, k_values_3, 'grafica_3.png')
guardar_tiempos_en_txt(tiempos_por_punto_3, puntos_consulta, k_values_3, 'tiempos_por_k_y_punto3.txt')
