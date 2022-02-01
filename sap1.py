from collections import deque
from assembler import assemble


class ProgramCounter:
    def __init__(self) -> None:
        self.count = 0

    def inc(self):
        self.count += 1
        if self.count == 4 ** 2:
            self.count = 0

    def read(self):
        return int_to_bin(self.count, 4)

    def clr(self):
        self.count = 0


class Register:
    def __init__(self, size) -> None:
        self.size = size
        self.data = int_to_bin(0, 8)

    def set(self, data):
        self.data = data

    def clr(self):
        self.data = int_to_bin(0, 8)


class Memory:
    def __init__(self) -> None:
        self.state = [int_to_bin(0, 8) for a in range(16)]

    def set(self, register, data):
        self.state[int(register, 2)] = data

    def program(self, data):
        self.state = data

    def read(self, register: list[int]):
        return self.state[int(register, 2)]

    def clr(self):
        self.state = [int_to_bin(0, 8) for a in range(16)]


class Control_Unit:
    def __init__(self) -> None:
        self.state = int_to_bin(1, 6)

    def inc(self):
        _tmp = deque(self.state)        # convert to deque object
        _tmp.rotate(-1)                 # rotate the list
        self.state = "".join(_tmp)      # join back to a string

    def clr(self):
        self.state = int_to_bin(1, 6)


class Bus():
    def __init__(self) -> None:
        self.data = int_to_bin(0, 8)

    def set(self, data):
        self.data = data

    def clr(self):
        self.data = int_to_bin(0, 8)


class Instruction_Register(Register):
    def get_opcode(self):
        return self.data[:4]

    def get_operand(self):
        return self.data[4:]


def int_to_bin(i, bits):
    if bits == 8:
        return str(format(i, '08b'))
    if bits == 6:
        return str(format(i, '06b'))
    if bits == 4:
        return str(format(i, '04b'))


def binary_addition(a, b):
    _a = int(a, 2)
    _b = int(b, 2)
    _sum = _a + _b
    return int_to_bin(_sum, 8)


def binary_subtraction(a, b):
    _a = int(a, 2)
    _b = int(b, 2)
    _sum = _a - _b
    if _sum < 1:
        _sum = bin(_sum & (2**8 - 1))
        _sum = int(_sum, 2)
    return int_to_bin(_sum, 8)


if __name__ == '__main__':
    mem = Memory()
    cu = Control_Unit()
    mar = Register(4)
    pc = ProgramCounter()
    bus = Bus()
    ir = Instruction_Register(8)
    b_reg = Register(8)
    acc = Register(8)
    out = Register(8)
    run_flag = True

    prog = assemble('prog.txt')
    mem.program(prog)

    while(run_flag):
        for i in range(6):
            if cu.state[5] == '1':
                bus.set(pc.read())
                mar.set(bus.data)
            if cu.state[4] == '1':
                pc.inc()
            if cu.state[3] == '1':
                _add = mem.read(mar.data)
                bus.set(_add)
                ir.set(bus.data)
            if cu.state[2] == '1':
                # check for LDA
                if ir.get_opcode() == '1111':
                    bus.set(ir.get_operand())
                    mar.set(bus.data)
                # check for ADD or SUB
                if ir.get_opcode() == '0001' or ir.get_opcode() == '0010':
                    bus.set(ir.get_operand())
                    mar.set(bus.data)
                # check for OUT
                if ir.get_opcode() == '1110':
                    bus.set(acc.data)
                    out.set(bus.data)
                    print(out.data, int(out.data, 2))
                # check for HLT
                if ir.get_opcode() == '1111':
                    run_flag = False
                    break
            if cu.state[1] == '1':
                # LDA
                if ir.get_opcode() == '0000':
                    _data = mem.read(bus.data)
                    bus.set(_data)
                    acc.set(bus.data)
                # ADD or SUB
                if ir.get_opcode() == '0001' or ir.get_opcode() == '0010':
                    _data = mem.read(bus.data)
                    bus.set(_data)
                    b_reg.set(bus.data)

            if cu.state[0] == '1':
                # ADD
                if ir.get_opcode() == '0001':
                    _sum = binary_addition(acc.data, b_reg.data)
                    bus.set(_sum)
                    acc.set(bus.data)
                # SUB
                if ir.get_opcode() == '0010':
                    _sum = binary_subtraction(acc.data, b_reg.data)
                    bus.set(_sum)
                    acc.set(bus.data)
            cu.inc()
