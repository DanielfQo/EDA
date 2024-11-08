import pygame
import sys
from PointQuadTree import PointQuadTree, Rectangulo, Punto, Circulo
import random

ancho = 1024
alto = 720

pygame.init()
screen = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Visualización QuadTree")

limite = Rectangulo(0, 0, ancho, alto)
quadtree = PointQuadTree(limite)

random.seed(42)
for _ in range(50):
    x = random.randint(0, ancho)
    y = random.randint(0, alto)
    punto = Punto(x, y)
    quadtree.insertar(punto)

corriendo = True
presionado = False
mouse_pos = (0, 0)

while corriendo:
    screen.fill((0, 0, 0)) 
    quadtree.dibujar(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            corriendo = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3: 
                presionado = True
                mouse_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:  
                presionado = False
        elif event.type == pygame.MOUSEMOTION:
            if presionado:
                mouse_pos = event.pos

    if presionado:
        rango = Circulo(mouse_pos[0], mouse_pos[1], 200)
        rango.dibujar(screen)
        puntos = quadtree.buscar_por_rango(rango)
        for punto in puntos:
            pygame.draw.circle(screen, (0, 0, 255), (punto.x, punto.y), 5)

    pygame.display.flip()

pygame.quit()
