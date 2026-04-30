from core.astar import astar
from system.validator import is_path_valid


def plan_path(grid, start, goal, cache):

    key = (goal.x, goal.y) 

    cached_path = cache.get(key) if cache.has(key) else None

    if cached_path:

        if is_path_valid(cached_path, start):

            try:
                start_index = cached_path.index(start)
                return cached_path[start_index:], "CACHE_HIT"
            except ValueError:
                pass  

        new_path = astar(grid, start, goal)
        cache.set(key, new_path)
        return new_path, "REPLAN"

    new_path = astar(grid, start, goal)
    cache.set(key, new_path)
    return new_path, "NEW_PATH"