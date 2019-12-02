if __name__ == '__main__':
    # Calculate fuel from modules
    fuel_requirements = []
    with open('./input', 'r') as f:
        for i, line in enumerate(f):
            module_mass = int(line)
            module_fuel = (module_mass // 3) - 2
            fuel_requirements.append(module_fuel)

    # Calculate fuel for fuel
    extra_fuel_requirements = []
    for fuel_batch in fuel_requirements:
        total_fuel_for_batch = 0
        next_fuel_batch = fuel_batch
        while True:
            fuel_batch_fuel = (next_fuel_batch // 3) - 2
            if fuel_batch_fuel <= 0:
                break
            next_fuel_batch = fuel_batch_fuel
            total_fuel_for_batch += next_fuel_batch
        extra_fuel_requirements.append(total_fuel_for_batch)

    fuel_requirements += extra_fuel_requirements
    total_fuel = sum(fuel_requirements)

    print('Answer:', total_fuel)
