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
SIM_POS = (50, 50)
BG_COLOR = (160, 160, 160)
TEXT_COLOR = (0, 0, 0)

pygame.init()

font = pygame.font.Font('cmunbi.ttf', 32)

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
    def __init__(self, gridArr, alive, dead, ruleset):
        self.grid = gridArr
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        self.alive = alive
        self.dead = dead
        self.birth_rules = ruleset[0]
        self.survival_rules = ruleset[1]


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

        for cell_y in range(self.rows):
            for cell_x in range(self.cols):

                isAlive = self.grid[cell_y][cell_x] > self.dead
                live_neighbours = self.countliveneighbours(cell_x, cell_y)

                # if isAlive:
                #
                #     if live_neighbours == 2 or live_neighbours == 3:
                #         new_grid[cell_y][cell_x] = self.grid[cell_y][cell_x] + 1
                #
                #     else:
                #         new_grid[cell_y][cell_x] = self.dead
                #
                # else:
                #
                #     if live_neighbours == 3:
                #         new_grid[cell_y][cell_x] = self.alive
                #
                #     else:
                #         new_grid[cell_y][cell_x] = self.dead

                if isAlive:

                    if live_neighbours in self.survival_rules:
                        new_grid[cell_y][cell_x] = self.grid[cell_y][cell_x] + 1

                    else:
                        new_grid[cell_y][cell_x] = self.dead

                else:
                    if live_neighbours in self.birth_rules:
                        new_grid[cell_y][cell_x] = self.grid[cell_y][cell_x] + 1

        return new_grid

    def displayGrid(self):

        for i in range(self.rows):
            for j in range(self.cols):

                TOP = j * CELL_SIZE + SIM_POS[0]
                LEFT = i * CELL_SIZE+ SIM_POS[1]
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
        cell_x = min(math.floor((x - SIM_POS[0]) / CELL_SIZE), self.cols - 1)
        cell_y = min(math.floor((y - SIM_POS[1]) / CELL_SIZE), self.rows - 1)

        self.grid[cell_x][cell_y] = state

    def statistics(self):
        alive_cell_count = 0
        dead_cell_count = 0
        avg_age_alive = 0
        avg_age_dead = 0

        for cell_y in range(self.rows):
            for cell_x in range(self.cols):

                if self.grid[cell_y][cell_x] > 0:

                    alive_cell_count += 1
                    avg_age_alive += self.grid[cell_y][cell_x]
                    avg_age_dead += self.grid[cell_y][cell_x]

                elif self.grid[cell_y][cell_x] == self.dead:

                    dead_cell_count += 1
                    avg_age_dead += self.grid[cell_y][cell_x]

        if alive_cell_count == 0:
            avg_age_alive = 0
        else:
            avg_age_alive /= alive_cell_count

        avg_age_dead /= self.rows * self.cols

        return alive_cell_count, dead_cell_count, avg_age_alive, avg_age_dead

    def reset(self):
        for cell_y in range(self.rows):
            for cell_x in range(self.cols):
                self.grid[cell_y][cell_x] = self.dead



arena = Grid(25, 25)

screen = pygame.display.set_mode((arena.cols * CELL_SIZE + 300, arena.rows * CELL_SIZE + 300))
screen.fill(BG_COLOR)
pygame.display.set_caption("yep")

rules = [
    {2, 3},
    {2, 3}
]
play = arena.genEmptyGrid()
game = Simulation(play, 1, 0, rules)

# play[3][5] = arena.alive
# play[4][5] = arena.alive
# play[5][5] = arena.alive
# play[3][4] = arena.alive

running = True
playing = True
press_count = 0

while running:

    screen.fill(BG_COLOR)

    stats = game.statistics()
    alive_count = stats[0]
    dead_count = stats[1]
    avg_age_alive = stats[2]
    avg_age_dead = stats[3]

    # blank_text = font.render('', True, TEXT_COLOR, BG_COLOR)

    alive_count_text = font.render(('Alive cells: ' + str(alive_count)), True, TEXT_COLOR, BG_COLOR)
    alive_count_textRect = alive_count_text.get_rect()
    alive_count_textRect.topleft = (SIM_POS[0], 550)

    dead_count_text = font.render(('Dead cells: ' + str(dead_count)), True, TEXT_COLOR, BG_COLOR)
    dead_count_textRect = dead_count_text.get_rect()
    dead_count_textRect.topleft = (SIM_POS[0], 590)

    avg_age_alive_text = font.render(('Average cell age: ' + str(avg_age_alive)), True, TEXT_COLOR, BG_COLOR)
    avg_age_alive_textRect = avg_age_alive_text.get_rect()
    avg_age_alive_textRect.topleft = (SIM_POS[0], 630)

    avg_age_dead_text = font.render(('Average cell age w/ dead cells: ' + str(avg_age_dead)), True, TEXT_COLOR, BG_COLOR)
    avg_age_dead_textRect = avg_age_dead_text.get_rect()
    avg_age_dead_textRect.topleft = (SIM_POS[0], 670)

    screen.blit(alive_count_text, alive_count_textRect)
    screen.blit(dead_count_text, dead_count_textRect)
    screen.blit(avg_age_alive_text, avg_age_alive_textRect)
    screen.blit(avg_age_dead_text, avg_age_dead_textRect)

    game.displayGrid()
    pygame.display.update()


    if playing:
        game.grid = game.step()
        pygame.time.wait(100)

    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if press_count % 2 == 0:
                    playing = False
                else:
                    playing = True
                press_count += 1

            if event.key == pygame.K_r:
                game.reset()

            if event.key == pygame.K_s:
                game.grid = game.step()

        elif pygame.mouse.get_pressed():
            x, y = pygame.mouse.get_pos()

            if pygame.mouse.get_pressed()[0]:
                game.setCellAtPos(game.alive, x, y)
            elif pygame.mouse.get_pressed()[2]:
                game.setCellAtPos(game.dead, x, y)

        if event.type == pygame.QUIT:
            running = False

pygame.quit()
