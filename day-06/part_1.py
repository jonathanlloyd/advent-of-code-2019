class Node:
    def __init__(self, value):
        self.value = value
        self._children = {}

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"<Node value={self.value}, children=[{','.join([child.value for child in self.children])}]>"

    def add_child(self, child_node):
        self._children[child_node.value] = child_node

    @property
    def children(self):
        return list(self._children.values())


def count_orbits(orbit_pairs):
    root = make_orbit_tree(orbit_pairs)
    return sum(tree_to_orbit_count(root).values())


def make_orbit_tree(orbit_pairs):
    nodes = {}
    for parent, child in orbit_pairs:
        if parent in nodes:
            parent_node = nodes[parent]
        else:
            parent_node = Node(parent)
            nodes[parent] = parent_node

        if child in nodes:
            child_node = nodes[child]
        else:
            child_node = Node(child)
            nodes[child] = child_node

        parent_node.add_child(child_node)

    return nodes.get('COM')


def tree_to_orbit_count(root, current_depth=0):
    orbit_counts = {root.value: current_depth}
    for child in root.children:
        orbit_counts.update(tree_to_orbit_count(child, current_depth+1))
    return orbit_counts



if __name__ == '__main__':
    with open('./input', 'r') as f:
        raw = f.read()

    raw_lines = raw.split('\n')[:-1]
    orbit_pairs = []
    for line in raw_lines:
        [parent, child] = line.split(')')
        orbit_pairs.append((parent, child))

    print('Total orbits:', count_orbits(orbit_pairs))
