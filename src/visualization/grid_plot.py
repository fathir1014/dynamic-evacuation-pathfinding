import matplotlib.patches as mpatches
import matplotlib.patches as patches
import matplotlib.pyplot as plt


def plot_grid(
    grid,
    path=None,
    full_path=None,
    agent_pos=None,
    start=None,
    goal=None,
    exits=None,
    show=True,
):
    ax = plt.gca()
    ax.clear()

    for x in range(grid.width):
        for y in range(grid.height):
            node = grid.get_node(x, y)

            if not node.base_walkable:
                color = "#2b2b2b"
            elif not node.walkable:
                color = "#7a3b22"
            elif node.smoke > 0:
                color = "#bfc3c7"
            elif node.liquid > 0:
                color = "#74b9ff"
            elif node.crowd > 0:
                color = "#c77dff"
            else:
                color = "#f7f2df"

            rect = patches.Rectangle(
                (x - 0.5, y - 0.5),
                1,
                1,
                linewidth=0.15,
                edgecolor="#e0e0e0",
                facecolor=color,
            )
            ax.add_patch(rect)

    if exits:
        for ex in exits:
            x, y = ex
            ax.add_patch(
                patches.Rectangle(
                    (x - 0.5, y - 0.5),
                    1,
                    1,
                    facecolor="#12b76a",
                    alpha=0.9,
                    zorder=5,
                )
            )
            ax.text(
                x,
                y,
                "EXIT",
                ha="center",
                va="center",
                fontsize=5,
                color="white",
                weight="bold",
                zorder=6,
            )

    if full_path:
        xs = [node.x for node in full_path]
        ys = [node.y for node in full_path]
        ax.plot(xs, ys, linestyle="--", linewidth=1.5, color="#1d4ed8", alpha=0.5)

    if path:
        xs = [node.x for node in path]
        ys = [node.y for node in path]
        ax.plot(xs, ys, linewidth=3, color="#22c55e", zorder=10)

    if agent_pos:
        ax.scatter(
            agent_pos[0],
            agent_pos[1],
            s=180,
            color="#06b6d4",
            edgecolors="black",
            zorder=20,
        )

    if start:
        ax.scatter(start.x, start.y, s=130, color="#f59e0b", zorder=20)

    if goal:
        ax.scatter(goal.x, goal.y, s=180, color="#ef4444", marker="X", zorder=25)

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(-1, grid.width)
    ax.set_ylim(-1, grid.height)
    ax.set_aspect("equal")

    legend = [
        mpatches.Patch(color="#2b2b2b", label="Static wall"),
        mpatches.Patch(color="#f7f2df", label="Safe area"),
        mpatches.Patch(color="#7a3b22", label="Obstacle / barrier"),
        mpatches.Patch(color="#bfc3c7", label="Smoke"),
        mpatches.Patch(color="#74b9ff", label="Liquid"),
        mpatches.Patch(color="#c77dff", label="Crowd"),
        mpatches.Patch(color="#12b76a", label="Exit"),
    ]
    ax.legend(
        handles=legend,
        loc="center left",
        bbox_to_anchor=(1.02, 0.5),
        borderaxespad=0,
        fontsize=8,
    )

    if show:
        plt.tight_layout()
        plt.show()