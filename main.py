from src.bankers import BankersAlgorithm
from src.simulation import get_user_input
from src.recovery import Recovery
from src.visualization import ResourceAllocationGraph
from src.detection import DeadlockDetection
from src.logger import generate_report
from src.waitfor_visualization import WaitForGraphVisualizer

import time
import copy


def print_matrix(name, matrix):
    print(f"\n{name}:")
    for row in matrix:
        print(row)


def main():
    print("====================================")
    print(" Deadlock Prevention & Recovery Toolkit ")
    print("====================================")

    print("\nSelect Mode:")
    print("1. Prevention Only (Banker's Algorithm)")
    print("2. Detection Only")
    print("3. Full Prevention + Detection + Recovery (with Strategy Comparison)")
    print("4. Exit")

    mode = input("\nEnter your choice (1-4): ")

    if mode == "4":
        print("Exiting Toolkit...")
        return

    choice = input("\nUse sample data? (y/n): ").lower()

    if choice == 'y':
        allocation = [
            [0, 1, 0],
            [2, 0, 0],
            [3, 0, 2],
            [2, 1, 1],
            [0, 0, 2]
        ]

        maximum = [
            [7, 5, 3],
            [3, 2, 2],
            [9, 0, 2],
            [2, 2, 2],
            [4, 3, 3]
        ]

        available = [3, 3, 2]

    else:
        allocation, maximum, available = get_user_input()

    # ------------------------------
    # MODE 1: PREVENTION ONLY
    # ------------------------------
    if mode == "1":
        banker = BankersAlgorithm(allocation, maximum, available)
        safe, sequence = banker.is_safe()

        print_matrix("Allocation Matrix", allocation)
        print_matrix("Maximum Matrix", maximum)
        print_matrix("Need Matrix", banker.need)

        if safe:
            print("\nSystem is SAFE.")
            print("Safe Sequence:", sequence)
        else:
            print("\nSystem is UNSAFE.")

    # ------------------------------
    # MODE 2: DETECTION ONLY
    # ------------------------------
    elif mode == "2":
        detector = DeadlockDetection(allocation, available)
        wait_graph = detector.build_wait_for_graph()

        cycle_found, deadlocked_nodes = detector.detect_cycle(wait_graph)

        if cycle_found:
            print("\nDeadlock detected!")
            print("Deadlocked Processes:", deadlocked_nodes)

            print("\nDisplaying Wait-For Graph...")
            wfg = WaitForGraphVisualizer(wait_graph, deadlocked_nodes)
            wfg.draw()
        else:
            print("\nNo Deadlock detected.")

    # ------------------------------
    # MODE 3: FULL SYSTEM + COMPARISON
    # ------------------------------
    elif mode == "3":

        # Prevention check
        start_time = time.time()
        banker = BankersAlgorithm(allocation, maximum, available)
        safe, sequence = banker.is_safe()
        end_time = time.time()

        print_matrix("Allocation Matrix", allocation)
        print_matrix("Maximum Matrix", maximum)
        print_matrix("Need Matrix", banker.need)

        print("\nExecution Time:", round(end_time - start_time, 6), "seconds")

        print("\nDisplaying Resource Allocation Graph...")
        rag = ResourceAllocationGraph(allocation)
        rag.draw_graph()

        if safe:
            print("\nSystem is SAFE.")
            print("Safe Sequence:", sequence)

        else:
            print("\nSystem is UNSAFE.")

            # Detection
            detector = DeadlockDetection(allocation, available)
            wait_graph = detector.build_wait_for_graph()
            cycle_found, deadlocked_nodes = detector.detect_cycle(wait_graph)

            if cycle_found:
                print("Deadlock detected!")
                print("Deadlocked Processes:", deadlocked_nodes)

                print("\nDisplaying Wait-For Graph...")
                wfg = WaitForGraphVisualizer(wait_graph, deadlocked_nodes)
                wfg.draw()

            # -----------------------------
            # STRATEGY COMPARISON
            # -----------------------------
            print("\nRunning Recovery Strategy Comparison...\n")

            strategies = {
                "1": "MAX allocated resources",
                "2": "MIN allocated resources",
                "3": "MAX need"
            }

            results = {}

            for key, name in strategies.items():
                print(f"Testing Strategy {key}: {name}")

                alloc_copy = copy.deepcopy(allocation)
                avail_copy = copy.deepcopy(available)

                recovery = Recovery(alloc_copy, maximum, avail_copy)

                start = time.time()
                pid = recovery.find_process(key)
                recovery.terminate_process(pid)

                banker_test = BankersAlgorithm(alloc_copy, maximum, avail_copy)
                safe_test, seq_test = banker_test.is_safe()
                end = time.time()

                results[key] = {
                    "strategy": name,
                    "terminated": pid,
                    "safe": safe_test,
                    "sequence": seq_test,
                    "time": end - start
                }

                print(f"Terminated Process: P{pid}")
                print(f"Recovered: {safe_test}")
                print(f"Execution Time: {end - start:.6f} sec\n")

            # Determine Best Strategy
            best_strategy = None
            best_time = float('inf')

            for key, result in results.items():
                if result["safe"] and result["time"] < best_time:
                    best_time = result["time"]
                    best_strategy = key

            if best_strategy:
                print("====================================")
                print("Best Strategy:", results[best_strategy]["strategy"])
                print("Recovered Sequence:", results[best_strategy]["sequence"])
                print("====================================")
            else:
                print("No strategy successfully recovered the system.")

        # Generate report for original run
        generate_report(allocation, maximum, banker.need, available, safe, sequence)

    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()