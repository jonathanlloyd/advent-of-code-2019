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


def get_angle(origin, point):
    point_x = point[0] - origin[0]
    point_y = -(point[1] - origin[1])

    if point_x >= 0 and point_y >= 0:
        if point_y == 0:
            angle = math.pi * 0.5
        else:
            angle = math.atan(point_x / point_y)
    elif point_x >= 0 and point_y < 0:
        if point_x == 0:
            angle = math.pi
        else:
            angle = math.atan(-point_y / point_x) + math.pi * 0.5
    elif point_x < 0 and point_y < 0:
        angle = math.atan(-point_x / -point_y) + math.pi * 1
    elif point_x < 0 and point_y >= 0:
        angle = math.atan(point_y / -point_x) + math.pi * 1.5

    return (angle / (2 * math.pi)) * 360


def distance(a, b):
    a_x = a[0]
    a_y = a[1]
    b_x = b[0]
    b_y = b[1]

    return math.sqrt(math.pow(a_x - b_x, 2) + math.pow(a_y - b_y, 2)) + 1.75


def num_visable_asteroids(current_asteroid, asteroids):
    angle_to_asteroids = {}
    for asteroid in asteroids:
        if asteroid == current_asteroid:
            continue
        angle = get_angle(current_asteroid, asteroid)
        slot = angle_to_asteroids.get(angle, [])
        slot.append(asteroid)
        slot.sort(key=lambda a: distance(a, current_asteroid))
        angle_to_asteroids[angle] = slot

    return len(angle_to_asteroids)


def find_highest_visibility(asteriod_map):
    asteroids = parse_map(asteriod_map)

    visibility_counts = {
        a: num_visable_asteroids(a, asteroids)
        for a in asteroids
    }

    return max(visibility_counts.items(), key=lambda i: i[1])


if __name__ == '__main__':
    with open('./input') as f:
        asteriod_map = f.read()[:-1]

    result = find_highest_visibility(asteriod_map)

    print('Answer:', result)
