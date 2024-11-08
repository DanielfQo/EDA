import pygame
import math

radio = 5
ancho_linea = 1

class Punto:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dibujar(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), radio)

class Rectangulo:
    def __init__(self, x, y, ancho, alto):
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto

    def contiene(self, punto):

        return (self.x <= punto.x <= self.x + self.ancho and
                self.y <= punto.y <= self.y + self.alto)
    
    def contiene_circulo(self, circulo):
        x = circulo.x
        y = circulo.y
        radio = circulo.radio

        x1 = self.x
        y1 = self.y
        x2 = self.x + self.ancho
        y2 = self.y + self.alto

        x = max(x1, min(x, x2))
        y = max(y1, min(y, y2))

        distancia = math.sqrt((x - circulo.x) ** 2 + (y - circulo.y) ** 2)

        return distancia < radio


class Circulo:
    def __init__(self, x, y, radio):
        self.x = x
        self.y = y
        self.radio = radio

    def contiene_punto(self, punto):
        x = punto.x
        y = punto.y

        distancia = math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

        return distancia < self.radio

    def dibujar(self, screen):
        surface = pygame.Surface((self.radio * 2, self.radio * 2), pygame.SRCALPHA)
        pygame.draw.circle(surface, (0, 255, 0, 128), (self.radio, self.radio), self.radio)
        screen.blit(surface, (self.x - self.radio, self.y - self.radio))

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
        if self.punto is not None:
            self.punto.dibujar(screen)
        
        pygame.draw.rect(screen, (255, 255, 255), 
                        (self.limite.x, self.limite.y, self.limite.ancho, self.limite.alto), ancho_linea)
        
        if self.noroeste is not None:
            self.noroeste.dibujar(screen)

        if self.noreste is not None:
            self.noreste.dibujar(screen)

        if self.suroeste is not None:
            self.suroeste.dibujar(screen)

        if self.sureste is not None:
            self.sureste.dibujar(screen)
    
    def buscar(self, punto):
        if self.limite.contiene(punto):
            if self.punto is not None:
                if self.punto.x == punto.x and self.punto.y == punto.y:
                    return True
            else:
                if self.noreste.buscar(punto): return True
                elif self.noroeste.buscar(punto): return True
                elif self.sureste.buscar(punto): return True
                elif self.suroeste.buscar(punto): return True
                else: return False
        return False
    
    def buscar_por_rango(self, circulo):
        puntos = []
        if self.limite.contiene_circulo(circulo):
            if self.punto is not None:
                if circulo.contiene_punto(self.punto):
                    puntos.append(self.punto)
            if self.dividido:
                puntos.extend(self.noreste.buscar_por_rango(circulo))
                puntos.extend(self.noroeste.buscar_por_rango(circulo))
                puntos.extend(self.sureste.buscar_por_rango(circulo))
                puntos.extend(self.suroeste.buscar_por_rango(circulo))

        return puntos