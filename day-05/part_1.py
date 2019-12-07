class Computer:
    def __init__(self, memory_contents, input_callback=None,
                 output_callback=None):
        self._memory = memory_contents
        self._input_callback = input_callback
        self._output_callback = output_callback
        self._pc = 0

    def read(self, location):
        if location > len(self._memory):
            return None
        return self._memory[location]

    def write(self, location, value):
        if location > len(self._memory):
            raise RuntimeError('segfault')
        self._memory[location] = value

    def run(self):
        while True:
            opcode = self._extract_opcode(self.read(self._pc))
            modecode = self._extract_modecode(self.read(self._pc))
            if opcode == 1:
                self._do_additon(modecode)
            elif opcode == 2:
                self._do_multiplication(modecode)
            elif opcode == 3:
                self._do_input(modecode)
            elif opcode == 4:
                self._do_output(modecode)
            elif opcode == 99:
                return
            else:
                raise RuntimeError('Bad state')

    def _extract_opcode(self, raw_instruction):
        return raw_instruction % 100

    def _extract_modecode(self, raw_instruction):
        return raw_instruction // 100

    def _extract_modes(self, modecode, num_modes):
        acc = modecode
        modes = []
        for _ in range(0, num_modes):
            if acc == 0:
                mode = 0
            else:
                mode = acc % 10
                acc = acc // 10
            modes.append(mode)
        return modes

    def _value_by_mode(self, part, mode):
        if mode == 0:
            return self.read(part)
        elif mode == 1:
            return part
        else:
            raise RuntimeError('Unknown value mode')

    def _do_additon(self, modecode):
        [input_a_mode, input_b_mode] = self._extract_modes(modecode, 2)
        [_, input_a_part, input_b_part, output_part] = self._memory[self._pc:self._pc+4]

        input_a = self._value_by_mode(input_a_part, input_a_mode)
        input_b = self._value_by_mode(input_b_part, input_b_mode)
        output_addr = output_part

        self.write(output_addr, input_a + input_b)
        self._pc += 4

    def _do_multiplication(self, modecode):
        [input_a_mode, input_b_mode] = self._extract_modes(modecode, 2)
        [_, input_a_part, input_b_part, output_part] = self._memory[self._pc:self._pc+4]

        input_a = self._value_by_mode(input_a_part, input_a_mode)
        input_b = self._value_by_mode(input_b_part, input_b_mode)
        output_addr = output_part

        self.write(output_addr, input_a * input_b)
        self._pc += 4

    def _do_input(self, _):
        if not self._input_callback:
            raise IOError('Input port not connected')

        input_value = self._input_callback()
        [_, output_addr] = self._memory[self._pc:self._pc+2]

        self.write(output_addr, input_value)
        self._pc += 2

    def _do_output(self, _):
        if not self._output_callback:
            raise IOError('Output port not connected')

        [_, output_addr] = self._memory[self._pc:self._pc+2]
        output_value = self.read(output_addr)
        self._output_callback(output_value)

        self._pc += 2


if __name__ == '__main__':
    with open('./input', 'r') as f:
        raw = f.read()
    memory_contents = [int(code) for code in raw.split(',')]

    def get_input():
        return 1

    output_buffer = []
    def do_output(value):
        output_buffer.append(value)

    computer = Computer(memory_contents, input_callback=get_input,
                        output_callback=do_output)
    computer.run()

    print('Output Stream:', output_buffer)
