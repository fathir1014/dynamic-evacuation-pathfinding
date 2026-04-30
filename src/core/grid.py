# src/core/grid.py

class Node:
    def __init__(self, x, y, walkable=True):
        self.x = x
        self.y = y
        self.walkable = walkable

        # risk factors
        self.smoke = 0
        self.debris = 0
        self.liquid = 0
        self.crowd = 0

    def __repr__(self):
        return f"Node({self.x},{self.y})"


class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.nodes = [[Node(x, y) for y in range(height)] for x in range(width)]

    def get_node(self, x, y):
        return self.nodes[x][y]

    def get_neighbors(self, node):
        directions = [(0,1),(1,0),(0,-1),(-1,0)]
        neighbors = []

        for dx, dy in directions:
            nx, ny = node.x + dx, node.y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                neighbor = self.nodes[nx][ny]
                if neighbor.walkable:
                    neighbors.append(neighbor)

        return neighbors