# src/core/astar.py

import heapq
from core.risk import calculate_risk


def heuristic(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)


def astar(grid, start, goal, risk_weight=1.0):
    open_set = []
    counter = 0

    heapq.heappush(open_set, (0, counter, start))

    came_from = {}
    g_score = {start: 0}

    while open_set:
        _, _, current = heapq.heappop(open_set)

        if current == goal:
            return reconstruct_path(came_from, current)

        for neighbor in grid.get_neighbors(current):

            # 🔥 FIX: jangan masuk obstacle
            if not neighbor.walkable:
                continue

            risk = calculate_risk(neighbor)
            tentative_g = g_score[current] + 1 + risk_weight * risk

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g
                f = tentative_g + heuristic(neighbor, goal)

                counter += 1
                heapq.heappush(open_set, (f, counter, neighbor))

                came_from[neighbor] = current

    return None

def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path