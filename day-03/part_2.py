
def wire_length_to_intersection(directions):
    # Find the visited points for each wire
    visited_points = [
        get_visited_points(wire_directions)
        for wire_directions in directions
    ]

    # Find each point that has been visted by multiple wires
    point_to_visit_count = {}
    for wire_visited_points in visited_points:
        for point in wire_visited_points:
            point_to_visit_count[point] = point_to_visit_count.get(point, 0) + 1

    repeatedly_visited_points = {
        point
        for point, count in point_to_visit_count.items()
        if count > 1
    }

    # Calculate the total number of steps in all wires for each intersection
    point_to_total_dist = {
        point: sum([dist_along_wire(wire_directions, point) for wire_directions in directions])
        for point in repeatedly_visited_points
    }

    return min(point_to_total_dist.values())


def dist_along_wire(wire_directions, point):
    x = 0
    y = 0
    total_dist = 0
    for direction in wire_directions:
        ordinal = direction[0]
        dist = int(direction[1:])
        while dist > 0:
            if ordinal == 'U':
                y -= 1
            elif ordinal == 'D':
                y += 1
            elif ordinal == 'L':
                x -= 1
            elif ordinal == 'R':
                x += 1
            total_dist += 1
            dist -= 1
            if (x, y,) == point:
                return total_dist
    return None


def get_visited_points(wire_directions):
    x = 0
    y = 0
    visited_points = set()
    for direction in wire_directions:
        ordinal = direction[0]
        dist = int(direction[1:])
        while dist > 0:
            if ordinal == 'U':
                y -= 1
            elif ordinal == 'D':
                y += 1
            elif ordinal == 'L':
                x -= 1
            elif ordinal == 'R':
                x += 1
            visited_points.add((x, y,))
            dist -= 1
    return visited_points


def distance_from_origin(point):
    return abs(point[0]) + abs(point[1])


if __name__ == '__main__':
    with open('./input', 'r') as f:
        raw = f.read()
        raw_lines = raw.split('\n')[:-1]
        directions = [raw_line.split(',') for raw_line in raw_lines]

    print(wire_length_to_intersection(directions))
