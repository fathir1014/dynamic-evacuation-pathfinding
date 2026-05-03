from core.astar import astar, astar_no_risk
from core.risk import calculate_risk


def is_path_available(grid, start, exits):
    for exit_pos in exits:
        goal = grid.get_node(exit_pos[0], exit_pos[1])
        if astar_no_risk(grid, start, goal):
            return True
    return False


def is_safe_path_available(grid, start, exits):
    for exit_pos in exits:
        goal = grid.get_node(exit_pos[0], exit_pos[1])
        if astar(grid, start, goal, panic_mode=False):
            return True
    return False


def is_path_valid(path, current_node=None, allow_risk=False, max_node_risk=7.0, max_avg_risk=4.5):
    if not path:
        return False

    start_index = 0
    if current_node is not None and current_node in path:
        start_index = path.index(current_node)

    remaining = path[start_index:]
    if not remaining:
        return False

    total_risk = 0
    for node in remaining:
        if not node.walkable:
            return False

        risk = calculate_risk(node)
        if not allow_risk and risk > 0:
            return False

        if risk > max_node_risk:
            return False

        total_risk += risk

    return (total_risk / len(remaining)) <= max_avg_risk