if __name__ == '__main__':
    total_fuel = 0
    with open('./input', 'r') as f:
        for line in f:
            module_mass = int(line)
            module_fuel = (module_mass // 3) - 2
            total_fuel += module_fuel

    print('Answer:', total_fuel)
