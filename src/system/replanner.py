from core.astar import astar
from system.validator import is_path_valid


def plan_path(grid, start, goal, cache):

    key = (start.x, start.y, goal.x, goal.y)

    # 🔥 ambil cache dulu (biar ga undefined)
    cached_path = cache.get(key) if cache.has(key) else None

    # 🔥 kalau ada cache & masih valid
    if cached_path and is_path_valid(cached_path):
        return cached_path, "CACHE_HIT"

    # 🔥 kalau cache ada tapi rusak → REPLAN
    if cached_path:
        new_path = astar(grid, start, goal)
        cache.set(key, new_path)
        return new_path, "REPLAN"

    # 🔥 kalau belum pernah ada → NEW
    new_path = astar(grid, start, goal)
    cache.set(key, new_path)
    return new_path, "NEW_PATH"