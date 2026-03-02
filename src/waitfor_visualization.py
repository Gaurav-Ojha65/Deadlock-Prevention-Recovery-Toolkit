import networkx as nx
import matplotlib.pyplot as plt


class WaitForGraphVisualizer:
    def __init__(self, wait_graph, deadlocked_nodes):
        self.wait_graph = wait_graph
        self.deadlocked_nodes = deadlocked_nodes

    def draw(self):
        G = nx.DiGraph()

        for process in self.wait_graph:
            G.add_node(f"P{process}")

        for process, neighbors in self.wait_graph.items():
            for neighbor in neighbors:
                G.add_edge(f"P{process}", f"P{neighbor}")

        pos = nx.spring_layout(G, seed=42, k=1.5)

        plt.figure(figsize=(9, 7))

        node_colors = []
        for node in G.nodes:
            pid = int(node[1:])
            if pid in self.deadlocked_nodes:
                node_colors.append("#E53935")  # Red
            else:
                node_colors.append("#43A047")  # Green

        nx.draw_networkx_nodes(
            G, pos,
            node_color=node_colors,
            node_size=2800,
            edgecolors="black",
            linewidths=1.5
        )

        nx.draw_networkx_edges(
            G, pos,
            arrows=True,
            arrowstyle='-|>',
            width=2.5,
            connectionstyle='arc3,rad=0.1'
        )

        nx.draw_networkx_labels(
            G, pos,
            font_size=12,
            font_weight="bold",
            font_color="white"
        )

        # Legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='#E53935', edgecolor='black', label='Deadlocked Process'),
            Patch(facecolor='#43A047', edgecolor='black', label='Safe Process')
        ]

        plt.legend(handles=legend_elements, loc="upper right")

        plt.title("Wait-For Graph (Deadlock Highlighted)", fontsize=15)
        plt.axis("off")
        plt.tight_layout()

        plt.savefig("wait_for_graph.png", dpi=300)
        plt.show()