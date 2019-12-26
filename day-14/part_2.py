"""Day 14: Space Stoichiometry"""

from dataclasses import dataclass
import math

@dataclass
class Quantity:
    kind: str
    amount: int

@dataclass
class Conversion:
    src: list
    dst: Quantity


def parse_conversions(raw_string):
    def parse_qty(raw_qty):
        amount_part, kind_part = raw_qty.split(' ')
        return Quantity(
            kind=kind_part,
            amount=int(amount_part),
        )

    def parse_conversion(raw_line):
        src_part, dst_part = raw_line.split(' => ')
        src_qtys = [parse_qty(v) for v in src_part.strip().split(', ')]
        dst_qty = parse_qty(dst_part)
        return Conversion(
            src=src_qtys,
            dst=dst_qty,
        )

    return [parse_conversion(line) for line in raw_string.strip().split('\n')]


def apply_conversion(conversion, resources, waste):
    next_resources = resources.copy()
    next_waste = waste.copy()

    target_resource = conversion.dst.kind
    target_resource_amount = resources.get(target_resource, 0)
    conversion_yield = conversion.dst.amount

    num_conversions = math.ceil(target_resource_amount / conversion_yield)

    for mat in conversion.src:
        amount_mat_produced = mat.amount * num_conversions

        # Consume waste
        amount_from_waste = min([waste.get(mat.kind, 0), amount_mat_produced])
        next_waste[mat.kind] = next_waste.get(mat.kind, 0) - amount_from_waste
        if next_waste[mat.kind] == 0:
            del next_waste[mat.kind]
        amount_mat_produced -= amount_from_waste

        next_resources[mat.kind] = next_resources.get(mat.kind, 0) + amount_mat_produced
    del next_resources[target_resource]

    amount_wasted = conversion_yield * num_conversions - target_resource_amount
    next_waste[target_resource] = next_waste.get(target_resource, 0) + amount_wasted

    return next_waste, next_resources


def calc_ore_requried(conversions, requirements):
    waste = {}
    while list(requirements.keys()) != ['ORE']:
        matching_conversions = [
            c
            for c in conversions
            if c.dst.kind in set(requirements.keys())
        ]
        c = matching_conversions[0]
        waste, requirements = apply_conversion(c, requirements, waste)

    return requirements['ORE']

def calc_fuel_produced(conversions, ore_amount):
    lower_bound = 0
    higher_bound = ore_amount

    while True:
        fuel_amount = (lower_bound + higher_bound) // 2
        ore_required = calc_ore_requried(conversions, {'FUEL': fuel_amount})
        next_ore_required = calc_ore_requried(conversions, {'FUEL': fuel_amount + 1})
        if ore_required <= ore_amount and next_ore_required > ore_amount:
            return fuel_amount
        elif ore_required <= ore_amount and next_ore_required <= ore_amount:
            lower_bound = fuel_amount
        else:
            higher_bound = fuel_amount


if __name__ == '__main__':
    with open('./input', 'r') as f:
        raw = f.read()

    conversions = parse_conversions(raw)
    result = calc_fuel_produced(conversions, 1000000000000)

    print('Ore Required:', result)
