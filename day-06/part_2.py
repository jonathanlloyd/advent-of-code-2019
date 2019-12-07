class Node:
    def __init__(self, value):
        self.value = value
        self._children = {}
        self.parent = None

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"<Node value={self.value}, children=[{','.join([child.value for child in self.children])}]>"

    def add_child(self, child_node):
        self._children[child_node.value] = child_node

    @property
    def children(self):
        return list(self._children.values())


def distance(src, dst, orbit_pairs):
    root, nodes = make_orbit_tree(orbit_pairs)

    src_node = nodes[src]
    dst_node = nodes[dst]

    counts = tree_to_orbit_count(root)
    common_ancestor = find_common_ancestor(src_node, dst_node)

    return (counts[src_node.value] - counts[common_ancestor.value]) + (counts[dst_node.value] - counts[common_ancestor.value]) - 2


def find_common_ancestor(node_a, node_b):
    node_a_ancestors = set()
    current = node_a
    while current.parent:
        node_a_ancestors.add(current.parent)
        current = current.parent

    current = node_b
    while current.parent:
        if current in node_a_ancestors:
            return current
        current = current.parent

    return None


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
        child_node.parent = parent_node

    return nodes.get('COM'), nodes


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

    print('Distance:',distance('YOU', 'SAN', orbit_pairs))
