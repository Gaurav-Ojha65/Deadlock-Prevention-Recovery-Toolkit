class Recovery:
    def __init__(self, allocation, maximum, available):
        self.allocation = allocation
        self.maximum = maximum
        self.available = available
        self.num_processes = len(allocation)

    def find_process(self, strategy):
        if strategy == "1":
            # Max allocated resources
            values = [sum(row) for row in self.allocation]
            return values.index(max(values))

        elif strategy == "2":
            # Min allocated resources
            values = [sum(row) for row in self.allocation]
            return values.index(min(values))

        elif strategy == "3":
            # Max need
            needs = []
            for i in range(self.num_processes):
                need = sum(self.maximum[i][j] - self.allocation[i][j]
                           for j in range(len(self.available)))
                needs.append(need)
            return needs.index(max(needs))

        else:
            print("Invalid strategy. Defaulting to MAX allocated.")
            values = [sum(row) for row in self.allocation]
            return values.index(max(values))

    def terminate_process(self, process_id):
        print(f"\nTerminating Process P{process_id}...")

        for i in range(len(self.available)):
            self.available[i] += self.allocation[process_id][i]
            self.allocation[process_id][i] = 0

        print("Resources after recovery:", self.available)