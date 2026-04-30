def is_path_valid(path, current_node=None):
    if not path:
        return False

    if current_node and current_node in path:
        start_index = path.index(current_node)
    else:
        start_index = 0

    for node in path[start_index:]:
        if not node.walkable:
            return False

    return True