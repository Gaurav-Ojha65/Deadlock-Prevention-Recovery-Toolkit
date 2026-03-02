import networkx as nx
import matplotlib.pyplot as plt


class ResourceAllocationGraph:
    def __init__(self, allocation):
        self.allocation = allocation
        self.num_processes = len(allocation)
        self.num_resources = len(allocation[0])

    def draw_graph(self):
        G = nx.DiGraph()

        for i in range(self.num_processes):
            G.add_node(f"P{i}", type="process")

        for j in range(self.num_resources):
            G.add_node(f"R{j}", type="resource")

        for i in range(self.num_processes):
            for j in range(self.num_resources):
                if self.allocation[i][j] > 0:
                    G.add_edge(f"R{j}", f"P{i}",
                               label=str(self.allocation[i][j]))

        pos = nx.spring_layout(G, seed=42, k=1.3)

        process_nodes = [n for n in G.nodes if G.nodes[n]["type"] == "process"]
        resource_nodes = [n for n in G.nodes if G.nodes[n]["type"] == "resource"]

        plt.figure(figsize=(11, 8))

        nx.draw_networkx_nodes(
            G, pos,
            nodelist=process_nodes,
            node_color="#4CAF50",
            node_size=3000,
            node_shape="o",
            edgecolors="black",
            linewidths=1.5
        )

        nx.draw_networkx_nodes(
            G, pos,
            nodelist=resource_nodes,
            node_color="#1E88E5",
            node_size=3000,
            node_shape="s",
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

        edge_labels = nx.get_edge_attributes(G, "label")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='#4CAF50', edgecolor='black', label='Process'),
            Patch(facecolor='#1E88E5', edgecolor='black', label='Resource')
        ]

        plt.legend(handles=legend_elements, loc="upper right")

        plt.title("Resource Allocation Graph (RAG)", fontsize=15)
        plt.axis("off")
        plt.tight_layout()

        plt.savefig("resource_allocation_graph.png", dpi=300)
        plt.show()