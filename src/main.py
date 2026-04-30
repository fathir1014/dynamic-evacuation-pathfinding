# src/main.py

import random
import csv

from core.grid import Grid
from system.cache import PathCache
from simulation.simulator import run_simulation


def randomize_environment(grid, start, goal):
    for x in range(grid.width):
        for y in range(grid.height):
            node = grid.get_node(x, y)

            if node == start or node == goal:
                continue

            node.walkable = random.random() > 0.1
            node.smoke = random.randint(0, 5)
            node.debris = random.randint(0, 3)
            node.crowd = random.randint(0, 4)


def init_csv():
    with open("output/results.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Step", "Status", "Time"])


def log_to_csv(step, status, exec_time):
    with open("output/results.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([step, status, exec_time])


def main():
    # random.seed(42)

    grid = Grid(20, 20)
    cache = PathCache()

    start = grid.get_node(0, 0)
    goal = grid.get_node(19, 19)

    randomize_environment(grid, start, goal)
    init_csv()

    run_simulation(
        grid=grid,
        start=start,
        goal=goal,
        cache=cache,
        steps=20,
        log_fn=log_to_csv
    )


if __name__ == "__main__":
    main()