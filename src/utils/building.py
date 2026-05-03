import random

from system.validator import is_safe_path_available


def build_building(grid):
    for x in range(grid.width):
        for y in range(grid.height):
            grid.set_floor(x, y)

    for x in range(grid.width):
        grid.set_wall(x, 0)
        grid.set_wall(x, grid.height - 1)

    for y in range(grid.height):
        grid.set_wall(0, y)
        grid.set_wall(grid.width - 1, y)

    rooms = [
        (2, 20, 9, 27),    # ruang rapat
        (2, 13, 8, 19),    # direktur / tamu
        (5, 2, 13, 7),     # server / IT
        (10, 20, 15, 27),  # ruang kerja 1
        (16, 20, 21, 27),  # ruang kerja 2
        (22, 20, 27, 27),  # ruang kerja 3
        (12, 10, 25, 16),  # keuangan / HRD / administrasi
        (28, 10, 33, 16),  # pantry / mushola
        (34, 10, 43, 16),  # training
        (29, 20, 34, 27),  # arsip
        (35, 20, 40, 27),  # gudang
        (41, 20, 48, 27),  # kantin
        (44, 12, 48, 19),  # toilet
        (30, 2, 39, 7),    # laboratorium
        (40, 2, 48, 7),    # ruang proyek
    ]

    for room in rooms:
        wall_rect(grid, *room)

    doors = [
        (6, 20), (8, 16), (8, 13), (8, 5),
        (13, 20), (18, 20), (24, 20),
        (18, 16), (18, 10), (24, 12),
        (28, 13), (33, 13), (36, 10),
        (31, 20), (37, 20), (43, 20),
        (44, 15), (48, 15), (33, 7), (41, 7), (48, 5),
        (15, 5), (25, 5),
    ]

    for x, y in doors:
        if grid.in_bounds(x, y):
            grid.set_floor(x, y)

    exits = carve_exits(grid)

    return exits


def wall_rect(grid, x1, y1, x2, y2):
    for x in range(x1, x2 + 1):
        grid.set_wall(x, y1)
        grid.set_wall(x, y2)

    for y in range(y1, y2 + 1):
        grid.set_wall(x1, y)
        grid.set_wall(x2, y)


def carve_exits(grid):
    exits = [
        (5, grid.height - 1),
        (25, grid.height - 1),
        (46, grid.height - 1),
        (0, 15),
        (grid.width - 1, 15),
        (8, 0),
        (25, 0),
        (grid.width - 1, 5),
    ]

    for x, y in exits:
        open_exit_gap(grid, x, y)

    return exits


def open_exit_gap(grid, x, y):
    grid.set_floor(x, y)

    if y == 0:
        grid.set_floor(x, 1)
        if grid.in_bounds(x - 1, 0):
            grid.set_floor(x - 1, 0)
            grid.set_floor(x - 1, 1)
        if grid.in_bounds(x + 1, 0):
            grid.set_floor(x + 1, 0)
            grid.set_floor(x + 1, 1)
    elif y == grid.height - 1:
        grid.set_floor(x, grid.height - 2)
        if grid.in_bounds(x - 1, grid.height - 1):
            grid.set_floor(x - 1, grid.height - 1)
            grid.set_floor(x - 1, grid.height - 2)
        if grid.in_bounds(x + 1, grid.height - 1):
            grid.set_floor(x + 1, grid.height - 1)
            grid.set_floor(x + 1, grid.height - 2)
    elif x == 0:
        grid.set_floor(1, y)
        if grid.in_bounds(0, y - 1):
            grid.set_floor(0, y - 1)
            grid.set_floor(1, y - 1)
        if grid.in_bounds(0, y + 1):
            grid.set_floor(0, y + 1)
            grid.set_floor(1, y + 1)
    elif x == grid.width - 1:
        grid.set_floor(grid.width - 2, y)
        if grid.in_bounds(grid.width - 1, y - 1):
            grid.set_floor(grid.width - 1, y - 1)
            grid.set_floor(grid.width - 2, y - 1)
        if grid.in_bounds(grid.width - 1, y + 1):
            grid.set_floor(grid.width - 1, y + 1)
            grid.set_floor(grid.width - 2, y + 1)

def reset_hazards(grid):
    grid.reset_dynamic()


def add_hazards(grid, start, exits, block_chance=0.018, risk_chance=0.10, max_try=120):
    protected = {start.pos, *exits}

    for _ in range(max_try):
        reset_hazards(grid)

        for node in grid.walkable_nodes():
            if node.pos in protected:
                continue

            is_main_corridor = (
                node.x in {1, grid.width // 2, grid.width - 2} or
                node.y in {1, grid.height // 2, grid.height - 2}
            )
            local_block_chance = block_chance * (0.25 if is_main_corridor else 1.0)

            roll = random.random()
            if roll < local_block_chance:
                node.walkable = False
                node.debris = 10
                node.hazard = "blocked"
            elif roll < local_block_chance + risk_chance:
                node.hazard = random.choice(["smoke", "crowd", "liquid"])
                if node.hazard == "smoke":
                    node.smoke = random.randint(2, 6)
                elif node.hazard == "crowd":
                    node.crowd = random.randint(2, 5)
                else:
                    node.liquid = random.randint(1, 4)

        if is_safe_path_available(grid, start, exits):
            return True

    reset_hazards(grid)
    return False