class BankersAlgorithm:
    def __init__(self, allocation, maximum, available):
        self.allocation = allocation
        self.maximum = maximum
        self.available = available
        self.num_processes = len(allocation)
        self.num_resources = len(available)
        self.need = self.calculate_need()

    def calculate_need(self):
        need = []
        for i in range(self.num_processes):
            row = []
            for j in range(self.num_resources):
                row.append(self.maximum[i][j] - self.allocation[i][j])
            need.append(row)
        return need

    def is_safe(self):
        work = self.available.copy()
        finish = [False] * self.num_processes
        safe_sequence = []

        while len(safe_sequence) < self.num_processes:
            allocated_in_this_round = False

            for i in range(self.num_processes):
                if not finish[i]:
                    if all(self.need[i][j] <= work[j] for j in range(self.num_resources)):
                        for j in range(self.num_resources):
                            work[j] += self.allocation[i][j]
                        safe_sequence.append(i)
                        finish[i] = True
                        allocated_in_this_round = True

            if not allocated_in_this_round:
                return False, []

        return True, safe_sequence