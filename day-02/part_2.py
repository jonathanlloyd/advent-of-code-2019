class Computer:
    def __init__(self, memory_contents):
        self._memory = memory_contents
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
            opcode = self.read(self._pc)
            if opcode == 1:
                self._do_addition()
            elif opcode == 2:
                self._do_multiplication()
            elif opcode == 99:
                return
            else:
                raise RuntimeError('Bad state')

    def _do_addition(self):
        [_, input_a_addr, input_b_addr, output_addr] = self._memory[self._pc:self._pc+4]
        input_a = self.read(input_a_addr)
        input_b = self.read(input_b_addr)
        self.write(output_addr, input_a + input_b)
        self._pc += 4

    def _do_multiplication(self):
        [_, input_a_addr, input_b_addr, output_addr] = self._memory[self._pc:self._pc+4]
        input_a = self.read(input_a_addr)
        input_b = self.read(input_b_addr)
        self.write(output_addr, input_a * input_b)
        self._pc += 4



if __name__ == '__main__':
    with open('./input', 'r') as f:
        raw = f.read()
    memory_contents = [int(code) for code in raw.split(',')]
    def brute_force():
        for noun in range(0, 100):
            for verb in range(0, 100):
                computer = Computer(memory_contents.copy())
                computer.write(1, noun)
                computer.write(2, verb)
                try:
                    computer.run()
                except:
                    continue
                result = computer.read(0)
                if result == 19690720:
                    return noun, verb,
    noun, verb = brute_force()
    answer = 100 * noun + verb
    print('Answer:', answer)

