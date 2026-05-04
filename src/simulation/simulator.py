import time

import matplotlib.pyplot as plt

from core.astar import astar, find_best_exit_path
from core.risk import calculate_health_damage
from simulation.agent import Agent
from system.replanner import plan_best_path
from system.validator import is_path_valid
from utils.building import add_hazards
from visualization.grid_plot import plot_grid


HAZARD_CHANGE_INTERVAL = 5
STEP_DAMAGE = 0.08


def run_simulation(
    grid,
    start,
    exits,
    cache,
    steps,
    log_fn,
    speed,
    mode="HYBRID",
    run_name=None,
    visualize=True,
):
    fig = None
    ax = None
    if visualize:
        plt.ion()
        fig, ax = plt.subplots(figsize=(14, 7))
        fig.subplots_adjust(right=0.82)

    agent = Agent(start)
    current_path = None
    goal = None
    results = []
    run_name = run_name or mode

    for step in range(1, steps + 1):
        status = "MOVE_ONLY"
        exec_time = 0.0

        print(f"\n[{run_name}] === STEP {step} ===")

        if step > 1 and step % HAZARD_CHANGE_INTERVAL == 0:
            changed = add_hazards(grid, agent.get_node(), exits)
            if cache:
                current_path = None
                cache.clear()
            print("HAZARD_CHANGED" if changed else "HAZARD_RESET_FALLBACK")

        if mode == "HYBRID" and current_path and not is_path_valid(current_path, agent.get_node()):
            current_path = None

        need_replan = current_path is None or agent.target_index >= len(current_path)

        if need_replan:
            t0 = time.perf_counter()

            if mode == "ASTAR_ONLY":
                path, goal, status = plan_astar_only(grid, agent.get_node(), exits)
            else:
                path, goal, status = plan_best_path(grid, agent.get_node(), exits, cache)

            exec_time = time.perf_counter() - t0

            if path:
                current_path = path
                agent.set_path(path)
            else:
                current_path = None

        print(f"STATUS: {status}")

        agent.update()
        damage = STEP_DAMAGE + calculate_health_damage(agent.get_node())
        agent.apply_damage(damage)

        agent_node = agent.get_node()
        agent_pos = agent.get_pos()
        reached_goal = goal is not None and agent_node == goal

        row = {
            "run": run_name,
            "mode": mode,
            "step": step,
            "status": status,
            "time": exec_time,
            "health": round(agent.health, 3),
            "damage": round(damage, 3),
            "x": agent_node.x,
            "y": agent_node.y,
            "goal_x": goal.x if goal else "",
            "goal_y": goal.y if goal else "",
            "reached_goal": reached_goal,
        }
        results.append(row)
        log_fn(row)

        if visualize:
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
            ax.set_title(f"{run_name} - Step {step} - {status} - Health {agent.health:.1f}")
            plt.pause(speed)

        if reached_goal:
            print(f"GOAL REACHED with health {agent.health:.1f}")
            break

        if not agent.is_alive():
            print("AGENT FAILED: health reached 0")
            break

    if visualize:
        plt.ioff()
        plt.show()

    return results


def plan_astar_only(grid, start, exits):
    best_path = None
    best_goal = None
    best_cost = float("inf")

    for exit_pos in exits:
        goal = grid.get_node(exit_pos[0], exit_pos[1])
        path = astar(grid, start, goal, risk_weight=0, panic_mode=True)
        if not path:
            continue

        if len(path) < best_cost:
            best_path = path
            best_goal = goal
            best_cost = len(path)

    if best_path:
        return best_path, best_goal, "ASTAR_ONLY"

    path, goal, status = find_best_exit_path(grid, start, exits)
    return path, goal, status
