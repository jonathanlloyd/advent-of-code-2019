"""Day 12: The N-Body Problem"""

from dataclasses import dataclass


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


def calc_vel(moon, other_moons, vel_key, pos_key):
    moon_pos = pos_key(moon)
    deltas = []
    for other_moon in other_moons:
        other_moon_pos = pos_key(other_moon)
        if other_moon_pos > moon_pos:
            delta = 1
        elif other_moon_pos < moon_pos:
            delta = -1
        else:
            delta = 0
        deltas.append(delta)

    return vel_key(moon) + sum(deltas)


def calc_energy(moon):
    potential_energy = abs(moon.pos.x) + abs(moon.pos.y) + abs(moon.pos.z)
    kinetic_energy = abs(moon.vel.x) + abs(moon.vel.y) + abs(moon.vel.z)
    return potential_energy * kinetic_energy


def run_step(moons):
    updated_vel = [
        Moon(
            id=moon.id,
            pos=moon.pos,
            vel=Vec3(
                x=calc_vel(moon, moons, vel_key=lambda m: m.vel.x, pos_key=lambda m: m.pos.x),
                y=calc_vel(moon, moons, vel_key=lambda m: m.vel.y, pos_key=lambda m: m.pos.y),
                z=calc_vel(moon, moons, vel_key=lambda m: m.vel.z, pos_key=lambda m: m.pos.z),
            ),
        )
        for moon in moons
    ]
    updated_pos = [
        Moon(
            id=moon.id,
            pos=Vec3(
                x=moon.pos.x + moon.vel.x,
                y=moon.pos.y + moon.vel.y,
                z=moon.pos.z + moon.vel.z,
            ),
            vel=moon.vel,
        )
        for moon in updated_vel
    ]
    return updated_pos


def get_total_energy(moons, steps):
    for i in range(0, steps):
        moons = run_step(moons)

    return sum([calc_energy(moon) for moon in moons])


if __name__ == '__main__':
    with open('./input') as f:
        raw = f.read()

    moons = [parse_moon(line, i) for i, line in enumerate(raw.strip().split('\n'))]
    result = get_total_energy(moons, 1000)
    print('Answer:', result)
