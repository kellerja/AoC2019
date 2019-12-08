import csv
from enum import Enum
from itertools import permutations


class Memory:

    def __init__(self, memory):
        self.memory = memory

    def __getitem__(self, item):
        return self.memory[item]

    def __repr__(self):
        return self.memory.__repr__()

    def dereference(self, reference):
        return self.get_value(self.get_value(reference))

    def get_value(self, address):
        return self.memory[address]

    def set_value(self, address, value):
        self.memory[address] = value

    def set_value_by_reference(self, reference, value):
        self.set_value(self.get_value(reference), value)


class IO:

    def __init__(self, pipes=None, wait_input=input):
        self.stream = []
        self.inputs = []
        self.pipes = pipes
        self.wait_input = wait_input

    def print(self, value):
        self.stream.append(value)
        if self.pipes is not None:
            for pipe in self.pipes:
                pipe.inputs.append(value)

    def read(self):
        if len(self.inputs) > 0:
            return self.inputs.pop(0)
        return self.wait_input()

    def prepare_inputs(self, inputs):
        self.inputs.extend(inputs)

    def print_entire_output(self):
        print("!!!! OUTPUT !!!!")
        for item in self.stream:
            print(item)
        print("!!!!!!!!!!!!!!!!")


class Process:

    def __init__(self, memory, io=IO()):
        self.ic = 0
        self.memory = memory
        self.io = io

        self.alive = True
        self.ready = True


class ProcessStatus(Enum):
    CONTINUE = 1,
    HALT = 2,
    WAIT = 3

