"""Day 10: Monitoring Station"""
import math
import textwrap


def parse_map(asteriod_map):
    map_lines = asteriod_map.split('\n')
    width = len(map_lines[0])
    height = len(map_lines)

    asteroids = []

    for y in range(0, height):
        for x in range(0, width):
            char = map_lines[y][x]
            if char == '#':
                asteroids.append((x, y))

    return asteroids


def can_see(asteroid_a, asteroid_b, asteroids):
    def is_between(a, b, c):
        a_x = a[0]
        a_y = a[1]
        b_x = b[0]
        b_y = b[1]
        c_x = c[0]
        c_y = c[1]

        cross_product = (c_y - a_y) * (b_x - a_x) - (c_x - a_x) * (b_y - a_y)
        is_colinear = math.isclose(cross_product, 0)

        dot_product = (c_x - a_x) * (b_x - a_x) + (c_y - a_y)*(b_y - a_y)
        length_squared = (b_x - a_x)*(b_x - a_x) + (b_y - a_y)*(b_y - a_y)
        in_between = dot_product >= 0 and dot_product <= length_squared

        return is_colinear and in_between

    is_blocked = False
    for asteroid in asteroids:
        if not asteroid == asteroid_a and not asteroid == asteroid_b:
            if is_between(asteroid_a, asteroid_b, asteroid):
                is_blocked = True
                break

    return not is_blocked


def find_highest_visibility(asteriod_map):
    asteroids = parse_map(asteriod_map)
    visibility_counts = {}

    for asteroid_a in asteroids:
        for asteroid_b in asteroids:
            if not asteroid_a == asteroid_b:
                if can_see(asteroid_a, asteroid_b, asteroids):
                    visibility_counts[asteroid_a] = visibility_counts.get(asteroid_a, 0) + 1

    return max(visibility_counts.items(), key=lambda i: i[1])


if __name__ == '__main__':
    with open('./input') as f:
        asteriod_map = f.read()[:-1]

    result = find_highest_visibility(asteriod_map)

    print('Answer:', result)
