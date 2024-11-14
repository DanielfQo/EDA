import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


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
        dimension = profundidad % 3
        if valor[dimension] < nodo.valor[dimension]:
            if nodo.izq is None:
                nodo.izq = Nodo(valor)
            else:
                self._insertar_recursivo(nodo.izq, valor, profundidad + 1)
        else:
            if nodo.der is None:
                nodo.der = Nodo(valor)
            else:
                self._insertar_recursivo(nodo.der, valor, profundidad + 1)

    def dibujar(self):
        self._dibujar_recursivo(self.raiz)

    def _dibujar_recursivo(self, nodo):
        if nodo is not None:
            # Dibuja el nodo actual
            glPushMatrix()
            glTranslatef(*nodo.valor)  # Posiciona en el espacio 3D
            self.dibujar_esfera()
            glPopMatrix()

            # Dibuja conexiones hacia hijos
            if nodo.izq:
                self._dibujar_linea(nodo.valor, nodo.izq.valor)
                self._dibujar_recursivo(nodo.izq)
            if nodo.der:
                self._dibujar_linea(nodo.valor, nodo.der.valor)
                self._dibujar_recursivo(nodo.der)

    def _dibujar_linea(self, inicio, fin):
        glBegin(GL_LINES)
        glVertex3fv(inicio)
        glVertex3fv(fin)
        glEnd()

    def dibujar_esfera(self):
        glutSolidSphere(0.1, 10, 10)  # Tamaño y resolución de la esfera

def iniciar_opengl():
    pygame.init()
    pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
    gluPerspective(45, (800 / 600), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -10)

def visualizar_kdtree():
    arbol = KDTREE()
    puntos = [(1, 2, 3), (4, 5, 6), (7, 8, 1), (3, 7, 5)]
    for punto in puntos:
        arbol.insertar(punto)

    iniciar_opengl()
    angulo_rotacion = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        glRotatef(angulo_rotacion, 0, 1, 0)  # Rota el árbol

        arbol.dibujar()
        glPopMatrix()

        angulo_rotacion += 0.5  # Cambia el ángulo de rotación
        pygame.display.flip()
        pygame.time.wait(10)

visualizar_kdtree()
