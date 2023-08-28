import random

import pygame

# PYGAME ====================

pygame.init()

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 640

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption('Minesweeper')

clock = pygame.time.Clock()

# GAME ====================

BOARD_WIDTH = 20
BOARD_HEIGHT = 20

TILE_WIDTH = int(SCREEN_WIDTH / BOARD_WIDTH)
TILE_HEIGHT = int(SCREEN_HEIGHT / BOARD_HEIGHT)

BOMBS = (BOARD_WIDTH + BOARD_HEIGHT) * 2 - random.randint(0, BOARD_HEIGHT)

boardvals = []

covered = []  # 0 - not covered, 1 - covered, 2 - flag

bomb_pos = []

mines_left = BOMBS

first = True

myfont = pygame.font.SysFont('verdana', 24)

l_click = False
r_click = False

game_over = False

# COLORS ====================

val_colours = (
    (162, 209, 73), (25, 118, 210), (56, 142, 60), (211, 47, 47), (123, 31, 162), (255, 143, 0), (85, 55, 57),
    (78, 205, 196), (198, 15, 123), (23, 23, 23))

flag = (242, 54, 7)

bg_colours = ((162, 209, 73), (170, 215, 81), (229, 194, 159), (215, 184, 153))

border = (135, 175, 58)

# SCREEN-SHAKE
screen_shake_intensity = 0.4
screen_shake_t = 0


def num_of_bombs_around(x, y):
    count = 0
    for bomb in bomb_pos:
        if abs(y - bomb[0]) <= 1 and abs(x - bomb[1]) <= 1: count += 1
    return count


def uncover(x, y):
    if x < 0 or x >= BOARD_WIDTH or y < 0 or y >= BOARD_HEIGHT or covered[y][x] in (0, 2):
        return
    covered[y][x] = 0

    if boardvals[y][x] == 9:  # If bomb uncovered
        game_over = True

        for bomb in bomb_pos:
            covered[bomb[0]][bomb[1]] = 0  # uncover all bombs

    if boardvals[y][x] == 0:
        uncover(x + 1, y)
        uncover(x, y + 1)
        uncover(x - 1, y)
        uncover(x, y - 1)

        uncover(x + 1, y + 1)
        uncover(x - 1, y + 1)
        uncover(x + 1, y - 1)
        uncover(x - 1, y - 1)


def number_uncover(x, y):
    if boardvals[y][x] in (0, 9):
        return

    uncover(x + 1, y)
    uncover(x, y + 1)
    uncover(x - 1, y)
    uncover(x, y - 1)

    uncover(x + 1, y + 1)
    uncover(x - 1, y + 1)
    uncover(x + 1, y - 1)
    uncover(x - 1, y - 1)


def is_bomb(x, y):
    count = 0
    for bomb in bomb_pos:
        if bomb[0] == y and bomb[1] == x:
            return True
    return False


def set_board(fx, fy):
    global boardvals, bomb_pos, mines_left

    boardvals = []
    bomb_pos = []

    # PLACE BOMBS
    for bomb in range(BOMBS):
        # boardvals[random.randint(0,BOARD_HEIGHT-1)][random.randint(0,BOARD_WIDTH-1)] = 9

        while True:

            bomb_x = random.randint(0, BOARD_WIDTH - 1)
            bomb_y = random.randint(0, BOARD_HEIGHT - 1)

            if not is_bomb(bomb_x, bomb_y) and not (abs(fy - bomb_y) <= 1 and abs(fx - bomb_x) <= 1):
                break

        bomb_pos.append((bomb_y, bomb_x))

    for row in range(BOARD_HEIGHT):
        boardvals.append([])
        for col in range(BOARD_WIDTH):
            bombs = num_of_bombs_around(col, row)
            if is_bomb(col, row): bombs = 9
            boardvals[row].append(bombs)

    mines_left = BOMBS


def cover_all():
    global covered
    covered = []

    clonerow = [1] * BOARD_WIDTH
    for i in range(BOARD_HEIGHT):
        covered.append(clonerow.copy())


def is_covered(x, y):
    if x < 0 or x >= BOARD_WIDTH or y < 0 or y >= BOARD_HEIGHT:
        return 1
    return covered[y][x]


