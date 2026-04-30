import time
import random
import matplotlib.pyplot as plt

from system.replanner import plan_path
from visualization.grid_plot import plot_grid


MOVE_PER_STEP = 3
REPLAN_INTERVAL = 3


def update_environment(grid, start, goal, change_prob=0.03):
    for x in range(grid.width):
        for y in range(grid.height):
            node = grid.get_node(x, y)

            if node == start or node == goal:
                continue

            if random.random() < change_prob:
                node.walkable = random.random() > 0.2

            node.smoke = max(0, node.smoke + random.randint(-1, 1))
            node.debris = max(0, node.debris + random.randint(-1, 1))
            node.crowd = max(0, node.crowd + random.randint(-1, 1))


def run_simulation(grid, start, goal, cache, steps, log_fn):

    plt.ion()
    plt.figure(figsize=(6, 6))

    agent_position = start   # state asli agent
    current_path = None
    current_index = 0

    for step in range(1, steps + 1):

        print(f"\n=== STEP {step} ===")

        update_environment(grid, start, goal)

        # REPLAN kondisi:
        need_replan = (
            current_path is None or
            current_index >= len(current_path) or
            step % REPLAN_INTERVAL == 0
        )

        if need_replan:

            t0 = time.perf_counter()
            path, status = plan_path(grid, agent_position, goal, cache)
            t1 = time.perf_counter()

            exec_time = t1 - t0
            log_fn(step, status, exec_time)

            if path:
                current_path = path
                current_index = 0
            else:
                print("NO PATH")
                current_path = None

        else:
            status = "MOVE_ONLY"

        print(f"STATUS: {status}")

        # 🚶 GERAK
        if current_path:

            for _ in range(MOVE_PER_STEP):

                if current_index >= len(current_path):
                    break

                next_node = current_path[current_index]

                if not next_node.walkable:
                    print("🚧 BLOCKED → FORCE REPLAN")
                    current_path = None
                    break

                # UPDATE posisi agent
                agent_position = next_node

                current_index += 1

            partial_path = current_path[:current_index] if current_path else None

        else:
            partial_path = None

        # RENDER
        plt.clf()

        plot_grid(
            grid,
            path=partial_path,
            full_path=current_path,
            show=False
        )

        # FINISH
        if agent_position == goal:
            plt.title(f"GOAL REACHED at Step {step}")
            plt.pause(2)
            print("GOAL REACHED")
            break

        plt.title(f"Step {step} - {status}")
        plt.pause(0.9)

    plt.ioff()
    plt.show()