import pygame
import sys
from PointQuadTree import PointQuadTree, Rectangulo, Punto

"""
pygame.init()
screen = pygame.display.set_mode((512, 512))
pygame.display.set_caption("Visualización QuadTree")

limite = Rectangulo(0, 0, 800, 600)
quadtree = PointQuadTree(limite)


corriendo = True
while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            x, y = evento.pos
            punto = Punto(x, y)
            quadtree.insertar(punto)
            print("Punto insertado en: ", x, y)
            quadtree.imprimir_arbol()

    screen.fill((0, 0, 0)) 
    quadtree.dibujar(screen)
    pygame.display.flip()

pygame.quit()
"""


limite = Rectangulo(0, 0, 64, 64)
quadtree = PointQuadTree(limite)

punto = Punto(32, 32)
quadtree.insertar(punto)
quadtree.imprimir_arbol()
print("")
punto = Punto(16, 16)
quadtree.insertar(punto)
quadtree.imprimir_arbol()
