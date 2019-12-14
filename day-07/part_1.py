import itertools


class Computer:
    def __init__(self, memory_contents, input_callback=None,
                 output_callback=None):
        self._memory = memory_contents.copy()
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
            elif opcode == 5:
                self._do_jump_if_true(modecode)
            elif opcode == 6:
                self._do_jump_if_false(modecode)
            elif opcode == 7:
                self._do_less_than(modecode)
            elif opcode == 8:
                self._do_equals(modecode)
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
        [input_a_mode, input_b_mode] = self._extract_modes(modecode, 2)
        [_, input_a_part, input_b_part, output_part] = self._memory[self._pc:self._pc+4]

        input_a = self._value_by_mode(input_a_part, input_a_mode)
        input_b = self._value_by_mode(input_b_part, input_b_mode)
        output_addr = output_part

        if input_a < input_b:
            result = 1
        else:
            result = 0

        self.write(output_addr, result)
        self._pc += 4

    def _do_equals(self, modecode):
        [input_a_mode, input_b_mode] = self._extract_modes(modecode, 2)
        [_, input_a_part, input_b_part, output_part] = self._memory[self._pc:self._pc+4]

        input_a = self._value_by_mode(input_a_part, input_a_mode)
        input_b = self._value_by_mode(input_b_part, input_b_mode)
        output_addr = output_part

        if input_a == input_b:
            result = 1
        else:
            result = 0

        self.write(output_addr, result)
        self._pc += 4


def run_with_settings(programme, phase_settings):
    prev_amplifier_output = 0
    for setting in phase_settings:
        read_count = 0

        def get_input():
            nonlocal read_count
            if read_count == 0:
                result = setting
            else:
                result = prev_amplifier_output
            read_count += 1
            return result

        def do_output(value):
            nonlocal prev_amplifier_output
            prev_amplifier_output = value

        computer = Computer(programme, input_callback=get_input,
                            output_callback=do_output)
        computer.run()

    return prev_amplifier_output


def brute_force_phase_setting(programme, num_amplifiers):
    max_signal = None
    max_signal_settings = None

    for phase_settings in itertools.permutations([i for i in range(0, num_amplifiers)]):
        signal = run_with_settings(programme, phase_settings)

        if max_signal is None or max_signal < signal:
            max_signal = signal
            max_signal_settings = phase_settings

    return max_signal, max_signal_settings



if __name__ == '__main__':
    with open('./input', 'r') as f:
        raw = f.read()
    programme = [int(code) for code in raw.split(',')]

    max_signal, settings = brute_force_phase_setting(programme, 5)
    print('Max Signal:', max_signal)
    print('Settings:', settings)
