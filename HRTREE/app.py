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

def generate_random_squares(count, width, height, rectangulos = rectangles):
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

while running:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if BUTTON_X <= mouse_x <= BUTTON_X + BUTTON_WIDTH and BUTTON_Y <= mouse_y <= BUTTON_Y + BUTTON_HEIGHT:
                squares = generate_random_squares(square_count, WIDTH, HEIGHT)
                if(squaresSobrepuestos != []):
                    hrtree.create_new_version()
                    for square in squaresSobrepuestos:
                        x1, y1, x2, y2 = square.topleft[0], square.topleft[1], square.bottomright[0], square.bottomright[1]
                        mbr = ((x1, y1), (x2, y2))
                        hrtree.insert(mbr)

                    squaresSobrepuestos.clear()
                    
                    print("Estado después de la nueva versión:", hrtree.query(((0, 0), (WIDTH, HEIGHT))))


    screen.fill(WHITE)

    for square in squares:
        pg.draw.rect(screen, RED, square)

    for rect in rectangles:
        pg.draw.rect(screen, BLACK, rect, 2)

    pg.draw.rect(screen, GRAY, (BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT))
    font = pg.font.Font(None, 36)
    text = font.render("Next", True, BLACK)
    text_rect = text.get_rect(center=(BUTTON_X + BUTTON_WIDTH // 2, BUTTON_Y + BUTTON_HEIGHT // 2))
    screen.blit(text, text_rect)

    

    pg.display.flip()

pg.quit()

