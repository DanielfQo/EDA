import pygame as pg

# Colores
COLOR_FONDO = (255, 255, 255)
COLOR_NODO = (0, 0, 255)
COLOR_DIVISION = (255, 0, 0)

class Nodo:
    def __init__(self, valor, izq=None, der=None):
        self.valor = valor
        self.izq = izq
        self.der = der

class KDTREE:
    def __init__(self):
        self.raiz = None

    def insertar(self, valor):
        if self.raiz is None:
            self.raiz = Nodo(valor)
        else:
            self._insertar_recursivo(self.raiz, valor, 0)

    def _insertar_recursivo(self, nodo, valor, profundidad):
        eje = profundidad % 2
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

    def dibujar(self, pantalla, nodo=None, rect=None, profundidad=0):
        # Verificar si estamos en el nodo raíz
        ancho, alto = pantalla.get_size()
        if nodo is None:
            nodo = self.raiz
            rect = (0, 0, ancho, alto)

        # Si el nodo es None, no continuar
        if nodo is None:
            return

        # Coordenadas del nodo actual
        x, y = nodo.valor
        eje = profundidad % 2

        # Dibujar línea divisoria y actualizar rectángulos para hijos
        if eje == 0:  # Eje vertical
            pg.draw.line(pantalla, COLOR_DIVISION, (x, rect[1]), (x, rect[1] + rect[3]), 1)
            rect_izq = (rect[0], rect[1], x - rect[0], rect[3])
            rect_der = (x, rect[1], rect[2] - (x - rect[0]), rect[3])
        else:  # Eje horizontal
            pg.draw.line(pantalla, COLOR_DIVISION, (rect[0], y), (rect[0] + rect[2], y), 1)
            rect_izq = (rect[0], rect[1], rect[2], y - rect[1])
            rect_der = (rect[0], y, rect[2], rect[3] - (y - rect[1]))

        # Dibujar el nodo
        pg.draw.circle(pantalla, COLOR_NODO, (x, y), 5)

        # Llamada recursiva para los hijos, solo si existen
        if nodo.izq is not None:
            self.dibujar(pantalla, nodo.izq, rect_izq, profundidad + 1)
        if nodo.der is not None:
            self.dibujar(pantalla, nodo.der, rect_der, profundidad + 1)



