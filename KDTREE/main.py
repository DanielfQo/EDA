import TKDTREE as kd
import pygame as pg

arbol = kd.KDTREE()

pg.init()
screen = pg.display.set_mode((800, 600))
running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            arbol.insertar((x, y))
            print(f"Inserted node at: ({x}, {y})")

    screen.fill((255, 255, 255))
    arbol.dibujar(screen)
    pg.display.flip()
    

pg.quit()

