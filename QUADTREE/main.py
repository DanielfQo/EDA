import pygame
import sys
from PointQuadTree import PointQuadTree, Rectangulo, Punto, Circulo
import random
import subprocess

def generar_dot(quadtree, nombre_archivo="quadtree.dot"):
    with open(nombre_archivo, "w") as archivo:
        archivo.write("digraph PointQuadTree {\n")
        archivo.write("    node [shape=circle];\n")
        
        def agregar_nodos(quadtree, parent_id=None):
            if quadtree is None or quadtree.limite is None:
                return

            nodo_id = f"{id(quadtree)}"
            
            etiqueta = f"({quadtree.limite.x},{quadtree.limite.y})\\n{quadtree.limite.ancho}x{quadtree.limite.alto}"
            if quadtree.punto:
                etiqueta += f"\\nPunto: ({quadtree.punto.x}, {quadtree.punto.y})"

            archivo.write(f'    {nodo_id} [label="{etiqueta}"];\n')
            
            if parent_id:
                archivo.write(f"    {parent_id} -> {nodo_id};\n")
            
            if quadtree.dividido:
                agregar_nodos(quadtree.noroeste, nodo_id)
                agregar_nodos(quadtree.noreste, nodo_id)
                agregar_nodos(quadtree.suroeste, nodo_id)
                agregar_nodos(quadtree.sureste, nodo_id)
    
        agregar_nodos(quadtree)
        archivo.write("}\n")

    subprocess.run(["dot", "-Tpng", nombre_archivo, "-o", "quadtree.png"])


ancho = 1024
alto = 720
PUNTOSGENERADOS = 50

pygame.init()
screen = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Visualización QuadTree")

limite = Rectangulo(0, 0, ancho, alto)
quadtree = PointQuadTree(limite)

random.seed(pygame.time.get_ticks())
for _ in range(PUNTOSGENERADOS):
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

#Debe estar instalado graphviz
generar_dot(quadtree)

