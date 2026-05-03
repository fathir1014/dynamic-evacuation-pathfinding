import heapq
from collections import deque

from core.risk import calculate_risk


def heuristic(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)


def astar(grid, start, goal, risk_weight=8.0, panic_mode=False):
    if not start.walkable or not goal.walkable:
        return None

    open_set = []
    counter = 0
    heapq.heappush(open_set, (0, counter, start))

    came_from = {}
    g_score = {start: 0}
    visited = set()

    while open_set:
        _, _, current = heapq.heappop(open_set)

        if current == goal:
            return reconstruct_path(came_from, current)

        if current in visited:
            continue
        visited.add(current)

        for neighbor in grid.get_neighbors(current):
            risk = calculate_risk(neighbor)

            if not panic_mode and risk > 0:
                continue

            hazard_penalty = 0 if not neighbor.hazard else 25
            tentative_g = g_score[current] + 1 + (risk_weight * risk) + hazard_penalty

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g
                counter += 1
                priority = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (priority, counter, neighbor))
                came_from[neighbor] = current

    return None


def astar_no_risk(grid, start, goal):
    if not start.walkable or not goal.walkable:
        return False

    queue = deque([start])
    visited = {start}

    while queue:
        current = queue.popleft()

        if current == goal:
            return True

        for neighbor in grid.get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return False


def astar_with_fallback(grid, start, goal):
    path = astar(grid, start, goal, panic_mode=False)
    if path:
        return path, "SAFE_PATH"

    path = astar(grid, start, goal, panic_mode=True)
    if path:
        return path, "PANIC_PATH"

    return None, "NO_PATH"


def find_best_exit_path(grid, start, exits, risk_weight=2.0):
    best_path = None
    best_goal = None
    best_status = "NO_PATH"
    best_cost = float("inf")

    for exit_pos in exits:
        goal = grid.get_node(exit_pos[0], exit_pos[1])
        path, status = astar_with_fallback(grid, start, goal)
        if not path:
            continue

        risk_cost = sum(calculate_risk(node) for node in path) * risk_weight
        panic_penalty = 100 if status == "PANIC_PATH" else 0
        cost = len(path) + risk_cost + panic_penalty

        if cost < best_cost:
            best_path = path
            best_goal = goal
            best_status = status
            best_cost = cost

    return best_path, best_goal, best_status


def reconstruct_path(came_from, current):
    path = [current]

    while current in came_from:
        current = came_from[current]
        path.append(current)

    path.reverse()
    return path