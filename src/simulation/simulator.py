import time

import matplotlib.pyplot as plt

from simulation.agent import Agent
from system.replanner import plan_best_path
from system.validator import is_path_valid
from utils.building import add_hazards
from visualization.grid_plot import plot_grid


REPLAN_INTERVAL = 6
HAZARD_CHANGE_INTERVAL = 15


def run_simulation(grid, start, exits, cache, steps, log_fn, speed):
    plt.ion()
    fig, ax = plt.subplots(figsize=(14, 7))
    fig.subplots_adjust(right=0.82)

    agent = Agent(start)
    current_path = None
    goal = None

    for step in range(1, steps + 1):
        print(f"\n=== STEP {step} ===")

        if step > 1 and step % HAZARD_CHANGE_INTERVAL == 0:
            changed = add_hazards(grid, agent.get_node(), exits)
            current_path = None
            cache.clear()
            print("HAZARD_CHANGED" if changed else "HAZARD_RESET_FALLBACK")

        if current_path and not is_path_valid(current_path, agent.get_node()):
            current_path = None

        need_replan = (
            current_path is None or
            agent.target_index >= len(current_path) or
            step % REPLAN_INTERVAL == 0
        )

        if need_replan:
            t0 = time.perf_counter()
            path, goal, status = plan_best_path(grid, agent.get_node(), exits, cache)
            exec_time = time.perf_counter() - t0
            log_fn(step, status, exec_time)

import time

import matplotlib.pyplot as plt

from simulation.agent import Agent
from system.replanner import plan_best_path
from system.validator import is_path_valid
from utils.building import add_hazards
from visualization.grid_plot import plot_grid


REPLAN_INTERVAL = 6
HAZARD_CHANGE_INTERVAL = 15


def run_simulation(grid, start, exits, cache, steps, log_fn, speed):
    plt.ion()
    fig, ax = plt.subplots(figsize=(12, 7))

    agent = Agent(start)
    current_path = None
    goal = None

    for step in range(1, steps + 1):
        print(f"\n=== STEP {step} ===")

        if step > 1 and step % HAZARD_CHANGE_INTERVAL == 0:
            changed = add_hazards(grid, agent.get_node(), exits)
            current_path = None
            cache.clear()
            print("HAZARD_CHANGED" if changed else "HAZARD_RESET_FALLBACK")

        if current_path and not is_path_valid(current_path, agent.get_node()):
            current_path = None

        need_replan = (
            current_path is None or
            agent.target_index >= len(current_path) or
            step % REPLAN_INTERVAL == 0
        )

        if need_replan:
            t0 = time.perf_counter()
            path, goal, status = plan_best_path(grid, agent.get_node(), exits, cache)
            exec_time = time.perf_counter() - t0
            log_fn(step, status, exec_time)

            if path:
                current_path = path
                agent.set_path(path)
            else:
                current_path = None
        else:
            status = "MOVE_ONLY"

        print(f"STATUS: {status}")

        agent.update()

        agent_node = agent.get_node()
        agent_pos = agent.get_pos()
        traversed_path = current_path[:agent.target_index] if current_path else [agent_node]

        ax.clear()
        plot_grid(
            grid,
            path=traversed_path,
            full_path=current_path,
            agent_pos=agent_pos,
            start=start,
            goal=goal,
            exits=exits,
            show=False,
        )

        if goal and agent_node == goal:
            ax.set_title(f"GOAL REACHED at Step {step}")
            plt.pause(1.5)
            print("GOAL REACHED")
            break

        ax.set_title(f"Step {step} - {status}")
        plt.pause(speed)

    plt.ioff()
    plt.show()