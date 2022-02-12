from collections import deque
from assembler import assemble
from utils import int_to_bin, binary_addition, binary_subtraction


class ProgramCounter:
    def __init__(self) -> None:
        self.count = 0

    def __str__(self) -> str:
        return int_to_bin(self.count, 4)

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
        self.data = int_to_bin(0, size)

    def __str__(self) -> str:
        return self.data

    def set(self, data):
        self.data = data

    def clr(self):
        self.data = int_to_bin(0, self.size)


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

    def __str__(self) -> str:
        return self.state

    def inc(self):
        _tmp = deque(self.state)        # convert to deque object
        _tmp.rotate(-1)                 # rotate the list
        self.state = "".join(_tmp)      # join back to a string

    def clr(self):
        self.state = int_to_bin(1, 6)


class Bus():
    def __init__(self) -> None:
        self.data = int_to_bin(0, 8)

    def __str__(self) -> str:
        return self.data

    def set(self, data):
        _len = len(data)
        if _len < 8:
            self.data = '0'*_len + data
        else:
            self.data = data

    def clr(self):
        self.data = int_to_bin(0, 8)


class Instruction_Register(Register):
    def get_opcode(self):
        return self.data[:4]

    def get_operand(self):
        return self.data[4:]


class SAP_1():
    def __init__(self) -> None:
        self.mem = Memory()
        self.cu = Control_Unit()
        self.mar = Register(4)
        self.pc = ProgramCounter()
        self.bus = Bus()
        self.ir = Instruction_Register(8)
        self.b_reg = Register(8)
        self.acc = Register(8)
        self.out = Register(8)

    def program(self, data):
        self.mem.program(data)

    def memory_dump(self, hexa=False):
        for line in prog:
            if hexa:
                bin = int(line, 2)
                print(hex(bin))
            else:
                print(line)

    def _dump_state(self, cycle: int):
        print("Cycle: {:02d} | PC: {} | MAR: {} | BUS: {} | IR: {} | A: {} | B: {} | O: {}".format(
            cycle, self.pc, self.mar, self.bus, self.ir, self.acc, self.b_reg, self.out))

    def run(self, debug=False):
        _run = True
        cycle = 0
        while(_run):
            for i in range(6):
                if self.cu.state[5] == '1':
                    self.bus.set(self.pc.read())
                    self.mar.set(self.bus.data)
                if self.cu.state[4] == '1':
                    self.pc.inc()
                if self.cu.state[3] == '1':
                    _add = self.mem.read(self.mar.data)
                    self.bus.set(_add)
                    self.ir.set(self.bus.data)
                if self.cu.state[2] == '1':
                    # check for LDA
                    if self.ir.get_opcode() == '1111':
                        self.bus.set(self.ir.get_operand())
                        self.mar.set(self.bus.data)
                    # check for ADD or SUB
                    if self.ir.get_opcode() == '0001' or self.ir.get_opcode() == '0010':
                        self.bus.set(self.ir.get_operand())
                        self.mar.set(self.bus.data)
                    # check for OUT
                    if self.ir.get_opcode() == '1110':
                        self.bus.set(self.acc.data)
                        self.out.set(self.bus.data)
                        print(self.out.data, int(self.out.data, 2))
                    # check for HLT
                    if self.ir.get_opcode() == '1111':
                        _run = False
                        break
                if self.cu.state[1] == '1':
                    # LDA
                    if self.ir.get_opcode() == '0000':
                        _data = self.mem.read(self.bus.data)
                        self.bus.set(_data)
                        self.acc.set(self.bus.data)
                    # ADD or SUB
                    if self.ir.get_opcode() == '0001' or self.ir.get_opcode() == '0010':
                        _data = self.mem.read(self.bus.data)
                        self.bus.set(_data)
                        self.b_reg.set(self.bus.data)
                if self.cu.state[0] == '1':
                    # ADD
                    if self.ir.get_opcode() == '0001':
                        _sum = binary_addition(self.acc.data, self.b_reg.data)
                        self.bus.set(_sum)
                        self.acc.set(self.bus.data)
                    # SUB
                    if self.ir.get_opcode() == '0010':
                        _sum = binary_subtraction(
                            self.acc.data, self.b_reg.data)
                        self.bus.set(_sum)
                        self.acc.set(self.bus.data)

                self.cu.inc()

                if debug:
                    self._dump_state(cycle)
                cycle += 1


if __name__ == '__main__':
    prog = assemble('prog.txt')
    sap = SAP_1()
    sap.program(prog)
    sap.memory_dump(True)
    sap.run(False)
