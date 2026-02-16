def genEmptyGrid(size, cell):
    cols = size[0]
    rows = size[1]

    grid = []
    for i in range(rows):

        row = []
        for j in range(cols):

            if type(cell) == list:
                item = []
                for k in cell:
                    item.append(k)
                row.append(item)
            else:
                row.append(cell)
        grid.append(row)

    return grid

def printGrid(grid):
    for i in range(len(grid)):
        print('')

    for row in grid:
        print(' '.join(str(i) for i in row))