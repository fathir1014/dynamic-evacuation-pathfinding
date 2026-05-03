class Node:
    def __init__(self, x, y, walkable=True):
        self.x = x
        self.y = y
        self.walkable = walkable
        self.base_walkable = walkable

        self.smoke = 0
        self.debris = 0
        self.liquid = 0
        self.crowd = 0
        self.hazard = None

    def __repr__(self):
        return f"Node({self.x},{self.y})"

    @property
    def pos(self):
        return (self.x, self.y)

    def reset_dynamic(self):
        self.walkable = self.base_walkable
        self.smoke = 0
        self.debris = 0
        self.liquid = 0
        self.crowd = 0
        self.hazard = None

class Node:
    def __init__(self, x, y, walkable=True):
        self.x = x
        self.y = y
        self.walkable = walkable
        self.base_walkable = walkable

        self.smoke = 0
        self.debris = 0
        self.liquid = 0
        self.crowd = 0
        self.hazard = None

    def __repr__(self):
        return f"Node({self.x},{self.y})"

    @property
    def pos(self):
        return (self.x, self.y)

    def reset_dynamic(self):
        self.walkable = self.base_walkable
        self.smoke = 0
        self.debris = 0
        self.liquid = 0
        self.crowd = 0
        self.hazard = None


class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.nodes = [[Node(x, y) for y in range(height)] for x in range(width)]

    def get_node(self, x, y):
        return self.nodes[x][y]

    def in_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def set_wall(self, x, y):
        node = self.get_node(x, y)
        node.walkable = False
        node.base_walkable = False

    def set_floor(self, x, y):
        node = self.get_node(x, y)
        node.walkable = True
        node.base_walkable = True

    def reset_dynamic(self):
        for x in range(self.width):
            for y in range(self.height):
                self.get_node(x, y).reset_dynamic()

    def walkable_nodes(self):
        nodes = []
        for x in range(self.width):
            for y in range(self.height):
                node = self.get_node(x, y)
                if node.walkable:
                    nodes.append(node)
        return nodes

    def get_neighbors(self, node):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        neighbors = []

        for dx, dy in directions:
            nx, ny = node.x + dx, node.y + dy
            if self.in_bounds(nx, ny):
                neighbor = self.nodes[nx][ny]
                if neighbor.walkable:
                    neighbors.append(neighbor)

        return neighbors