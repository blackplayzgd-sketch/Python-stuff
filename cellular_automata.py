import copy
import pygame
import math
import numpy as np

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
small_font = pygame.font.Font('cmunbi.ttf', 16)


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

                TOP = i * CELL_SIZE + SIM_POS[0]
                LEFT = j * CELL_SIZE+ SIM_POS[1]
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

        self.grid[cell_y][cell_x] = state

    def statistics(self):
        alive_cell_count = 0
        dead_cell_count = 0
        avg_age_alive = 0
        avg_age_dead = 0
        percent_live_cells = 0

        for cell_y in range(self.rows):
            for cell_x in range(self.cols):

                if self.grid[cell_y][cell_x] > 0:

                    alive_cell_count += 1
                    avg_age_alive += self.grid[cell_y][cell_x]
                    avg_age_dead += self.grid[cell_y][cell_x]

                elif self.grid[cell_y][cell_x] == self.dead:

                    dead_cell_count += 1
                    avg_age_dead += self.grid[cell_y][cell_x]

        percent_live_cells = (alive_cell_count / (self.rows * self.cols )) * 100

        if alive_cell_count == 0:
            avg_age_alive = 0
        else:
            avg_age_alive /= alive_cell_count

        avg_age_dead /= self.rows * self.cols

        return alive_cell_count, dead_cell_count, avg_age_alive, avg_age_dead, percent_live_cells

    def reset(self):
        for cell_y in range(self.rows):
            for cell_x in range(self.cols):
                self.grid[cell_y][cell_x] = self.dead


def shiftPointByPoint(pShifted, pReference):
    point = (
        pReference[0] + pShifted[0],
        pReference[1] - pShifted[1]
    )
    return point

def shiftPointByCoords(point, xShift, yShift):
    new_point = (
        point[0] + xShift,
        point[1] + yShift
    )
    return new_point


def multiplyPointByNumbers(point, xMulti, yMulti):
    new_point = (
        point[0] * xMulti,
        point[1] * yMulti
    )
    return new_point


def drawMarkerAtPoint(surf, orientation, length, point):
    thickness = 3

    if orientation == 'vertical':
        pygame.draw.line(surf, (0, 0, 0), shiftPointByCoords(point, 0, length), shiftPointByCoords(point, 0, -length), thickness)
    elif orientation == 'horizontal':
        pygame.draw.line(surf, (0, 0, 0), shiftPointByCoords(point, -length, 0), shiftPointByCoords(point, length, 0), thickness)


def drawPlotAtPos(surf, stat, xPointSet, yPointSet, plot_pos, width, height, dec_x, dec_y):
    corner_bl = (plot_pos[0], plot_pos[1] + height)
    corner_br = (plot_pos[0] + width, plot_pos[1] + height)
    corner_tl = plot_pos
    unit_x = 50
    unit_y = 5

    x_marker_amount = 10
    step_x = width / x_marker_amount

    y_marker_amount = 6
    step_y = height / y_marker_amount

    pointSet = [(xPointSet[i], yPointSet[i]) for i in range(len(xPointSet))]
    xCorSet = [i[0] for i in pointSet]
    yCorSet = [i[1] for i in pointSet]

    if max(yCorSet) * unit_y > height:
        unit_y = height / max(yCorSet)

    if max(xCorSet) * unit_x > width:
        unit_x = math.floor(width / (max(xCorSet)))

    pygame.draw.rect(surf, (255, 255, 255), pygame.Rect(plot_pos[0], plot_pos[1], width, height))

    pygame.draw.line(surf, (0, 0, 0), corner_bl, corner_br, 7)
    pygame.draw.line(surf, (0, 0, 0), corner_bl, corner_tl, 7)

    for i in range(x_marker_amount + 1):
        marker_pos = shiftPointByPoint((step_x * i, 0), corner_bl)
        placeholder = step_x / unit_x

        drawMarkerAtPoint(screen, 'vertical', 9, marker_pos)

        marker_text = small_font.render(str(round(placeholder * i, dec_x)), True, TEXT_COLOR, BG_COLOR)
        markertextRect = marker_text.get_rect()
        markertextRect.topleft = shiftPointByCoords(marker_pos, -4, 10)
        surf.blit(marker_text, markertextRect)

    for i in range(y_marker_amount + 1):
        marker_pos = shiftPointByPoint((0, step_y * i), corner_bl)
        placeholder = step_y / unit_y

        drawMarkerAtPoint(screen, 'horizontal', 9, marker_pos)

        marker_text = small_font.render(str(round(placeholder * i, dec_y)), True, TEXT_COLOR, BG_COLOR)
        markertextRect = marker_text.get_rect()
        markertextRect.topleft = shiftPointByCoords(marker_pos, -38 - 7 * math.log(round(placeholder * i, dec_y) + 1, 10), -12)
        surf.blit(marker_text, markertextRect)

    caption_text = small_font.render(str(stat), True, TEXT_COLOR, BG_COLOR)
    caption_textRect = caption_text.get_rect()
    caption_textRect.topleft = shiftPointByCoords(corner_tl, 0, -25)
    surf.blit(caption_text, caption_textRect)

    for i in range(len(pointSet) - 1):
        p1 = multiplyPointByNumbers(pointSet[i], unit_x, unit_y)
        p2 = multiplyPointByNumbers(pointSet[i + 1], unit_x, unit_y)

        shifted_p1 = shiftPointByPoint(p1, corner_bl)
        shifted_p2 = shiftPointByPoint(p2, corner_bl)

        pygame.draw.line(surf, (0, 0, 0), shifted_p1, shifted_p2, 2)


