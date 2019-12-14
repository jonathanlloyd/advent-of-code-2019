def checksum(pixels, width, height):
    layers = pixels_to_layers(pixels, width, height)
    layer_index_to_0_count = {}
    for index, layer in enumerate(layers):
        layer_index_to_0_count[index] = num_digits_in_layer(0, layer)

    layer_fewest_0s_index = min(layer_index_to_0_count.keys(), key=lambda x: layer_index_to_0_count[x])
    layer_fewest_0s = layers[layer_fewest_0s_index]

    num_1s = num_digits_in_layer(1, layer_fewest_0s)
    num_2s = num_digits_in_layer(2, layer_fewest_0s)

    return num_1s * num_2s


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


def num_digits_in_layer(digit, layer):
    try:
        count = 0
        for y in range(0, len(layer)):
            for x in range(0, len(layer[0])):
                if layer[y][x] == digit:
                    count += 1
        return count
    except:
        import pdb; pdb.set_trace() 


if __name__ == '__main__':
    with open('./input', 'r') as f:
        raw = f.read()
    pixels = [int(d) for d in raw[:-1]]
    print('Checksun:', checksum(pixels, 25, 6))
