def get_user_input():
    print("\n===== User Input Simulation =====")

    n = int(input("Enter number of processes: "))
    m = int(input("Enter number of resources: "))

    print("\nEnter Allocation Matrix:")
    allocation = []
    for i in range(n):
        row = list(map(int, input(f"Allocation for P{i}: ").split()))
        allocation.append(row)

    print("\nEnter Maximum Matrix:")
    maximum = []
    for i in range(n):
        row = list(map(int, input(f"Maximum for P{i}: ").split()))
        maximum.append(row)

    print("\nEnter Available Resources:")
    available = list(map(int, input("Available: ").split()))

    return allocation, maximum, available