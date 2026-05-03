import csv
import os
import random
from collections import deque

from core.grid import Grid
from simulation.simulator import run_simulation
from system.cache import PathCache
from system.validator import is_path_available
from utils.building import add_hazards, build_building


OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
RESULT_FILE = os.path.join(OUTPUT_DIR, "results.csv")


def init_csv():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(RESULT_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Step", "Status", "Time"])

import csv
import os
import random
from collections import deque

from core.grid import Grid
from simulation.simulator import run_simulation
from system.cache import PathCache
from system.validator import is_path_available
from utils.building import add_hazards, build_building


OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
RESULT_FILE = os.path.join(OUTPUT_DIR, "results.csv")


def init_csv():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(RESULT_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Step", "Status", "Time"])


def log_to_csv(step, status, exec_time):
    with open(RESULT_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([step, status, exec_time])


def distance_to_nearest_exit(node, exits):
    return min(abs(node.x - ex[0]) + abs(node.y - ex[1]) for ex in exits)


def build_exit_distance_map(grid, exits):
    distances = {}
    queue = deque()

    for exit_pos in exits:
        exit_node = grid.get_node(exit_pos[0], exit_pos[1])
        distances[exit_node] = 1
        queue.append(exit_node)

    while queue:
        current = queue.popleft()
        for neighbor in grid.get_neighbors(current):
            if neighbor in distances:
                continue
            distances[neighbor] = distances[current] + 1
            queue.append(neighbor)

    return distances

import csv
import os
import random
from collections import deque

from core.grid import Grid
from simulation.simulator import run_simulation
from system.cache import PathCache
from system.validator import is_path_available
from utils.building import add_hazards, build_building


OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
RESULT_FILE = os.path.join(OUTPUT_DIR, "results.csv")


def init_csv():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(RESULT_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Step", "Status", "Time"])


def log_to_csv(step, status, exec_time):
    with open(RESULT_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([step, status, exec_time])


def distance_to_nearest_exit(node, exits):
    return min(abs(node.x - ex[0]) + abs(node.y - ex[1]) for ex in exits)


def build_exit_distance_map(grid, exits):
    distances = {}
    queue = deque()

    for exit_pos in exits:
        exit_node = grid.get_node(exit_pos[0], exit_pos[1])
        distances[exit_node] = 1
        queue.append(exit_node)

    while queue:
        current = queue.popleft()
        for neighbor in grid.get_neighbors(current):
            if neighbor in distances:
                continue
            distances[neighbor] = distances[current] + 1
            queue.append(neighbor)

    return distances


def is_good_spawn(grid, node):
    if not node.walkable:
        return False
    return len(grid.get_neighbors(node)) >= 2


def random_spawn(grid, exits):
    exit_distances = build_exit_distance_map(grid, exits)
    scored_candidates = []

    for node in grid.walkable_nodes():
        if not is_good_spawn(grid, node):
            continue

        path_length = exit_distances.get(node, 0)
        if path_length > 0:
            scored_candidates.append((path_length, node))

    scored_candidates.sort(key=lambda item: item[0], reverse=True)

    farthest_band = scored_candidates[: max(1, len(scored_candidates) // 8)]
    random.shuffle(farthest_band)

    for _, node in farthest_band:
        if is_path_available(grid, node, exits):
            return node

    raise RuntimeError("Tidak ada spawn valid yang punya jalur ke exit.")

    return distances


def is_good_spawn(grid, node):
    if not node.walkable:
        return False
    return len(grid.get_neighbors(node)) >= 2


def random_spawn(grid, exits):
    exit_distances = build_exit_distance_map(grid, exits)
    scored_candidates = []

    for node in grid.walkable_nodes():
        if not is_good_spawn(grid, node):
            continue

        path_length = exit_distances.get(node, 0)
        if path_length > 0:
            scored_candidates.append((path_length, node))

    scored_candidates.sort(key=lambda item: item[0], reverse=True)

    farthest_band = scored_candidates[: max(1, len(scored_candidates) // 8)]
    random.shuffle(farthest_band)

    for _, node in farthest_band:
        if is_path_available(grid, node, exits):
            return node

    raise RuntimeError("Tidak ada spawn valid yang punya jalur ke exit.")


def main():
    grid = Grid(50, 30)
    cache = PathCache()
    exits = build_building(grid)

    start = random_spawn(grid, exits)
    print(f"START: ({start.x}, {start.y})")
    exit_distances = build_exit_distance_map(grid, exits)
    print(f"NEAREST EXIT PATH LENGTH: {exit_distances[start]}")

    generated = add_hazards(grid, start, exits)
    print("Valid dynamic obstacle generated" if generated else "Hazard fallback: no blocking obstacle")

    init_csv()

    run_simulation(
        grid=grid,
        start=start,
        exits=exits,
        cache=cache,
        steps=120,
        log_fn=log_to_csv,
        speed=0.12,
    )


if __name__ == "__main__":
    main()