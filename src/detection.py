class DeadlockDetection:
    def __init__(self, allocation, available):
        self.allocation = allocation
        self.available = available
        self.num_processes = len(allocation)

    def build_wait_for_graph(self):
        graph = {i: [] for i in range(self.num_processes)}

        for i in range(self.num_processes):
            for j in range(self.num_processes):
                if i != j:
                    # If j holds resources and none are available
                    if any(self.allocation[j][k] > 0 and self.available[k] == 0
                           for k in range(len(self.available))):
                        graph[i].append(j)

        return graph

    def detect_cycle(self, graph):
        visited = set()
        stack = []
        cycle_nodes = set()

        def dfs(node):
            if node in stack:
                cycle_nodes.update(stack[stack.index(node):])
                return True

            if node in visited:
                return False

            visited.add(node)
            stack.append(node)

            for neighbor in graph[node]:
                if dfs(neighbor):
                    return True

            stack.pop()
            return False

        for node in graph:
            if dfs(node):
                return True, cycle_nodes

        return False, set()