from src.bankers import BankersAlgorithm
from src.simulation import get_user_input


def print_matrix(name, matrix):
    print(f"\n{name}:")
    for row in matrix:
        print(row)


def main():
    print("====================================")
    print(" Deadlock Prevention & Recovery Toolkit ")
    print("====================================")

    choice = input("Use sample data? (y/n): ").lower()

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

    banker = BankersAlgorithm(allocation, maximum, available)
    safe, sequence = banker.is_safe()

    print_matrix("Allocation Matrix", allocation)
    print_matrix("Maximum Matrix", maximum)
    print_matrix("Need Matrix", banker.need)

    print("\nAvailable Resources:", available)

    if safe:
        print("\nSystem is in SAFE state.")
        print("Safe sequence:", sequence)
    else:
        print("\nSystem is in UNSAFE state.")


if __name__ == "__main__":
    main()