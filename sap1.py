from collections import deque


class ProgramCounter:
    def __init__(self) -> None:
        self.count = 0

    def inc(self):
        self.count += 1
        if self.count == 4 ** 2:
            self.count = 0

    def read(self):
        return [int(d) for d in str(format(self.count, '#06b'))[2:]]

    def clr(self):
        self.count = 0


class Register:
    def __init__(self, size) -> None:
        self.size = size
        self.data = [0 for i in range(size)]

    def set(self, data):
        self.data = data

    def clr(self):
        self.data = [0 for i in range(self.size)]

# class Memory_Address_Register:
#     def __init__(self) -> None:
#         self.address = [0 for i in range(4)]

#     def set(self, address):
#         self.address = address

#     def clr(self):
#         self.address = [0 for i in range(4)]


class Memory:
    def __init__(self) -> None:
        self.state = [[0 for a in range(8)] for a in range(16)]

    def set(self, register, data):
        self.state[bin_array_to_int(register)] = data

    def read(self, register: list[int]):
        return self.state[bin_array_to_int(register)]

    def clr(self):
        self.state = [[0 for a in range(8)] for a in range(16)]


class Control_Unit:
    def __init__(self) -> None:
        self.state = [0, 0, 0, 0, 0, 1]

    def inc(self):
        _tmp = deque(self.state)
        _tmp.rotate(-1)
        self.state = list(_tmp)

    def clr(self):
        self.state = [0, 0, 0, 0, 0, 1]


class Bus():
    def __init__(self) -> None:
        self.data = [0, 0, 0, 0, 0, 0, 0, 0]

    def set(self, data):
        self.data = data

    def clr(self):
        self.data = [0, 0, 0, 0, 0, 0, 0, 0]


class Instruction_Register(Register):
    def get_opcode(self):
        return self.data[:4]

    def get_operand(self):
        return self.data[4:]


def bin_array_to_int(array) -> int:
    return int(''.join(map(str, array)), 2)


def int_to_bin_list(b):
    return [int(d) for d in str(format(b, '#010b'))[2:]]


def binary_addition(a, b):
    _a = bin_array_to_int(a)
    _b = bin_array_to_int(b)
    _sum = _a + _b
    return int_to_bin_list(_sum)


def binary_subtraction(a, b):
    _a = bin_array_to_int(a)
    _b = bin_array_to_int(b)
    _sum = _a - _b
    if _sum < 1:
        _sum = bin(_sum & (2**8 - 1))
        _sum = int(_sum, 2)
    return int_to_bin_list(_sum)


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

    mem.set([0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 1, 1])
    mem.set([0, 0, 0, 1], [0, 0, 1, 0, 1, 0, 1, 1])
    mem.set([0, 0, 1, 0], [1, 1, 1, 0, 0, 0, 0, 0])
    mem.set([0, 0, 1, 1], [1, 1, 1, 1, 0, 0, 0, 0])
    mem.set([1, 1, 1, 1], [0, 0, 0, 0, 0, 1, 1, 1])
    mem.set([1, 0, 1, 1], [0, 0, 0, 0, 0, 0, 1, 1])
    # print(binary_subtraction(
    #     [0, 0, 0, 0, 0, 0, 1, 1], [0, 0, 0, 0, 0, 1, 1, 1]))
    while(run_flag):
        for i in range(6):
            if cu.state[5] == 1:
                bus.set(pc.read())
                mar.set(bus.data)
            if cu.state[4] == 1:
                pc.inc()
            if cu.state[3] == 1:
                _add = mem.read(mar.data)
                bus.set(_add)
                ir.set(bus.data)
            if cu.state[2] == 1:
                # check for LDA
                if ir.get_opcode() == [0, 0, 0, 0]:
                    bus.set(ir.get_operand())
                    mar.set(bus.data)
                # check for ADD or SUB
                if ir.get_opcode() == [0, 0, 0, 1] or ir.get_opcode() == [0, 0, 1, 0]:
                    bus.set(ir.get_operand())
                    mar.set(bus.data)
                # check for OUT
                if ir.get_opcode() == [1, 1, 1, 0]:
                    bus.set(acc.data)
                    out.set(bus.data)
                    print(out.data)
                # check for HLT
                if ir.get_opcode() == [1, 1, 1, 1]:
                    run_flag = False
                    break
            if cu.state[1] == 1:
                # ADD
                if ir.get_opcode() == [0, 0, 0, 0]:
                    _data = mem.read(bus.data)
                    bus.set(_data)
                    acc.set(bus.data)
                # SUB
                if ir.get_opcode() == [0, 0, 0, 1] or ir.get_opcode() == [0, 0, 1, 0]:
                    _data = mem.read(bus.data)
                    bus.set(_data)
                    b_reg.set(bus.data)

            if cu.state[0] == 1:
                # ADD
                if ir.get_opcode() == [0, 0, 0, 1]:
                    _sum = binary_addition(acc.data, b_reg.data)
                    bus.set(_sum)
                    acc.set(bus.data)
                # SUB
                if ir.get_opcode() == [0, 0, 1, 0]:
                    _sum = binary_subtraction(acc.data, b_reg.data)
                    bus.set(_sum)
                    acc.set(bus.data)
            cu.inc()
