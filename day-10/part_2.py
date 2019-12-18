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


def get_blast_order(asteriod_map, laser_location):
    asteroids = parse_map(asteriod_map)
    angle_to_asteroids = {}
    for asteroid in asteroids:
        if asteroid == laser_location:
            continue
        angle = get_angle(laser_location, asteroid)
        slot = angle_to_asteroids.get(angle, [])
        slot.append(asteroid)
        slot.sort(key=lambda a: distance(a, laser_location))
        angle_to_asteroids[angle] = slot

    sorted_slots = sorted(angle_to_asteroids.items(), key=lambda i: i[0])
    blast_order = []
    while len(sorted_slots):
        next_slots = []
        for (angle, slot) in sorted_slots:
            if len(slot):
                next_asteroid = slot[0]
                blast_order.append(next_asteroid)
                next_slot = slot[1:]
                if len(next_slot):
                    next_slots.append((angle, next_slot))

        sorted_slots = next_slots

    return blast_order


if __name__ == '__main__':
    with open('./input') as f:
        asteriod_map = f.read()[:-1]

    result = get_blast_order(asteriod_map, (20,20))

    if len(result) < 200:
        print("Error: Not enough asteroids vaporised")

    result_x = result[199][0]
    result_y = result[199][1]

    print('Answer:', result_x * 100 + result_y)
