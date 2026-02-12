import copy
import pygame
import math

CELL_SIZE = 20
ALIVE_COLOR = [255, 0, 0]
ALIVE_OUTLINE = [180, 0, 0]
OUTLINE_THICKNESS = CELL_SIZE * 0.1
DEAD_COLOR = [100, 100, 100]
DEAD_OUTLINE = [50, 50, 50]
DARKENING_FACTOR = 1.1

pygame.init()


class Grid:
    def __init__(self, cols, rows, alive, dead):
        self.cols = cols
        self.rows = rows
        self.alive = alive
        self.dead = dead
        self.age = 0

    def genEmptyGrid(self):

        grid = []

        for i in range(self.rows):
            row = []

            for j in range(self.cols):
                row.append(arena.dead)

            grid.append(row)

        return grid

def printGrid(grid):
    for i in range(len(grid)):
        print('')

    for row in grid:
        print(' '.join(str(i) for i in row))

# class Simulation:
#     def __init__(self, grid):
#         self.grid = grid
#
#     def countliveneighbours(self, cell_x, cell_y):
#             count = 0
#
#             rows = len(self.grid)
#             cols = len(self.grid[0])
#
#             for i in [-1, 0, 1]:
#                 for j in [-1, 0, 1]:
#                     if self.grid[(cell_y + i) % rows][(cell_x + j) % cols] > arena.dead:
#                         count += 1
#
#             if self.grid[cell_y][cell_x] > arena.dead:
#                 count -= 1
#
#             return count

def countliveneighbours(grid, cell_x, cell_y):
    count = 0

    rows = len(grid)
    cols = len(grid[0])

    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if grid[(cell_y + i) % rows][(cell_x + j) % cols] > arena.dead:
                count += 1

    if grid[cell_y][cell_x] > arena.dead:
        count -= 1

    return count


# def countdeadneighbours(grid, x, y):
#     count = 0
#
#     rows = len(grid)
#     cols = len(grid[0])
#
#     for i in [-1, 0, 1]:
#         for j in [-1, 0, 1]:
#             if grid[(y + i) % rows][(x + j) % cols] == arena.dead:
#                 count += 1
#
#     if grid[y][x] == arena.dead:
#         count -= 1
#
#     return count


def step2(grid):
    rows = len(grid)
    cols = len(grid[0])

    new_grid = copy.deepcopy(grid)

    for y in range(rows):
        for x in range(cols):

            isAlive = grid[y][x] > arena.dead
            live_neighbours = countliveneighbours(grid, x, y)

            if isAlive:

                if live_neighbours == 2 or live_neighbours == 3:
                    new_grid[y][x] = grid[y][x] + 1

                else:
                    new_grid[y][x] = arena.dead

            else:

                if live_neighbours == 3:
                    new_grid[y][x] = arena.alive

                else:
                    new_grid[y][x] = arena.dead

            # if countLiveNeighbours(grid, x, y) == 2:
            #    new_grid[y][x] = arena.alive
            # else:
            #    new_grid[y][x] = arena.dead

    return new_grid


def displayGrid(grid):
    rows = len(grid)
    cols = len(grid[0])

    for i in range(rows):
        for j in range(cols):

            TOP = j * CELL_SIZE
            LEFT = i * CELL_SIZE
            WIDTH = CELL_SIZE
            HEIGHT = CELL_SIZE
            AGE = grid[i][j]
            DARKENING = DARKENING_FACTOR ** AGE

            if grid[i][j] > arena.dead:
                aged_color = [math.floor(ALIVE_COLOR[0] / DARKENING),
                              math.floor(ALIVE_COLOR[1] / DARKENING),
                              math.floor(ALIVE_COLOR[2] / DARKENING)]

                aged_outline_color = [math.floor(ALIVE_OUTLINE[0] / DARKENING),
                                      math.floor(ALIVE_OUTLINE[1] / DARKENING),
                                      math.floor(ALIVE_OUTLINE[2] / DARKENING)]

                pygame.draw.rect(screen, aged_outline_color, pygame.Rect(LEFT, TOP, WIDTH, HEIGHT))
                pygame.draw.rect(screen, aged_color,
                                 pygame.Rect(LEFT + OUTLINE_THICKNESS * 0.5, TOP + OUTLINE_THICKNESS * 0.5,
                                             WIDTH - OUTLINE_THICKNESS, HEIGHT - OUTLINE_THICKNESS))

            elif grid[i][j] == arena.dead:
                pygame.draw.rect(screen, DEAD_OUTLINE, pygame.Rect(LEFT, TOP, WIDTH, HEIGHT))
                pygame.draw.rect(screen, DEAD_COLOR,
                                 pygame.Rect(LEFT + OUTLINE_THICKNESS * 0.5, TOP + OUTLINE_THICKNESS * 0.5,
                                             WIDTH - OUTLINE_THICKNESS, HEIGHT - OUTLINE_THICKNESS))


def setCellAtPos(grid, state, x, y):
    cell_x = math.floor(x / CELL_SIZE)
    cell_y = math.floor(y / CELL_SIZE)

    grid[cell_x][cell_y] = state


arena = Grid(50, 50, 1, 0)

screen = pygame.display.set_mode((arena.cols * CELL_SIZE, arena.rows * CELL_SIZE))
pygame.display.set_caption("yep")

play = arena.genEmptyGrid()

printGrid(play)

# play[3][5] = arena.alive
# play[4][5] = arena.alive
# play[5][5] = arena.alive
# play[3][4] = arena.alive
printGrid(play)

# for i in range(30):
#     play = step2(play)
#     printGrid(play)
#     time.sleep(0.2)

running = True
playing = True
press_count = 0
while running:

    displayGrid(play)
    pygame.display.update()

    if playing:
        play = step2(play)
        pygame.time.wait(100)

    # displayGrid(play)
    # play = step2(play)

    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if press_count % 2 == 0:
                    playing = False
                else:
                    playing = True
                press_count += 1

        elif pygame.mouse.get_pressed():
            x, y = pygame.mouse.get_pos()

            if pygame.mouse.get_pressed()[0]:
                setCellAtPos(play, arena.alive, x, y)
            elif pygame.mouse.get_pressed()[2]:
                setCellAtPos(play, arena.dead, x, y)

        if event.type == pygame.QUIT:
            running = False

pygame.quit()
