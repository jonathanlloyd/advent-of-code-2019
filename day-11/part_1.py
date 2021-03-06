"""Day 11: Space Police"""

DEBUG_ENABLED = False


class Computer:
    def __init__(self, memory_contents, input_callback=None,
                 output_callback=None):
        self._memory = memory_contents.copy()
        self._input_callback = input_callback
        self._output_callback = output_callback
        self._pc = 0
        self._relative_base = 0
        self.halted = False

    def read(self, location):
        if location > len(self._memory):
            return 0
        return self._memory[location]

    def write(self, location, value):
        if location >= len(self._memory):
            deficit = location - len(self._memory)
            for _ in range(0, deficit + 100):
                self._memory.append(0)
        self._memory[location] = value

    def run(self):
        while True:
            if DEBUG_ENABLED:
                import pdb; pdb.set_trace() 
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
                return
            elif opcode == 5:
                self._do_jump_if_true(modecode)
            elif opcode == 6:
                self._do_jump_if_false(modecode)
            elif opcode == 7:
                self._do_less_than(modecode)
            elif opcode == 8:
                self._do_equals(modecode)
            elif opcode == 9:
                self._do_move_base(modecode)
            elif opcode == 99:
                self.halted = True
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
        elif mode == 2:
            return self.read(part + self._relative_base)
        else:
            raise RuntimeError('Unknown value mode')

    def _addr_by_mode(self, addr, mode):
        if mode == 2:
            return addr + self._relative_base
        else:
            return addr

    def _do_additon(self, modecode):
        [input_a_mode, input_b_mode, output_mode] = self._extract_modes(modecode, 3)
        [_, input_a_part, input_b_part, output_part] = self._memory[self._pc:self._pc+4]

        input_a = self._value_by_mode(input_a_part, input_a_mode)
        input_b = self._value_by_mode(input_b_part, input_b_mode)
        output_addr = self._addr_by_mode(output_part, output_mode)

        self.write(output_addr, input_a + input_b)
        self._pc += 4

    def _do_multiplication(self, modecode):
        [input_a_mode, input_b_mode, output_mode] = self._extract_modes(modecode, 3)
        [_, input_a_part, input_b_part, output_part] = self._memory[self._pc:self._pc+4]

        input_a = self._value_by_mode(input_a_part, input_a_mode)
        input_b = self._value_by_mode(input_b_part, input_b_mode)
        output_addr = self._addr_by_mode(output_part, output_mode)

        self.write(output_addr, input_a * input_b)
        self._pc += 4

    def _do_input(self, modecode):
        if not self._input_callback:
            raise IOError('Input port not connected')
        [output_mode] = self._extract_modes(modecode, 1)
        [_, output_part] = self._memory[self._pc:self._pc+2]

        output_addr = self._addr_by_mode(output_part, output_mode)

        input_value = self._input_callback()
        self.write(output_addr, input_value)

        self._pc += 2

    def _do_output(self, modecode):
        if not self._output_callback:
            raise IOError('Output port not connected')

        [output_mode] = self._extract_modes(modecode, 1)
        [_, output_part] = self._memory[self._pc:self._pc+2]

        output_value = self._value_by_mode(output_part, output_mode)
        self._output_callback(output_value)

        self._pc += 2

    def _do_jump_if_true(self, modecode):
        [flag_mode, target_addr_mode] = self._extract_modes(modecode, 2)
        [_, flag_part, target_addr_part] = self._memory[self._pc:self._pc+3]

        flag = self._value_by_mode(flag_part, flag_mode)
        target_addr = self._value_by_mode(target_addr_part, target_addr_mode)

        if flag:
            self._pc = target_addr
        else:
            self._pc += 3

    def _do_jump_if_false(self, modecode):
        [flag_mode, target_addr_mode] = self._extract_modes(modecode, 2)
        [_, flag_part, target_addr_part] = self._memory[self._pc:self._pc+3]

        flag = self._value_by_mode(flag_part, flag_mode)
        target_addr = self._value_by_mode(target_addr_part, target_addr_mode)

        if not flag:
            self._pc = target_addr
        else:
            self._pc += 3


    def _do_less_than(self, modecode):
        [input_a_mode, input_b_mode, output_mode] = self._extract_modes(modecode, 3)
        [_, input_a_part, input_b_part, output_part] = self._memory[self._pc:self._pc+4]

        input_a = self._value_by_mode(input_a_part, input_a_mode)
        input_b = self._value_by_mode(input_b_part, input_b_mode)
        output_addr = self._addr_by_mode(output_part, output_mode)

        if input_a < input_b:
            result = 1
        else:
            result = 0

        self.write(output_addr, result)
        self._pc += 4

    def _do_equals(self, modecode):
        [input_a_mode, input_b_mode, output_mode] = self._extract_modes(modecode, 3)
        [_, input_a_part, input_b_part, output_part] = self._memory[self._pc:self._pc+4]

        input_a = self._value_by_mode(input_a_part, input_a_mode)
        input_b = self._value_by_mode(input_b_part, input_b_mode)
        output_addr = self._addr_by_mode(output_part, output_mode)

        if input_a == input_b:
            result = 1
        else:
            result = 0

        self.write(output_addr, result)
        self._pc += 4

    def _do_move_base(self, modecode):
        [delta_mode] = self._extract_modes(modecode, 1)
        [_, delta_part] = self._memory[self._pc:self._pc+2]

        delta = self._value_by_mode(delta_part, delta_mode)
        self._relative_base += delta

        self._pc += 2


