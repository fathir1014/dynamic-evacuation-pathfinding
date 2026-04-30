import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches


def plot_grid(grid, path=None, full_path=None, show=True):

    # 🔥 RGB biar bisa multi warna
    data = np.zeros((grid.height, grid.width, 3))

    for x in range(grid.width):
        for y in range(grid.height):
            node = grid.get_node(x, y)

            if not node.walkable:
                data[y][x] = [0, 0, 0]  # ⬛ obstacle (hitam)

            else:
                # 🔥 PRIORITAS warna (biar ga tabrakan)
                if node.smoke > 0:
                    data[y][x] = [0.5, 0.5, 0.5]  # abu (smoke)

                elif node.debris > 0:
                    data[y][x] = [0.6, 0.3, 0.1]  # coklat (debris)

                elif node.crowd > 0:
                    data[y][x] = [0.6, 0, 0.6]  # ungu (crowd)

                else:
                    data[y][x] = [1, 1, 1]  # putih (aman)

    plt.imshow(data, origin="lower")

    # 🔵 cached / planned path
    if full_path:
        xs = [n.x for n in full_path]
        ys = [n.y for n in full_path]
        plt.plot(xs, ys, linestyle="--", linewidth=1, color="blue", label="Planned Path")

    # 🟢 path yang sedang ditempuh
    if path:
        xs = [n.x for n in path]
        ys = [n.y for n in path]
        plt.plot(xs, ys, linewidth=2, color="green", label="Agent Path")

        # 🔵 posisi agent
        x = path[-1].x
        y = path[-1].y
        plt.scatter(x, y, s=100, color="cyan", label="Agent")

    # 🟡 start
    plt.scatter(0, 0, s=150, marker="o", color="orange", label="Start")

    # 🔴 goal
    plt.scatter(grid.width - 1, grid.height - 1, s=150, marker="x", color="red", label="Goal")

    # 🔥 LEGEND (biar dosen ngerti langsung)
    legend_patches = [
        mpatches.Patch(color='black', label='Blocked'),
        mpatches.Patch(color='gray', label='Smoke'),
        mpatches.Patch(color='brown', label='Debris'),
        mpatches.Patch(color='purple', label='Crowd'),
    ]

    plt.legend(handles=legend_patches, loc='upper left')

    plt.grid(True)

    if show:
        plt.show()

def get_neighbors(self, node):
    neighbors = []

    directions = [(1,0), (-1,0), (0,1), (0,-1)]

    for dx, dy in directions:
        x = node.x + dx
        y = node.y + dy

        if 0 <= x < self.width and 0 <= y < self.height:
            neighbor = self.get_node(x, y)

            # 🔥 FIX UTAMA: filter obstacle
            if neighbor.walkable:
                neighbors.append(neighbor)

    return neighbors