import pygame
import random
import numpy as np
import ca_utils as ca

pygame.init()

GAME_SIZE = (11, 11)
CELL_SIZE = 30

SCREEN_SIZE = np.multiply(GAME_SIZE, CELL_SIZE)
OUTLINe_THICKNESS = CELL_SIZE * 0.1


class Simulation:
    def __init__(self, grid_size, tree_growth_rate, fire_spead_rate, lightning_probability, burn_time):
        self.cols = grid_size[0]
        self.rows = grid_size[1]
        self.tree_growth_rate = tree_growth_rate
        self.fire_spread_rate = fire_spead_rate
        self.lightning_probability = lightning_probability
        self.burn_time = burn_time

        self.dead = 0
        self.tree = 1
        self.burning = 2

        self.stateToColorDict = {
            self.dead: (100, 100, 100),
            self.tree: (0, 200, 0),
            self.burning: (200, 0, 0)
        }

        self.grid = ca.genEmptyGrid(grid_size, [self.dead, 0])

    def checkBurningNeighbours(self, cell_x, cell_y):
        count = 0

        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:

                neighbour_x = cell_x + j
                neighbour_y = cell_y + i

                if -1 < neighbour_x < self.cols:
                    if -1 < neighbour_y < self.rows:

                        if self.grid[neighbour_y][neighbour_x][0] == self.burning:
                            count += 1

        return count

    def step(self):

        new_grid = [row[:] for row in self.grid]

        for y in range(self.rows):
            for x in range(self.cols):

                curr_state = self.grid[y][x][0]
                curr_burn_time = self.grid[y][x][1]

                if curr_state == self.dead:

                    if random.random() < self.tree_growth_rate:
                        new_grid[y][x][0] = self.tree

                elif curr_state == self.tree:

                    if random.random() < self.fire_spread_rate * self.checkBurningNeighbours(x, y):
                        new_grid[y][x][0] = self.burning

                    elif random.random() < self.lightning_probability:
                        new_grid[y][x][0] = self.burning

                else:

                    if curr_burn_time > self.burn_time:
                        new_grid[y][x][0] = self.dead
                        new_grid[y][x][1] = 0

                    new_grid[y][x][1] += 1


        return new_grid

    def displayGrid(self, surf):

        for cell_y in range(self.rows):
            for cell_x in range(self.cols):
                curr_state = self.grid[cell_y][cell_x][0]

                pygame.draw.rect(surf, np.multiply(self.stateToColorDict[curr_state], 0.7), pygame.Rect(
                    (cell_x * CELL_SIZE, cell_y * CELL_SIZE),
                    (CELL_SIZE, CELL_SIZE)
                ))

                pygame.draw.rect(surf, self.stateToColorDict[curr_state], pygame.Rect(
                    (cell_x * CELL_SIZE + OUTLINe_THICKNESS, cell_y * CELL_SIZE + OUTLINe_THICKNESS),
                    (CELL_SIZE - 2 * OUTLINe_THICKNESS, CELL_SIZE - 2 * OUTLINe_THICKNESS)
                ))



screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Forest fire simulator')




game = Simulation(GAME_SIZE, 0.1, 0.2, 0.0005, 3)

ca.printGrid(game.grid)



running = True
timer = 0

while running:
    screen.fill((0, 0, 0))

    game.displayGrid(screen)
    pygame.display.update()

    if timer > 200:
        game.grid = game.step()
        timer = 0

    timer += 1


    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False


pygame.quit()
