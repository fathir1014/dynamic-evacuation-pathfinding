import copy
import csv
import os
import random
import time
from collections import deque

import matplotlib.pyplot as plt

from core.grid import Grid
from simulation.simulator import run_simulation
from system.cache import PathCache
from system.validator import is_path_available
from utils.building import add_hazards, build_building


OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
RESULT_FILE = os.path.join(OUTPUT_DIR, "comparison_results.csv")
SUMMARY_FILE = os.path.join(OUTPUT_DIR, "comparison_summary.csv")
HEALTH_GRAPH_FILE = os.path.join(OUTPUT_DIR, "health_performance.png")
RUN_SEED = 42

def init_output():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(RESULT_FILE, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=result_columns())
        writer.writeheader()


def result_columns():
    return [
        "seed",
        "run",
        "mode",
        "step",
        "status",
        "time",
        "health",
        "damage",
        "x",
        "y",
        "goal_x",
        "goal_y",
        "reached_goal",
    ]


def log_to_csv(row):
    row["seed"] = RUN_SEED
    with open(RESULT_FILE, "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=result_columns())
        writer.writerow(row)


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


def summarize_results(all_results):
    summary = []

    for mode in ["ASTAR_ONLY", "HYBRID"]:
        rows = [row for row in all_results if row["mode"] == mode]
        if not rows:
            continue

        final = rows[-1]
        planning_rows = [row for row in rows if row["status"] != "MOVE_ONLY"]
        avg_health = sum(float(row["health"]) for row in rows) / len(rows)
        total_time = sum(float(row["time"]) for row in rows)

        summary.append({
            "mode": mode,
            "steps": final["step"],
            "final_health": final["health"],
            "avg_health": round(avg_health, 3),
            "planning_count": len(planning_rows),
            "total_planning_time": round(total_time, 6),
            "reached_goal": final["reached_goal"],
        })

    with open(SUMMARY_FILE, "w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "mode",
                "steps",
                "final_health",
                "avg_health",
                "planning_count",
                "total_planning_time",
                "reached_goal",
            ],
        )
        writer.writeheader()
        writer.writerows(summary)

    return summary


def save_health_graph(all_results):
    plt.figure(figsize=(10, 5))

    for mode, color in [("ASTAR_ONLY", "#ef4444"), ("HYBRID", "#2563eb")]:
        rows = [row for row in all_results if row["mode"] == mode]
        if not rows:
            continue

        steps = [int(row["step"]) for row in rows]
        health = [float(row["health"]) for row in rows]
        plt.plot(steps, health, label=mode, linewidth=2.5, color=color)

    plt.title("Performance Comparison Based on Agent Health")
    plt.xlabel("Step")
    plt.ylabel("Health")
    plt.ylim(0, 105)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(HEALTH_GRAPH_FILE, dpi=160)
    plt.close()


def main():
    global RUN_SEED

    RUN_SEED = time.time_ns() % 1_000_000_000
    random.seed(RUN_SEED)
    init_output()
    print(f"RUN SEED: {RUN_SEED}")

    base_grid = Grid(50, 30)
    exits = build_building(base_grid)
    start = random_spawn(base_grid, exits)
    exit_distances = build_exit_distance_map(base_grid, exits)

    print(f"START: ({start.x}, {start.y})")
    print(f"NEAREST EXIT PATH LENGTH: {exit_distances[start]}")

    generated = add_hazards(base_grid, start, exits)
    print("Valid dynamic obstacle generated" if generated else "Hazard fallback: no blocking obstacle")

    start_pos = start.pos
    all_results = []

    for mode in ["ASTAR_ONLY", "HYBRID"]:
        random.seed(RUN_SEED + 1000)
        scenario_grid = copy.deepcopy(base_grid)
        scenario_start = scenario_grid.get_node(start_pos[0], start_pos[1])
        cache = PathCache() if mode == "HYBRID" else None

        results = run_simulation(
            grid=scenario_grid,
            start=scenario_start,
            exits=exits,
            cache=cache,
            steps=120,
            log_fn=log_to_csv,
            speed=0.08,
            mode=mode,
            run_name=mode,
            visualize=True,
        )
        all_results.extend(results)

    summary = summarize_results(all_results)
    save_health_graph(all_results)

    print("\n=== COMPARISON SUMMARY ===")
    for row in summary:
        print(row)

    print(f"\nSaved results: {RESULT_FILE}")
    print(f"Saved summary: {SUMMARY_FILE}")
    print(f"Saved graph: {HEALTH_GRAPH_FILE}")


if __name__ == "__main__":
    main()
