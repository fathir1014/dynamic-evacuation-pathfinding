def is_path_valid(path):
    if not path:
        return False

    for node in path:
        if not node.walkable:
            return False

    return True