arena = Grid(40, 40)

rules = [
    {3},
    {2, 3}
]
play = arena.genEmptyGrid()
game = Simulation(play, 1, 0, rules)

screen_height = game.rows * CELL_SIZE + 300
screen_width = game.cols * CELL_SIZE + 700
under_sim = game.rows * CELL_SIZE + 50
next_to_sim = 130 + game.cols * CELL_SIZE

text_order = []
plot_order = []

for i in range(10):
    text_order.append(i * 40 + under_sim)
    plot_order.append(i * 250 + 50)



screen = pygame.display.set_mode((screen_width, screen_height))
screen.fill(BG_COLOR)
pygame.display.set_caption("yep")

# play[3][5] = arena.alive
# play[4][5] = arena.alive
# play[5][5] = arena.alive
# play[3][4] = arena.alive

running = True
playing = False
press_count = 0
generation = 0

alive_y = []
dead_y = []
avg_age_alive_y = []
avg_age_dead_y = []
percent_alive_y = []
generation_x = []

printGrid(play)

while running:

    screen.fill(BG_COLOR)

    stats = game.statistics()
    alive_count = stats[0]
    dead_count = stats[1]
    avg_age_alive = round(stats[2], 2)
    avg_age_dead = round(stats[3], 2)
    percent_alive = round(stats[4], 2)

    generation_x.append(generation)
    alive_y.append(alive_count)
    dead_y.append(dead_count)
    avg_age_alive_y.append(avg_age_alive)
    avg_age_dead_y.append(avg_age_dead)
    percent_alive_y.append(percent_alive)

    # blank_text = font.render('', True, TEXT_COLOR, BG_COLOR)

    alive_count_text = font.render(('Alive cells: ' + str(alive_count)), True, TEXT_COLOR, BG_COLOR)
    alive_count_textRect = alive_count_text.get_rect()
    alive_count_textRect.topleft = (SIM_POS[0], text_order[0])

    dead_count_text = font.render(('Dead cells: ' + str(dead_count)), True, TEXT_COLOR, BG_COLOR)
    dead_count_textRect = dead_count_text.get_rect()
    dead_count_textRect.topleft = (SIM_POS[0], text_order[1])

    avg_age_alive_text = font.render(('Average cell age: ' + str(avg_age_alive)), True, TEXT_COLOR, BG_COLOR)
    avg_age_alive_textRect = avg_age_alive_text.get_rect()
    avg_age_alive_textRect.topleft = (SIM_POS[0], text_order[2])

    avg_age_dead_text = font.render(('Average cell age w/ dead cells: ' + str(avg_age_dead)), True, TEXT_COLOR, BG_COLOR)
    avg_age_dead_textRect = avg_age_dead_text.get_rect()
    avg_age_dead_textRect.topleft = (SIM_POS[0], text_order[3])

    percent_alive_text = font.render('Percentage of alive cells: ' + str(percent_alive) + '%', True, TEXT_COLOR, BG_COLOR)
    percent_alive_textRect = percent_alive_text.get_rect()
    percent_alive_textRect.topleft = (SIM_POS[0], text_order[4])

    screen.blit(alive_count_text, alive_count_textRect)
    screen.blit(dead_count_text, dead_count_textRect)
    screen.blit(avg_age_alive_text, avg_age_alive_textRect)
    screen.blit(avg_age_dead_text, avg_age_dead_textRect)
    screen.blit(percent_alive_text, percent_alive_textRect)

    drawPlotAtPos(screen, 'Alive cell count by generation', generation_x, alive_y, (next_to_sim, plot_order[0]), 500, 200, 0, 0)
    drawPlotAtPos(screen, 'Percent of alive cells', generation_x, percent_alive_y, (next_to_sim, plot_order[1]), 500, 200, 0, 0)
    drawPlotAtPos(screen, 'Average cell age by generation', generation_x, avg_age_alive_y, (next_to_sim, plot_order[2]), 500, 200, 0, 0)

    game.displayGrid()
    pygame.display.update()

    if playing:
        game.grid = game.step()
        generation += 1
        pygame.time.wait(20)

    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if press_count % 2 == 1:
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
