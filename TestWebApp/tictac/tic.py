import random

def get_rows():
    rows = []
    for x in range(3):
        v = []
        h = []
        for y in range(3):
            v.append(box(x + 1, y + 1))
            h.append(box(y + 1, x + 1))
        rows.append(v)
        rows.append(h)
    rows.append(["11", "22", "33"])
    rows.append(["13", "22", "31"])
    return rows


def box(x, y):
    return u"{}{}".format(x, y)

def get_random_box():
    return box(random.randint(1, 3), random.randint(1, 3))

def play(grid):
    box = get_random_box()
    while not grid.isfree(box):
        box = get_random_box()
    grid.play(box, "o")

class Grid:

    def __init__(self):
        self.reset()

    def reset(self):
        self.grid = {box(x, y) : "" for x in range(1, 4) for y in range(1, 4)}

    def isfree(self, box):
        return self.grid[box] == ""

    def check_status(self):
        for row in get_rows():
            symbols = set(self.grid[box] for box in row)
            if len(symbols) == 1 and u"" not in symbols:
                return  "player {} wins".format(symbols.pop())
        if "" in self.grid.values():
            return "continue"
        return "end"

    def play(self, box, symbol):
        if not self.isfree(box):
            raise Exception("{} is not free!".format(box))
        self.grid[box] = symbol

if __name__ == "__main__":
    print get_rows()
