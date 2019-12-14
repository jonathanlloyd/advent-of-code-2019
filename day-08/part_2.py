def render(pixels, width, height):
    layers = pixels_to_layers(pixels, width, height)
    layers.reverse()

    output = ''
    for y in range(0, height):
        for x in range(0, width):
            char = '!'
            for layer in layers:
                value = layer[y][x]
                if value == 0:
                    char = ' '
                elif value == 1:
                    char = 'X'
                else:
                    continue
            output += char
        output += '\n'

    return output


def pixels_to_layers(pixels, width, height):
    current_index = 0
    layers = []
    while current_index < len(pixels):
        current_layer = []
        for _ in range(0, height):
            current_layer.append(pixels[current_index:current_index+width])
            current_index += width
        layers.append(current_layer)
    return layers


if __name__ == '__main__':
    with open('./input', 'r') as f:
        raw = f.read()
    pixels = [int(d) for d in raw[:-1]]
    print(render(pixels, 25, 6))
