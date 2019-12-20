"""Day 12: The N-Body Problem"""

from dataclasses import dataclass
from math import gcd
from functools import reduce



@dataclass
class Vec3:
    x: float
    y: float
    z: float


@dataclass
class Moon:
    id: int
    pos: Vec3
    vel: Vec3

    def __hash__(self):
        return hash(self.id)


def parse_moon(moon_str, id):
    x = y = z = 0

    state = 'X'
    for i in range(0, len(moon_str)):
        if state == 'X':
            if moon_str[i] == '=':
                i += 1
                x_chars = ''
                while i < len(moon_str) and not moon_str[i] == ',':
                    x_chars += moon_str[i]
                    i += 1
                x = int(x_chars)
                state = 'Y'
                continue
        elif state == 'Y':
            if moon_str[i] == '=':
                i += 1
                y_chars = ''
                while i < len(moon_str) and not moon_str[i] == ',':
                    y_chars += moon_str[i]
                    i += 1
                y = int(y_chars)
                state = 'Z'
                continue
        elif state == 'Z':
            if moon_str[i] == '=':
                i += 1
                z_chars = ''
                while i < len(moon_str) and not moon_str[i] == '>':
                    z_chars += moon_str[i]
                    i += 1
                z = int(z_chars)
                break
        else:
            raise RuntimeError(f"Unknown state {state}")

    moon = Moon(
        id=id,
        pos=Vec3(x, y, z),
        vel=Vec3(0, 0, 0),
    )

    return moon


def fixed_point_pos_1d(vel_list, pos_list):
    seen = set()
    count = 0

    def calc_vel(pos_a, pos_b):
        if pos_b > pos_a:
            return 1
        elif pos_b < pos_a:
            return -1
        else:
            return 0

    current_pos = [pos for pos in pos_list]
    current_vels = [vel for vel in vel_list]
    while str([current_pos, current_vels]) not in seen:
        count += 1
        seen.add(str([current_pos, current_vels]))
        next_vels = [
            current_vels[pos_index] + sum([
                calc_vel(pos, other_pos)
                for other_pod_index, other_pos in enumerate(current_pos)
                if pos_index != other_pod_index
            ])
            for pos_index, pos in enumerate(current_pos)
        ]
        next_pos = [
            pos + next_vels[i]
            for i, pos in enumerate(current_pos)
        ]

        current_pos = next_pos
        current_vels = next_vels

    return count


def least_common_multiple(values):
    return reduce(lambda a,b: a*b // gcd(a,b), values)


def fixed_point_pos(moons):
    return least_common_multiple([
        fixed_point_pos_1d([moon.vel.x for moon in moons], [moon.pos.x for moon in moons]),
        fixed_point_pos_1d([moon.vel.y for moon in moons], [moon.pos.y for moon in moons]),
        fixed_point_pos_1d([moon.vel.z for moon in moons], [moon.pos.z for moon in moons]),
    ])


if __name__ == '__main__':
    with open('./input') as f:
        raw = f.read()

    moons = [parse_moon(line, i) for i, line in enumerate(raw.strip().split('\n'))]
    result = fixed_point_pos(moons)
    print('Answer:', result)
