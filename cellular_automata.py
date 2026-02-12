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
    def __init__(self, cols, rows):
        self.cols = cols
        self.rows = rows

    def genEmptyGrid(self):

        grid = []

        for i in range(self.rows):
            row = []

            for j in range(self.cols):
                row.append(0)

            grid.append(row)

        return grid
def printGrid(grid):
    for i in range(len(grid)):
        print('')

    for row in grid:
        print(' '.join(str(i) for i in row))

class Simulation:
    def __init__(self, gridArr, alive, dead):
        self.grid = gridArr
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        self.alive = 1
        self.dead = 0

    def countliveneighbours(self, cell_x, cell_y):
            count = 0

            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    if self.grid[(cell_y + i) % self.rows][(cell_x + j) % self.cols] > self.dead:
                        count += 1

            if self.grid[cell_y][cell_x] > self.dead:
                count -= 1

            return count

    def step(self):

        new_grid = copy.deepcopy(self.grid)

        for y in range(self.rows):
            for x in range(self.cols):

                isAlive = self.grid[y][x] > self.dead
                live_neighbours = self.countliveneighbours(x, y)

                if isAlive:

                    if live_neighbours == 2 or live_neighbours == 3:
                        new_grid[y][x] = self.grid[y][x] + 1

                    else:
                        new_grid[y][x] = self.dead

                else:

                    if live_neighbours == 3:
                        new_grid[y][x] = self.alive

                    else:
                        new_grid [y][x] = self.dead

        return new_grid

    def displayGrid(self):

        for i in range(self.rows):
            for j in range(self.cols):

                TOP = j * CELL_SIZE
                LEFT = i * CELL_SIZE
                WIDTH = CELL_SIZE
                HEIGHT = CELL_SIZE
                AGE = self.grid[i][j]
                DARKENING = DARKENING_FACTOR ** AGE

                if self.grid[i][j] > self.dead:
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

                elif self.grid[i][j] == self.dead:
                    pygame.draw.rect(screen, DEAD_OUTLINE, pygame.Rect(LEFT, TOP, WIDTH, HEIGHT))
                    pygame.draw.rect(screen, DEAD_COLOR,
                                     pygame.Rect(LEFT + OUTLINE_THICKNESS * 0.5, TOP + OUTLINE_THICKNESS * 0.5,
                                                 WIDTH - OUTLINE_THICKNESS, HEIGHT - OUTLINE_THICKNESS))

    def setCellAtPos(self, state, x, y):
        cell_x = math.floor(x / CELL_SIZE)
        cell_y = math.floor(y / CELL_SIZE)

        self.grid[cell_x][cell_y] = state


arena = Grid(50, 50)

screen = pygame.display.set_mode((arena.cols * CELL_SIZE, arena.rows * CELL_SIZE))
pygame.display.set_caption("yep")

play = arena.genEmptyGrid()
game = Simulation(play, 1, 0)


# play[3][5] = arena.alive
# play[4][5] = arena.alive
# play[5][5] = arena.alive
# play[3][4] = arena.alive

running = True
playing = True
press_count = 0

while running:

    game.displayGrid()
    pygame.display.update()

    if playing:
        game.grid = game.step()
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
                game.setCellAtPos(game.alive, x, y)
            elif pygame.mouse.get_pressed()[2]:
                game.setCellAtPos(game.dead, x, y)

        if event.type == pygame.QUIT:
            running = False

pygame.quit()
