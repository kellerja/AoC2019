def fuel_required(mass):
    fuel = int(mass / 3) - 2
    if fuel < 0:
        return 0
    return fuel + fuel_required(fuel)


if __name__ == '__main__':
    total_fuel = 0
    with open("input.txt", "r") as inputFile:
        for inputLine in inputFile:
            total_fuel += fuel_required(int(inputLine.strip()))
    with open("output.txt", "w") as outputFile:
        outputFile.write(str(total_fuel))
        outputFile.write("\n")
