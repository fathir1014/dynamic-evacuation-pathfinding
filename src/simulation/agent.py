import math


class Agent:
    def __init__(self, start_node):
        self.node = start_node
        self.pos = [float(start_node.x), float(start_node.y)]
        self.path = []
        self.target_index = 0
        self.speed = 1.0
        self.health = 100.0

    def set_path(self, path):
        if not path:
            return

        self.path = path
        closest_index = 0
        min_dist = float("inf")

        for i, node in enumerate(path):
            dx = node.x - self.pos[0]
            dy = node.y - self.pos[1]
            dist = dx * dx + dy * dy

            if dist < min_dist:
                min_dist = dist
                closest_index = i

        if min_dist < 0.03 and closest_index + 1 < len(path):
            self.target_index = closest_index + 1
        else:
            self.target_index = closest_index

    def update(self):
        if not self.path or self.target_index >= len(self.path):
            return

        target_node = self.path[self.target_index]
        dx = target_node.x - self.pos[0]
        dy = target_node.y - self.pos[1]
        dist = math.sqrt(dx * dx + dy * dy)

        if dist < 0.15:
            self.pos[0] = float(target_node.x)
            self.pos[1] = float(target_node.y)
            self.node = target_node
            self.target_index += 1
            return

        if self.speed >= dist:
            self.pos[0] = float(target_node.x)
            self.pos[1] = float(target_node.y)
            self.node = target_node
            self.target_index += 1
            return

        self.pos[0] += (dx / dist) * self.speed
        self.pos[1] += (dy / dist) * self.speed

    def get_node(self):
        return self.node

    def get_pos(self):
        return self.pos

    def apply_damage(self, amount):
        self.health = max(0.0, self.health - amount)

    def is_alive(self):
        return self.health > 0