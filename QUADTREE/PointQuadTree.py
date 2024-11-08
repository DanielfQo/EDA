import pygame
import math

radio = 3
ancho_linea = 1

class Punto:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dibujar(self, screen):
        pygame.draw.circle(screen, (0, 0, 255), (self.x, self.y), radio)

class Rectangulo:
    def __init__(self, x, y, ancho, alto):
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto

    def contiene(self, punto):

        return (self.x <= punto.x <= self.x + self.ancho and
                self.y <= punto.y <= self.y + self.alto)


class PointQuadTree:
    def __init__(self, limite):
        self.noroeste = None
        self.noreste = None
        self.sureste = None
        self.suroeste = None

        self.limite = limite
        
        self.punto = None
        self.dividido = False

    def subdividir(self, punto):
        x = punto.x
        y = punto.y

        inicio_x = self.limite.x
        inicio_y = self.limite.y

        ancho = self.limite.ancho
        alto = self.limite.alto

        noroeste = Rectangulo(inicio_x, inicio_y, (x - inicio_x),           (y - inicio_y)) #
        noreste = Rectangulo(x, inicio_y,         (ancho - (x - inicio_x)), (y - inicio_y))
        suroeste = Rectangulo(inicio_x, y,        (x - inicio_x),              (alto - ( y - inicio_y))) #
        sureste = Rectangulo(x, y,                (ancho - (x - inicio_x)), (alto - ( y - inicio_y)))

        

        self.noroeste = PointQuadTree(noroeste)
        self.noreste = PointQuadTree(noreste)
        self.suroeste = PointQuadTree(suroeste)
        self.sureste = PointQuadTree(sureste)

        self.dividido = True

    def insertar(self, punto):
        if self.limite.contiene(punto):
            if self.punto is None:
                self.punto = punto
                self.subdividir(punto)
                return True    
            
            if self.noreste.insertar(punto): return True
            elif self.noroeste.insertar(punto): return True
            elif self.sureste.insertar(punto): return True
            elif self.suroeste.insertar(punto): return True
            else : return False

        return False

    def dibujar(self, screen):

        pygame.draw.rect(screen, (255, 255, 255), 
                        (self.limite.x, self.limite.y, self.limite.ancho, self.limite.alto), ancho_linea)

        if self.punto is not None:
            self.punto.dibujar(screen)
        
        if self.noroeste is not None:
            self.noroeste.dibujar(screen)

        if self.noreste is not None:
            self.noreste.dibujar(screen)

        if self.suroeste is not None:
            self.suroeste.dibujar(screen)

        if self.sureste is not None:
            self.sureste.dibujar(screen)

    def imprimir_arbol(self):
        if self.dividido:
            print("Noroeste: ", self.noroeste.limite.x, self.noroeste.limite.y, self.noroeste.limite.ancho , self.noroeste.limite.alto)
            self.noroeste.imprimir_arbol()

            print("Noreste: ", self.noreste.limite.x, self.noreste.limite.y, self.noreste.limite.ancho , self.noreste.limite.alto)
            self.noreste.imprimir_arbol()

            print("Suroeste: ", self.suroeste.limite.x, self.suroeste.limite.y, self.suroeste.limite.ancho , self.suroeste.limite.alto)
            self.suroeste.imprimir_arbol()

            print("Sureste: ", self.sureste.limite.x, self.sureste.limite.y, self.sureste.limite.ancho , self.sureste.limite.alto)
            self.sureste.imprimir_arbol()