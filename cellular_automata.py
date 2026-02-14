import copy
import pygame
import math
import numpy as np

CELL_SIZE = 10
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
medium_font = pygame.font.Font('cmunbi.ttf', 24)


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


def convRules(ruleString):
    birth_string = ruleString.split('/')[0]
    survival_string = ruleString.split('/')[1]

    birth = birth_string.lstrip()
    survival = survival_string.lstrip()

    birth_list = []
    survival_list = []

    for i in birth:
        if i.isdigit():
            birth_list.append(int(i))
    for i in survival:
        if i.isdigit():
            survival_list.append(int(i))

    return birth_list, survival_list




class Simulation:
    def __init__(self, gridArr, alive, dead, ruleset):
        self.grid = gridArr
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        self.alive = alive
        self.dead = dead
        self.ruleset = ruleset
        self.birth_rules = convRules(self.ruleset)[0]
        self.survival_rules = convRules(self.ruleset)[1]
        self.generation = 0

    def countliveneighbours(self, cell_x, cell_y):
        count = 0

        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if self.grid[(cell_y + i) % self.rows][(cell_x + j) % self.cols] > self.dead:
                    count += 1

        if self.grid[cell_y][cell_x] > self.dead:
            count -= 1

        return count

    def updateRules(self):
        self.birth_rules = convRules(self.ruleset)[0]
        self.survival_rules = convRules(self.ruleset)[1]

    def step(self):

        new_grid = [row[:] for row in self.grid]

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
        self.generation += 1

        return new_grid

    def displayGrid(self):

        for i in range(self.rows):
            for j in range(self.cols):

                TOP = i * CELL_SIZE + SIM_POS[0]
                LEFT = j * CELL_SIZE + SIM_POS[1]
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
        rule_set = self.ruleset

        for cell_y in range(self.rows):
            for cell_x in range(self.cols):

                if self.grid[cell_y][cell_x] > 0:

                    alive_cell_count += 1
                    avg_age_alive += self.grid[cell_y][cell_x]
                    avg_age_dead += self.grid[cell_y][cell_x]

                elif self.grid[cell_y][cell_x] == self.dead:

                    dead_cell_count += 1
                    avg_age_dead += self.grid[cell_y][cell_x]

        percent_live_cells = (alive_cell_count / (self.rows * self.cols)) * 100

        if alive_cell_count == 0:
            avg_age_alive = 0
        else:
            avg_age_alive /= alive_cell_count

        avg_age_dead /= self.rows * self.cols

        return alive_cell_count, dead_cell_count, avg_age_alive, avg_age_dead, percent_live_cells, rule_set

    def reset(self):
        self.generation = 0

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

class Button:
    def __init__(self, surf, text, color, pos, width, height):
        self.surf = surf
        self.text = text
        self.pos = pos
        self.color = color
        self.width = width
        self.height = height

        self.center = (self.pos[0] + self.width / 2, self.pos[1] + self.height / 2)

    def drawButton(self):
        pygame.draw.rect(self.surf, (0, 0, 0), pygame.Rect(self.pos, (self.width, self.height)))
        pygame.draw.rect(self.surf, self.color, pygame.Rect(shiftPointByCoords(self.pos, 3, 3), (self.width - 6, self.height - 6)))

        button_text = medium_font.render(self.text, True, TEXT_COLOR, self.color)
        button_textRect = button_text.get_rect()
        button_textRect.center = self.center
        self.surf.blit(button_text, button_textRect)

    def isClicked(self, cursor_x, cursor_y, isMouseClicked):
        clicked = False

        right_bound = self.pos[0] + self.width
        left_bound = self.pos[0]

        bottom_bound = self.pos[1] + self.height
        top_bound = self.pos[1]

        if isMouseClicked:
            if left_bound < cursor_x < right_bound:
                if top_bound < cursor_y < bottom_bound:
                    clicked = True

        return clicked