class Robot:
    def __init__(self, programme):
        def get_input():
            return self._painted_panels.get((self.x, self.y), 0)

        def do_output(value):
            self._last_output = value

        self._core = Computer(
            programme,
            input_callback=get_input,
            output_callback=do_output,
        )
        self._painted_panels = {}
        self._last_output = None

        self.running = True
        self.x = 0
        self.y = 0
        self.direction = 'UP'

    def _turn_left(self):
        if self.direction == 'UP':
            self.direction = 'LEFT'
        elif self.direction == 'LEFT':
            self.direction = 'DOWN'
        elif self.direction == 'DOWN':
            self.direction = 'RIGHT'
        elif self.direction == 'RIGHT':
            self.direction = 'UP'
        else:
            raise RuntimeError(f"Unknown direction {self.direction}")

    def _turn_right(self):
        if self.direction == 'UP':
            self.direction = 'RIGHT'
        elif self.direction == 'RIGHT':
            self.direction = 'DOWN'
        elif self.direction == 'DOWN':
            self.direction = 'LEFT'
        elif self.direction == 'LEFT':
            self.direction = 'UP'
        else:
            raise RuntimeError(f"Unknown direction {self.direction}")

    def step(self):
        if not self.running:
            return

        self._core.run()
        color = self._last_output

        self._core.run()
        direction = self._last_output

        self._painted_panels[(self.x, self.y)] = color

        if direction == 0:
            self._turn_left()
        elif direction == 1:
            self._turn_right()
        else:
            raise RuntimeError(f"Unknown direction {direction}")

        if self.direction == 'UP':
            self.y += 1
        elif self.direction == 'RIGHT':
            self.x += 1
        elif self.direction == 'DOWN':
            self.y -= 1
        elif self.direction == 'LEFT':
            self.x -= 1
        else:
            raise RuntimeError(f"Unknown direction {self.direction}")

        self.running = not self._core.halted

def calc_num_painted_panels(programme):
    visited_panels = set()
    robot = Robot(programme)
    while robot.running:
        robot.step()
        visited_panels.add((robot.x, robot.y))

    return len(visited_panels)


if __name__ == '__main__':
    with open('./input', 'r') as f:
        raw = f.read()
    programme = [int(code) for code in raw.split(',')]
    result = calc_num_painted_panels(programme)
    print('Num panels:', result)
