import pygame
import random

pygame.init()

FPS = 100

FIELD_size_x = 2000
FIELD_size_y = 1000

WIN_size_x = 700
WIN_size_y = 700

CAM_SPEED = 600 // FPS
cam_pos_x = 0
cam_pos_y = 0

ZOOM_SPEED = 1 / FPS
multiply = 4

CELL_size = 50
CELL_DELAY = 0

sc = pygame.display.set_mode((WIN_size_x, WIN_size_y))
sc.fill((255, 255, 240))

clock = pygame.time.Clock()
repeat = 0
need = FPS // 2
need = int(need)

start = False
game_map_width = 50
game_map_height = 50
game_map = []
for i in range(game_map_height):
    game_map.append([])
    for x in range(game_map_width):
        game_map[i].append("b" if i == 0 or i == game_map_height - 1 or x == 0 or x == game_map_width - 1 else 0)
COLORS = {
    0: (246, 249, 255),  # Standart
    1: (143, 177, 65),  # Colored
    "b": (178, 2, 47),  # border
}
while True:
    sc.fill((53, 54, 46))
    x, y = 0, 0
    for line in game_map:
        x = 0
        for cell in line:
            pygame.draw.rect(sc, COLORS[cell],
                             (x - cam_pos_x, y - cam_pos_y, CELL_size // multiply - CELL_DELAY,
                              CELL_size // multiply - CELL_DELAY))
            x += CELL_size // multiply
        y += CELL_size // multiply
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
    mouse_button = pygame.mouse.get_pressed(3)
    if mouse_button[0]:
        x, y = pygame.mouse.get_pos()
        x = int((x + cam_pos_x) // (CELL_size // multiply))
        y = int((y + cam_pos_y) // (CELL_size // multiply))
        try:
            game_map[y][x] = 1 if game_map[y][x] != "b" else "b"
        except IndexError:
            pass
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        cam_pos_x += CAM_SPEED
    if keys[pygame.K_LEFT]:
        cam_pos_x -= CAM_SPEED
    if keys[pygame.K_UP]:
        cam_pos_y -= CAM_SPEED
    if keys[pygame.K_DOWN]:
        cam_pos_y += CAM_SPEED
    if keys[pygame.K_s]:
        multiply += ZOOM_SPEED
    if keys[pygame.K_w]:
        multiply -= ZOOM_SPEED
    if keys[pygame.K_SPACE]:
        start = False
        if keys[pygame.K_LCTRL]:
            for i in range(len(game_map)):
                for cell in range(len(game_map[i])):
                    game_map[i][cell] = random.choice([0, 1, 0]) if game_map[i][cell] != "b" else "b"
        else:
            x, y = pygame.mouse.get_pos()
            x = int((x + cam_pos_x) // (CELL_size // multiply))
            y = int((y + cam_pos_y) // (CELL_size // multiply))
            try:
                game_map[y][x] = 0 if game_map[y][x] != "b" else "b"
            except IndexError:
                pass
    if keys[pygame.K_1]:
        start = True
    if keys[pygame.K_2]:
        start = False
    if keys[pygame.K_3]:
        start = False
        game_map = [[0 if j != 'b' else 'b' for j in i] for i in game_map]
    if start:
        repeat += 1
    if start and need == repeat:
        repeat = 0
        new_map = [list(lis) for lis in game_map]
        for line in range(len(game_map)):
            for cell in range(len(game_map[line])):
                if game_map[line][cell] == "b":
                    continue
                cell_sum = 0
                for cur_cell in (
                        game_map[line - 1][cell - 1],
                        game_map[line - 1][cell],
                        game_map[line - 1][cell + 1],
                        game_map[line][cell - 1],
                        game_map[line][cell + 1],
                        game_map[line + 1][cell - 1],
                        game_map[line + 1][cell],
                        game_map[line + 1][cell + 1],):
                    if cur_cell != "b":
                        cell_sum += cur_cell
                if game_map[line][cell] == 0 and cell_sum == 3:
                    new_map[line][cell] = 1
                elif game_map[line][cell] == 1 and (cell_sum == 2 or cell_sum == 3):
                    new_map[line][cell] = 1
                else:
                    new_map[line][cell] = 0
        game_map = [list(lis) for lis in new_map]

    clock.tick(FPS)
    pygame.display.update()
