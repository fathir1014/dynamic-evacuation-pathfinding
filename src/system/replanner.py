from core.astar import astar_with_fallback, find_best_exit_path
from core.risk import calculate_risk
from system.validator import is_path_valid


def path_avg_risk(path):
    if not path:
        return float("inf")
    return sum(calculate_risk(node) for node in path) / len(path)


def plan_path(grid, start, goal, cache):
    key = (start.x, start.y, goal.x, goal.y)
    cached_path = cache.get(key, grid) if cache.has(key) else None

    if cached_path and is_path_valid(cached_path, start):
        start_index = cached_path.index(start)
        trimmed = cached_path[start_index:]
        if path_avg_risk(trimmed) <= 4.5:
            return trimmed, goal, "CACHE_HIT"

    path, status = astar_with_fallback(grid, start, goal)
    if path and status == "SAFE_PATH":
        cache.set(key, path)

    return path, goal, status


def plan_best_path(grid, start, exits, cache):
    best_cached = None
    best_cached_goal = None
    best_cached_cost = float("inf")

    for exit_pos in exits:
        goal = grid.get_node(exit_pos[0], exit_pos[1])
        key = (start.x, start.y, goal.x, goal.y)
        cached_path = cache.get(key, grid) if cache.has(key) else None

        if cached_path and is_path_valid(cached_path, start):
            start_index = cached_path.index(start)
            trimmed = cached_path[start_index:]
            cost = len(trimmed) + path_avg_risk(trimmed) * 2
            if cost < best_cached_cost:
                best_cached = trimmed
                best_cached_goal = goal
                best_cached_cost = cost

    if best_cached is not None:
        return best_cached, best_cached_goal, "CACHE_HIT"

    path, goal, status = find_best_exit_path(grid, start, exits)
    if path and goal and status == "SAFE_PATH":
        key = (start.x, start.y, goal.x, goal.y)
        cache.set(key, path)

    return path, goal, status