class CPU:
    def get_op(self, process):
        command = str(process.memory.get_value(process.ic))
        return int(command[-2:])

    def get_parameter_handlers(self, process, param_num):
        flags = self.get_parameter_flag(process)
        if len(flags) >= param_num:
            flag = int(flags[param_num - 1])
            if flag == 1:
                return process.memory.get_value, process.memory.set_value
        return process.memory.dereference, process.memory.set_value_by_reference

    def get_parameter_flag(self, process):
        command = str(process.memory.get_value(process.ic))
        return command[-3::-1]

    def process_addition(self, process):
        read_1, _ = self.get_parameter_handlers(process, 1)
        read_2, _ = self.get_parameter_handlers(process, 2)
        _, write_3 = self.get_parameter_handlers(process, 3)
        a = read_1(process.ic + 1)
        b = read_2(process.ic + 2)
        write_3(process.ic + 3, a + b)
        process.ic += 3
        return ProcessStatus.CONTINUE

    def process_multiply(self, process):
        read_1, _ = self.get_parameter_handlers(process, 1)
        read_2, _ = self.get_parameter_handlers(process, 2)
        _, write_3 = self.get_parameter_handlers(process, 3)
        a = read_1(process.ic + 1)
        b = read_2(process.ic + 2)
        write_3(process.ic + 3, a * b)
        process.ic += 3
        return ProcessStatus.CONTINUE

    def read_input(self, process):
        value = process.io.read()
        if value is None:
            return ProcessStatus.WAIT
        value = int(value)
        _, write_1 = self.get_parameter_handlers(process, 1)
        write_1(process.ic + 1, value)
        process.ic += 1
        return ProcessStatus.CONTINUE

    def print_output(self, process):
        read_1, _ = self.get_parameter_handlers(process, 1)
        process.io.print(read_1(process.ic + 1))
        process.ic += 1
        return ProcessStatus.CONTINUE

    def jump_if_non_zero(self, process):
        read_1, _ = self.get_parameter_handlers(process, 1)
        read_2, _ = self.get_parameter_handlers(process, 2)
        if read_1(process.ic + 1) != 0:
            process.ic = read_2(process.ic + 2) - 1
        else:
            process.ic += 2
        return ProcessStatus.CONTINUE

    def jump_if_zero(self, process):
        read_1, _ = self.get_parameter_handlers(process, 1)
        read_2, _ = self.get_parameter_handlers(process, 2)
        if read_1(process.ic + 1) == 0:
            process.ic = read_2(process.ic + 2) - 1
        else:
            process.ic += 2
        return ProcessStatus.CONTINUE

    def less_than(self, process):
        read_1, _ = self.get_parameter_handlers(process, 1)
        read_2, _ = self.get_parameter_handlers(process, 2)
        _, write_3 = self.get_parameter_handlers(process, 3)
        value = 1 if read_1(process.ic + 1) < read_2(process.ic + 2) else 0
        write_3(process.ic + 3, value)
        process.ic += 3
        return ProcessStatus.CONTINUE

    def equals(self, process):
        read_1, _ = self.get_parameter_handlers(process, 1)
        read_2, _ = self.get_parameter_handlers(process, 2)
        _, write_3 = self.get_parameter_handlers(process, 3)
        value = 1 if read_1(process.ic + 1) == read_2(process.ic + 2) else 0
        write_3(process.ic + 3, value)
        process.ic += 3
        return ProcessStatus.CONTINUE

    def process_halt(self, _):
        return ProcessStatus.HALT

    def __init__(self):
        self.OP_CODES = {
            1: self.process_addition,
            2: self.process_multiply,
            3: self.read_input,
            4: self.print_output,
            5: self.jump_if_non_zero,
            6: self.jump_if_zero,
            7: self.less_than,
            8: self.equals,
            99: self.process_halt
        }

        self.processes = []

    def step(self, process, debug=False):
        op = self.get_op(process)
        if debug:
            print(f'Starting new step. IC {process.ic} running op {op} ({self.OP_CODES.get(op, lambda x: None).__name__}) with flags {self.get_parameter_flag(process)} ({process.memory[process.ic]})')
            print(f'Memory {process.memory}')
        return self.OP_CODES[op](process)

    def process(self, process, debug=False):
        if not process.alive:
            return ProcessStatus.HALT, process
        if debug:
            step_count = 0
            print('Starting program\n')
        while True:
            status = self.step(process, debug)
            if status == ProcessStatus.HALT:
                process.alive = False
                break
            if status == ProcessStatus.WAIT:
                break
            process.ic += 1
            if debug:
                step_count += 1
                print(f'Ending step {step_count} with status {status}')
                print(f'Memory {process.memory}\n')
        if debug:
            print(f'Ending program. Total steps {step_count}')
            print(f'Memory {process.memory}')
        return status, process

    def run(self):
        finished_processes = set()
        while len(finished_processes) != len(self.processes):
            for process in self.processes:
                status, _ = self.process(process)
                if status == ProcessStatus.HALT:
                    finished_processes.add(process)


def read_memory():
    mem = []
    with open('input.txt', 'r') as file:
        reader = csv.reader(file)
        for line in reader:
            for element in line:
                mem.append(int(element))
    return mem


def write_result(result):
    with open('output.txt', 'w') as file:
        file.write(str(result))
        file.write("\n")


def wait_for_input():
    pass


if __name__ == '__main__':
    orig_memory = read_memory()
    print(f'Original program: {orig_memory}')

    highest_signal = 0
    for phase_sequence in permutations(range(5, 10)):
        cpu = CPU()
        processes = [Process(Memory(orig_memory.copy()), IO()) for _ in range(len(phase_sequence))]
        for index, process in enumerate(processes):
            process.io.pipes = [processes[(index + 1) % len(processes)].io]
            process.io.wait_input = lambda: None
            process.io.prepare_inputs([phase_sequence[index]])
        processes[0].io.prepare_inputs([0])

        cpu.processes = processes
        cpu.run()
        highest_signal = max(highest_signal, processes[-1].io.stream[-1])
        print(f'\nRun complete for sequence {phase_sequence}. Score {processes[-1].io.stream[-1]}')
        # for index, process in enumerate(processes):
        #     print(f'Amp {index} finished with input stream length {len(process.io.inputs)} output stream length {len(process.io.stream)}')
        #     process.io.print_entire_output()
    print(f'Best score {highest_signal}')
    write_result(highest_signal)
