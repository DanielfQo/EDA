import math
import csv
import time
import heapq  # Para optimizar la lista de vecinos cercanos

class Nodo:
    def __init__(self, valor, izq=None, der=None):
        self.valor = valor
        self.izq = izq
        self.der = der

class KDTREE:
    def __init__(self, dimension=3):
        self.raiz = None
        self.dimension = dimension

    def insertar(self, valor):
        if len(valor) != self.dimension:
            raise ValueError(f"El valor debe tener {self.dimension} coordenadas.")
        if self.raiz is None:
            self.raiz = Nodo(valor)
        else:
            self._insertar_recursivo(self.raiz, valor, 0)

    def _insertar_recursivo(self, nodo, valor, profundidad):
        eje = profundidad % self.dimension
        if valor[eje] < nodo.valor[eje]:
            if nodo.izq is None:
                nodo.izq = Nodo(valor)
            else:
                self._insertar_recursivo(nodo.izq, valor, profundidad + 1)
        else:
            if nodo.der is None:
                nodo.der = Nodo(valor)
            else:
                self._insertar_recursivo(nodo.der, valor, profundidad + 1)

    def calcular_distancia(self, p1, p2):
        """Calcula la distancia euclidiana entre dos puntos."""
        return math.sqrt(sum((p1[i] - p2[i]) ** 2 for i in range(len(p1))))

    def k_vecinos_mas_proximos(self, punto, k):
        """Devuelve los k vecinos más cercanos al punto dado."""
        if len(punto) != self.dimension:
            raise ValueError(f"El punto debe tener {self.dimension} coordenadas.")
        # Usar un heap de tamaño fijo para mantener los k vecinos más cercanos
        vecinos = []
        self._k_vecinos_recursivo(self.raiz, punto, k, 0, vecinos)
        # Ordenar los vecinos antes de devolverlos
        return [heapq.heappop(vecinos)[1] for _ in range(len(vecinos))]

    def _k_vecinos_recursivo(self, nodo, punto, k, profundidad, vecinos):
        if nodo is None:
            return

        distancia = self.calcular_distancia(nodo.valor, punto)
        
        # Usar un heap max para mantener los k vecinos más cercanos de forma eficiente
        if len(vecinos) < k:
            heapq.heappush(vecinos, (-distancia, nodo.valor))
        elif distancia < -vecinos[0][0]:  # Compara con el mayor en el heap
            heapq.heappushpop(vecinos, (-distancia, nodo.valor))

        eje = profundidad % self.dimension
        direccion = nodo.izq if punto[eje] < nodo.valor[eje] else nodo.der
        self._k_vecinos_recursivo(direccion, punto, k, profundidad + 1, vecinos)
        
        # Revisar el otro lado del árbol si es necesario
        if len(vecinos) < k or abs(punto[eje] - nodo.valor[eje]) < -vecinos[0][0]:
            otro_lado = nodo.der if direccion is nodo.izq else nodo.izq
            self._k_vecinos_recursivo(otro_lado, punto, k, profundidad + 1, vecinos)

    def cargar_desde_csv(self, nombre_archivo):
        with open(nombre_archivo, 'r') as archivo_csv:
            lector_csv = csv.reader(archivo_csv)
            for fila in lector_csv:
                punto = tuple(map(int, fila))
                self.insertar(punto)

def medir_tiempo_knn(arbol_kdtree, archivo_csv, punto, k):
    arbol_kdtree.cargar_desde_csv(archivo_csv)
    inicio = time.time()
    vecinos = arbol_kdtree.k_vecinos_mas_proximos(punto, k)
    fin = time.time()
    tiempo_ms = round((fin - inicio) * 1000, 4)
    return tiempo_ms
