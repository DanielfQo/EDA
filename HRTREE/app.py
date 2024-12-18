import pygame as pg
import random
import hrtree as hrt

pg.init()

WIDTH, HEIGHT = 1200, 800
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Visualización de HRTREE")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

SQUARE_SIZE = 50
BUTTON_WIDTH, BUTTON_HEIGHT = 100, 50
BUTTON_X, BUTTON_Y = WIDTH - 150, HEIGHT - 100

widthR = 300
heightR = 175

rectangles = [
    pg.Rect(100, 50, widthR, heightR),
    pg.Rect(800, 50, widthR, heightR),
    pg.Rect(450, 325, widthR, heightR),
    pg.Rect(100, 600, widthR, heightR),
    pg.Rect(800, 600, widthR, heightR)
]

squaresSobrepuestos = []

def generate_random_squares(count, width, height, rectangulos=rectangles):
    squares = []
    for _ in range(count):
        x = random.randint(0, width - SQUARE_SIZE)
        y = random.randint(0, height - SQUARE_SIZE)
        nuevo = pg.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE)
        squares.append(nuevo)
        for rect in rectangulos:
            if rect.colliderect(nuevo):
                squaresSobrepuestos.append(nuevo)

    return squares

square_count = 10
squares = generate_random_squares(square_count, WIDTH, HEIGHT)

running = True
hrtree = hrt.HRTree()

# Variables para el rectángulo de selección
selecting = False
start_pos = None
end_pos = None
selection_rect = None

# Lista para los cuadrados resultado del query
queried_squares = []

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            # Verificar si se presiona el botón "Next"
            if BUTTON_X <= mouse_x <= BUTTON_X + BUTTON_WIDTH and BUTTON_Y <= mouse_y <= BUTTON_Y + BUTTON_HEIGHT:
                squares = generate_random_squares(square_count, WIDTH, HEIGHT)
                if squaresSobrepuestos:
                    hrtree.create_new_version()
                    for square in squaresSobrepuestos:
                        x1, y1, x2, y2 = square.topleft[0], square.topleft[1], square.bottomright[0], square.bottomright[1]
                        mbr = ((x1, y1), (x2, y2))
                        hrtree.insert(mbr)

                    squaresSobrepuestos.clear()

                    print("Estado después de la nueva versión:", hrtree.query(((0, 0), (WIDTH, HEIGHT))))
            else:
                # Inicio del rectángulo de selección
                selecting = True
                start_pos = event.pos
        elif event.type == pg.MOUSEBUTTONUP:
            # Fin del rectángulo de selección
            if selecting:
                selecting = False
                end_pos = event.pos
                # Crear el rectángulo de selección final
                x1, y1 = start_pos
                x2, y2 = end_pos
                selection_rect = pg.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))

                # Realizar el query en el área seleccionada
                if selection_rect:
                    mbr_query = ((selection_rect.left, selection_rect.top),
                                 (selection_rect.right, selection_rect.bottom))
                    resultado = hrtree.query(mbr_query)
                    print("Resultado del query en el área seleccionada:", resultado)

                    # Actualizar la lista de cuadrados resultado del query
                    queried_squares = [
                        pg.Rect(mbr[0][0], mbr[0][1], mbr[1][0] - mbr[0][0], mbr[1][1] - mbr[0][1])
                        for mbr in resultado
                    ]

        elif event.type == pg.MOUSEMOTION:
            # Actualizar el rectángulo de selección mientras se arrastra el mouse
            if selecting:
                x1, y1 = start_pos
                x2, y2 = event.pos
                selection_rect = pg.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))

    screen.fill(WHITE)

    # Dibujar los cuadrados
    for square in squares:
        pg.draw.rect(screen, RED, square)

    # Dibujar los rectángulos predefinidos
    for rect in rectangles:
        pg.draw.rect(screen, BLACK, rect, 2)

    # Dibujar el botón "Next"
    pg.draw.rect(screen, GRAY, (BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT))
    font = pg.font.Font(None, 36)
    text = font.render("Next", True, BLACK)
    text_rect = text.get_rect(center=(BUTTON_X + BUTTON_WIDTH // 2, BUTTON_Y + BUTTON_HEIGHT // 2))
    screen.blit(text, text_rect)

    # Dibujar el rectángulo de selección
    if selecting and selection_rect:
        pg.draw.rect(screen, BLUE, selection_rect, 2)

    # Dibujar los cuadrados resultado del query
    for queried_square in queried_squares:
        pg.draw.rect(screen, GREEN, queried_square)

    pg.display.flip()

pg.quit()

full_visualizer = hrt.HRTreeFullVisualizer(hrtree)
full_visualizer.draw_full_history()