cover_all()
# set_board(0,0)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                first = True
                cover_all()

    l_mouse_down = pygame.mouse.get_pressed()[0]
    r_mouse_down = pygame.mouse.get_pressed()[2]

    if pygame.mouse.get_focused() == 1 and not game_over:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        tile_row = int(mouse_y // TILE_HEIGHT)
        tile_column = int(mouse_x // TILE_WIDTH)

        if (l_mouse_down and not l_click) and (r_mouse_down and not r_click) and not first:
            number_uncover(tile_column, tile_row)

        if l_mouse_down:
            if l_click:
                if first:
                    set_board(tile_column, tile_row)
                    first = False

                uncover(tile_column, tile_row)

                screen_shake_t = int(clock.get_fps() * 0.2)
            l_click = False
        else:
            l_click = True

        if r_mouse_down:
            if r_click:
                if covered[tile_row][tile_column] != 0 and not first:
                    if covered[tile_row][tile_column] == 2:
                        covered[tile_row][tile_column] = 1
                    else:
                        covered[tile_row][tile_column] = 2
                        mines_left -= 1
            r_click = False
        else:
            r_click = True

    screen.fill(val_colours[0])

    counter = 0

    for row in range(BOARD_HEIGHT):
        for column in range(BOARD_WIDTH):
            lx = column * TILE_WIDTH
            uy = row * TILE_HEIGHT

            bg_rect = (lx, uy, TILE_WIDTH, TILE_HEIGHT)

            if covered[row][column] == 0:
                pygame.draw.rect(screen, bg_colours[2] if counter % 2 == 0 else bg_colours[3], bg_rect)

                # Number
                val = boardvals[row][column]
                if val != 0:
                    textsurface = myfont.render(str(val) if val != 9 else '#', True, val_colours[val])

                    piece_pos = (column * TILE_WIDTH + int((TILE_WIDTH - textsurface.get_width()) / 2),
                                 row * TILE_HEIGHT + int((TILE_HEIGHT - textsurface.get_height()) / 2))

                    screen.blit(textsurface, piece_pos)

                '''# Border
 
                rx = lx + TILE_WIDTH
                by = uy + TILE_HEIGHT
 
                if is_covered(column, row - 1): pygame.draw.line(screen, border, (lx, uy), (rx, uy), 6)
                if is_covered(column, row + 1): pygame.draw.line(screen, border, (lx, by), (rx, by), 6)
                if is_covered(column - 1, row): pygame.draw.line(screen, border, (lx, uy), (lx, by), 6)
                if is_covered(column + 1, row): pygame.draw.line(screen, border, (rx, uy), (rx, by), 6)'''

            else:

                pygame.draw.rect(screen, bg_colours[0] if counter % 2 == 0 else bg_colours[1], bg_rect)

                # pygame.draw.rect(screen, button,
                #                  (column * TILE_WIDTH + 1, row * TILE_HEIGHT + 1, TILE_WIDTH - 2, TILE_HEIGHT - 2))

                if covered[row][column] == 2:
                    textsurface = myfont.render('F', True, flag)

                    piece_pos = (lx + int((TILE_WIDTH - textsurface.get_width()) / 2),
                                 uy + int((TILE_HEIGHT - textsurface.get_height()) / 2))

                    screen.blit(textsurface, piece_pos)

            counter += 1
        counter += 1

    # Border

    for row in range(BOARD_HEIGHT):
        for column in range(BOARD_WIDTH):
            if covered[row][column] == 0:
                lx = column * TILE_WIDTH
                uy = row * TILE_HEIGHT
                rx = lx + TILE_WIDTH
                by = uy + TILE_HEIGHT

                if is_covered(column, row - 1): pygame.draw.line(screen, border, (lx, uy), (rx, uy), 2)
                if is_covered(column, row + 1): pygame.draw.line(screen, border, (lx, by), (rx, by), 2)
                if is_covered(column - 1, row): pygame.draw.line(screen, border, (lx, uy), (lx, by), 2)
                if is_covered(column + 1, row): pygame.draw.line(screen, border, (rx, uy), (rx, by), 2)

    flag_icon = myfont.render('F', True, flag)
    textsurface = myfont.render(str(mines_left), True, (0, 0, 0))

    screen.blit(flag_icon, (SCREEN_WIDTH - 90, SCREEN_HEIGHT - 50))
    screen.blit(textsurface, (SCREEN_WIDTH - 70, SCREEN_HEIGHT - 50))

    if (screen_shake_t > 0):
        strength = int(screen_shake_t * screen_shake_intensity)

        screen.blit(screen, (random.randint(-strength, strength),
                             random.randint(-strength, strength)))

        screen_shake_t -= 1

    pygame.display.update()

    clock.tick(60)