class Plotter:
    def __init__(self, surf):
        self.surface = surf

    def drawMarkerAtPoint(self, orientation, length, point):
        thickness = 3

        if orientation == 'vertical':
            pygame.draw.line(self.surface, (0, 0, 0), shiftPointByCoords(point, 0, length),
                             shiftPointByCoords(point, 0, -length), thickness)
        elif orientation == 'horizontal':
            pygame.draw.line(self.surface, (0, 0, 0), shiftPointByCoords(point, -length, 0),
                             shiftPointByCoords(point, length, 0), thickness)

    def drawMarkerText(self, text, pos):
        marker_text = small_font.render(text, True, TEXT_COLOR, BG_COLOR)
        markertextRect = marker_text.get_rect()
        markertextRect.topleft = pos
        self.surface.blit(marker_text, markertextRect)

    def drawCaption(self, caption, pos):
        caption_text = small_font.render(caption, True, TEXT_COLOR, BG_COLOR)
        caption_textRect = caption_text.get_rect()
        caption_textRect.topleft = pos
        self.surface.blit(caption_text, caption_textRect)

    def drawPlotAtPos(self, stat, xPointSet, yPointSet, plot_pos, width, height, dec_x, dec_y):
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
            unit_x = width / (max(xCorSet))

        pygame.draw.rect(self.surface, (255, 255, 255), pygame.Rect(plot_pos[0], plot_pos[1], width, height))

        pygame.draw.line(self.surface, (0, 0, 0), corner_bl, corner_br, 7)
        pygame.draw.line(self.surface, (0, 0, 0), corner_bl, corner_tl, 7)

        for i in range(x_marker_amount + 1):
            marker_pos = shiftPointByPoint((step_x * i, 0), corner_bl)
            placeholder = step_x / unit_x
            text = str(round(placeholder * i, dec_x))
            text_pos = shiftPointByCoords(marker_pos, -4, 10)

            drawMarkerAtPoint(screen, 'vertical', 9, marker_pos)
            drawMarkerText(screen, text, text_pos)

        for i in range(y_marker_amount + 1):
            marker_pos = shiftPointByPoint((0, step_y * i), corner_bl)
            placeholder = step_y / unit_y
            text = str(round(placeholder * i, dec_y))
            text_pos = shiftPointByCoords(marker_pos, -38 - 7 * math.log(round(placeholder * i, dec_y) + 1, 10), -12)

            drawMarkerAtPoint(screen, 'horizontal', 9, marker_pos)
            drawMarkerText(screen, text, text_pos)

        drawCaption(screen, str(stat), shiftPointByCoords(corner_tl, 0, -25))

        for i in range(len(pointSet) - 1):
            p1 = multiplyPointByNumbers(pointSet[i], unit_x, unit_y)
            p2 = multiplyPointByNumbers(pointSet[i + 1], unit_x, unit_y)

            shifted_p1 = shiftPointByPoint(p1, corner_bl)
            shifted_p2 = shiftPointByPoint(p2, corner_bl)

            pygame.draw.line(self.surface, (0, 0, 0), shifted_p1, shifted_p2, 2)



def drawMarkerAtPoint(surf, orientation, length, point):
    thickness = 3

    if orientation == 'vertical':
        pygame.draw.line(surf, (0, 0, 0), shiftPointByCoords(point, 0, length), shiftPointByCoords(point, 0, -length), thickness)
    elif orientation == 'horizontal':
        pygame.draw.line(surf, (0, 0, 0), shiftPointByCoords(point, -length, 0), shiftPointByCoords(point, length, 0), thickness)


def drawMarkerText(surf, text, pos):
    marker_text = small_font.render(text, True, TEXT_COLOR, BG_COLOR)
    markertextRect = marker_text.get_rect()
    markertextRect.topleft = pos
    surf.blit(marker_text, markertextRect)

def drawCaption(surf, caption, pos):
    caption_text = small_font.render(caption, True, TEXT_COLOR, BG_COLOR)
    caption_textRect = caption_text.get_rect()
    caption_textRect.topleft = pos
    surf.blit(caption_text, caption_textRect)


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
        unit_x = width / (max(xCorSet))

    pygame.draw.rect(surf, (255, 255, 255), pygame.Rect(plot_pos[0], plot_pos[1], width, height))

    pygame.draw.line(surf, (0, 0, 0), corner_bl, corner_br, 7)
    pygame.draw.line(surf, (0, 0, 0), corner_bl, corner_tl, 7)

    for i in range(x_marker_amount + 1):
        marker_pos = shiftPointByPoint((step_x * i, 0), corner_bl)
        placeholder = step_x / unit_x
        text = str(round(placeholder * i, dec_x))
        text_pos = shiftPointByCoords(marker_pos, -4, 10)


        drawMarkerAtPoint(screen, 'vertical', 9, marker_pos)
        drawMarkerText(screen, text, text_pos)


    for i in range(y_marker_amount + 1):
        marker_pos = shiftPointByPoint((0, step_y * i), corner_bl)
        placeholder = step_y / unit_y
        text = str(round(placeholder * i, dec_y))
        text_pos = shiftPointByCoords(marker_pos, -38 - 7 * math.log(round(placeholder * i, dec_y) + 1, 10), -12)

        drawMarkerAtPoint(screen, 'horizontal', 9, marker_pos)
        drawMarkerText(screen, text, text_pos)


    drawCaption(screen,str(stat), shiftPointByCoords(corner_tl, 0, -25))

    for i in range(len(pointSet) - 1):
        p1 = multiplyPointByNumbers(pointSet[i], unit_x, unit_y)
        p2 = multiplyPointByNumbers(pointSet[i + 1], unit_x, unit_y)

        shifted_p1 = shiftPointByPoint(p1, corner_bl)
        shifted_p2 = shiftPointByPoint(p2, corner_bl)

        pygame.draw.line(surf, (0, 0, 0), shifted_p1, shifted_p2, 2)

