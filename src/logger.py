def generate_report(allocation, maximum, need, available, safe, sequence):
    with open("report.txt", "w") as f:
        f.write("Deadlock Prevention & Recovery Report\n\n")
        f.write("Allocation Matrix:\n")
        for row in allocation:
            f.write(str(row) + "\n")

        f.write("\nMaximum Matrix:\n")
        for row in maximum:
            f.write(str(row) + "\n")

        f.write("\nNeed Matrix:\n")
        for row in need:
            f.write(str(row) + "\n")

        f.write("\nAvailable Resources:\n")
        f.write(str(available) + "\n")

        if safe:
            f.write("\nSystem is SAFE.\n")
            f.write("Safe Sequence: " + str(sequence))
        else:
            f.write("\nSystem is UNSAFE.\n")

    print("Report generated as report.txt")