import pygame as pg
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import csv
import math

# Colores para la visualización
COLOR_FONDO = (255, 255, 255)
COLOR_NODO = (0, 0, 255)
COLOR_DIVISION = (255, 0, 0)

class Nodo:
    def __init__(self, valor, izq=None, der=None):
        self.valor = valor
        self.izq = izq
        self.der = der

class KDTREE:
    def __init__(self, dimension=2):
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

    def buscar(self, valor):
        if len(valor) != self.dimension:
            raise ValueError(f"El valor debe tener {self.dimension} coordenadas.")
        return self._buscar_recursivo(self.raiz, valor, 0)

    def _buscar_recursivo(self, nodo, valor, profundidad):
        if nodo is None:
            return False
        if nodo.valor == valor:
            return True

        eje = profundidad % self.dimension
        if valor[eje] < nodo.valor[eje]:
            return self._buscar_recursivo(nodo.izq, valor, profundidad + 1)
        else:
            return self._buscar_recursivo(nodo.der, valor, profundidad + 1)
        
    def calcular_distancia(self, p1, p2):
        """Calcula la distancia euclidiana entre dos puntos."""
        return math.sqrt(sum((p1[i] - p2[i]) ** 2 for i in range(len(p1))))

    def k_vecinos_mas_proximos(self, punto, k):
        """Devuelve los k vecinos más cercanos al punto dado."""
        if len(punto) != self.dimension:
            raise ValueError(f"El punto debe tener {self.dimension} coordenadas.")
        vecinos = []
        self._k_vecinos_recursivo(self.raiz, punto, k, 0, vecinos)
        return sorted(vecinos, key=lambda x: x[0])[:k]

    def _k_vecinos_recursivo(self, nodo, punto, k, profundidad, vecinos):
        if nodo is None:
            return

        distancia = self.calcular_distancia(nodo.valor, punto)

        if len(vecinos) < k:
            vecinos.append((distancia, nodo.valor))
        else:
            vecinos.sort()
            if distancia < vecinos[-1][0]:
                vecinos[-1] = (distancia, nodo.valor)

        eje = profundidad % self.dimension
        if punto[eje] < nodo.valor[eje]:
            self._k_vecinos_recursivo(nodo.izq, punto, k, profundidad + 1, vecinos)
            if len(vecinos) < k or abs(punto[eje] - nodo.valor[eje]) < vecinos[-1][0]:
                self._k_vecinos_recursivo(nodo.der, punto, k, profundidad + 1, vecinos)
        else:
            self._k_vecinos_recursivo(nodo.der, punto, k, profundidad + 1, vecinos)
            if len(vecinos) < k or abs(punto[eje] - nodo.valor[eje]) < vecinos[-1][0]:
                self._k_vecinos_recursivo(nodo.izq, punto, k, profundidad + 1, vecinos)

    def cargar_desde_csv(self, nombre_archivo):
        with open(nombre_archivo, 'r') as archivo_csv:
            lector_csv = csv.reader(archivo_csv)
            for fila in lector_csv:
                punto = tuple(map(int, fila))
                self.insertar(punto)

    def dibujar_3d(self):
        if self.dimension != 3:
            raise NotImplementedError("La visualizacion 3D solo esta implementada para KDTrees de 3 dimensiones.")
        self._dibujar_recursivo_3d(self.raiz)

    def _dibujar_recursivo_3d(self, nodo):
        if nodo is not None:
            glPushMatrix()
            glTranslatef(*nodo.valor)
            self._dibujar_esfera()
            glPopMatrix()

            if nodo.izq:
                self._dibujar_linea(nodo.valor, nodo.izq.valor)
                self._dibujar_recursivo_3d(nodo.izq)
            if nodo.der:
                self._dibujar_linea(nodo.valor, nodo.der.valor)
                self._dibujar_recursivo_3d(nodo.der)

    def _dibujar_linea(self, inicio, fin):
        glBegin(GL_LINES)
        glVertex3fv(inicio)
        glVertex3fv(fin)
        glEnd()

    def _dibujar_esfera(self):
        glColor3f(1.0, 0.5, 0.0)  
        glutSolidSphere(1, 10, 10)
        glColor3f(1.0, 1.0, 1.0)  

    def iniciar_opengl(self):
        pg.init()
        
        pg.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
        glutInit()
        gluPerspective(45, (800 / 600), 0.1, 5000.0)
        glTranslatef(0.0, 0.0, -20)

    def dibujar_ejes(self):
        glBegin(GL_LINES)
        glColor3f(1, 0, 0)
        glVertex3f(-1000, 0, 0)
        glVertex3f(1000, 0, 0)
        glColor3f(0, 1, 0)
        glVertex3f(0, -1000, 0)
        glVertex3f(0, 1000, 0)
        glColor3f(0, 0, 1)
        glVertex3f(0, 0, -1000)
        glVertex3f(0, 0, 1000)
        glEnd()
        glColor3f(1, 1, 1)

    def visualizar_3d(self):
        self.iniciar_opengl()

        angulo_x, angulo_y = 0, 0
        distancia_z = -100
        mouse_presionado = False
        last_mouse_pos = (0, 0)

        while True:
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    return
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_presionado = True
                        last_mouse_pos = pg.mouse.get_pos()
                elif event.type == MOUSEBUTTONUP:
                    if event.button == 1:
                        mouse_presionado = False
                elif event.type == MOUSEMOTION and mouse_presionado:
                    mouse_x, mouse_y = pg.mouse.get_pos()
                    dx = mouse_x - last_mouse_pos[0]
                    dy = mouse_y - last_mouse_pos[1]
                    angulo_x += dy * 0.1
                    angulo_y += dx * 0.1
                    last_mouse_pos = (mouse_x, mouse_y)
                elif event.type == MOUSEWHEEL:
                    distancia_z += event.y * 10

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glPushMatrix()
            glTranslatef(0.0, 0.0, distancia_z)
            glRotatef(angulo_x, 1, 0, 0)
            glRotatef(angulo_y, 0, 1, 0)

            self.dibujar_ejes()
            self.dibujar_3d()

            glPopMatrix()
            pg.display.flip()
            pg.time.wait(10)

    def dibujar_2d(self, pantalla, nodo=None, rect=None, profundidad=0):
        if self.dimension != 2:
            raise NotImplementedError("La visualización 2D solo está implementada para KDTrees de 2 dimensiones.")

        ancho, alto = pantalla.get_size()
        if nodo is None:
            nodo = self.raiz
            rect = (0, 0, ancho, alto)

        if nodo is None:
            return

        x, y = nodo.valor[:2]
        eje = profundidad % 2

        if eje == 0:
            pg.draw.line(pantalla, COLOR_DIVISION, (x, rect[1]), (x, rect[1] + rect[3]), 1)
            rect_izq = (rect[0], rect[1], x - rect[0], rect[3])
            rect_der = (x, rect[1], rect[2] - (x - rect[0]), rect[3])
        else: 
            pg.draw.line(pantalla, COLOR_DIVISION, (rect[0], y), (rect[0] + rect[2], y), 1)
            rect_izq = (rect[0], rect[1], rect[2], y - rect[1])
            rect_der = (rect[0], y, rect[2], rect[3] - (y - rect[1]))

        pg.draw.circle(pantalla, COLOR_NODO, (x, y), 5)

        if nodo.izq is not None:
            self.dibujar_2d(pantalla, nodo.izq, rect_izq, profundidad + 1)
        if nodo.der is not None:
            self.dibujar_2d(pantalla, nodo.der, rect_der, profundidad + 1)

    def visualizacion_2d(self):
        pg.init()
        pantalla = pg.display.set_mode((800, 600))
        pg.display.set_caption("Visualización 2D del KDTree")
        corriendo = True

        while corriendo:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    corriendo = False
                elif evento.type == pg.MOUSEBUTTONDOWN and evento.button == 1:
                    x, y = evento.pos
                    self.insertar((x, y))
                    print(f"Insertado nodo en: ({x}, {y})")

            pantalla.fill(COLOR_FONDO)
            self.dibujar_2d(pantalla)
            pg.display.flip()

        pg.quit()