def resetArrays(arr):
    new_arr = []

    for i in range(len(arr)):
        new_arr.append([])

    return new_arr


def drawStatText(surf, text, order):
    stat_text = font.render(text, True, TEXT_COLOR, BG_COLOR)
    stat_text_rect = stat_text.get_rect()
    stat_text_rect.topleft = (SIM_POS[0], text_order[order])

    surf.blit(stat_text, stat_text_rect)


arena = Grid(70, 70)

rules = 'B3/S23'
print(convRules(rules))
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

plotter = Plotter(screen)

auto_rules_button = Button(screen, 'Toggle auto', (0, 255, 0), (800, 800), 200, 100)
reset_button = Button(screen, 'Reset', (150, 150, 150), (1050, 800), 200, 100)

# play[3][5] = arena.alive
# play[4][5] = arena.alive
# play[5][5] = arena.alive
# play[3][4] = arena.alive

running = True
playing = False
auto = False

stats = game.statistics()

alive_y = []
dead_y = []
avg_age_alive_y = []
avg_age_dead_y = []
percent_alive_y = []
generation_x = []

plot_stats = [
    alive_y,
    dead_y,
    avg_age_alive_y,
    avg_age_dead_y,
    percent_alive_y,
    generation_x,
]

# printGrid(play)
while running:

    screen.fill(BG_COLOR)
    game.updateRules()

    if playing:
        game.grid = game.step()
        stats = game.statistics()
        pygame.time.wait(20)


    alive_count = stats[0]
    dead_count = stats[1]
    avg_age_alive = round(stats[2], 2)
    avg_age_dead = round(stats[3], 2)
    percent_alive = round(stats[4], 2)
    current_rules = stats[5]


    generation_x.append(game.generation)
    alive_y.append(alive_count)
    dead_y.append(dead_count)
    avg_age_alive_y.append(avg_age_alive)
    avg_age_dead_y.append(avg_age_dead)
    percent_alive_y.append(percent_alive)

    if auto:
        if percent_alive < 7.5:
            game.ruleset = 'B3/S1245'

        if percent_alive > 40:
            game.ruleset = 'B3/S23'

        auto_rules_button.color = (0, 255, 0)

    else:
        auto_rules_button.color = (255, 0, 0)

    # blank_text = font.render('', True, TEXT_COLOR, BG_COLOR)

    drawStatText(screen, 'Alive cells: ' + str(alive_count), 0)
    drawStatText(screen, 'Dead cells: ' + str(dead_count), 1)
    drawStatText(screen, 'Average cell age: ' + str(avg_age_alive), 2)
    # drawStatText(screen, 'Average cell age w/ dead cells: ' + str(avg_age_dead), 3)
    drawStatText(screen, 'Percentage of alive cells: ' + str(percent_alive) + '%', 3)
    drawStatText(screen, 'Current ruleset: ' + str(current_rules), 4)

    auto_rules_button.drawButton()
    reset_button.drawButton()

    plotter.drawPlotAtPos('Alive cell count by generation', generation_x, alive_y, (next_to_sim, plot_order[0]), 500, 200, 0, 0)
    plotter.drawPlotAtPos('Percent of alive cells', generation_x, percent_alive_y, (next_to_sim, plot_order[1]), 500, 200, 0, 2)
    plotter.drawPlotAtPos('Average cell age by generation', generation_x, avg_age_alive_y, (next_to_sim, plot_order[2]), 500, 200, 0, 0)

    game.displayGrid()
    pygame.display.update()



    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                playing = not playing

            if event.key == pygame.K_a:
                auto = not auto

            if event.key == pygame.K_r:
                game.reset()
                stats = game.statistics()
                generation = 0
                alive_y = []
                dead_y = []
                avg_age_alive_y = []
                avg_age_dead_y = []
                percent_alive_y = []
                generation_x = []

            if event.key == pygame.K_s:
                game.grid = game.step()
                stats = game.statistics()

            if event.key == pygame.K_f:
                game.ruleset = str(input())

        if pygame.mouse.get_pressed():
            x, y = pygame.mouse.get_pos()

            if pygame.mouse.get_pressed()[0]:
                game.setCellAtPos(game.alive, x, y)
            elif pygame.mouse.get_pressed()[2]:
                game.setCellAtPos(game.dead, x, y)

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()

            if reset_button.isClicked(x, y, pygame.mouse.get_pressed()[0]):
                game.reset()
                stats = game.statistics()
                generation = 0
                alive_y = []
                dead_y = []
                avg_age_alive_y = []
                avg_age_dead_y = []
                percent_alive_y = []
                generation_x = []
                playing = False

            if auto_rules_button.isClicked(x, y, pygame.mouse.get_pressed()[0]):
                auto = not auto




        if event.type == pygame.QUIT:
            running = False




pygame.quit()
