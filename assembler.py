from utils import hex_to_bin, hex_to_int, int_to_bin


def assemble(path):
    progam = [int_to_bin(0, 8) for a in range(16)]
    with open(path) as f:
        lines = f.readlines()
        i = 0
        for line in lines:
            d = line.strip().split(' ')
            opcode = opcode_lookup(d[0])
            if isinstance(opcode, int):
                operand = hex_to_bin(d[1], 8)
                progam[opcode] = operand
            else:
                if len(d) > 1:
                    operand = hex_to_bin(d[1], 4)
                else:
                    operand = '0000'
                progam[i] = opcode + operand
                i += 1
    return progam


def opcode_lookup(mnemonic):
    if mnemonic == 'LDA':
        return '0000'
    if mnemonic == 'ADD':
        return '0001'
    if mnemonic == 'SUB':
        return '0010'
    if mnemonic == 'OUT':
        return '1110'
    if mnemonic == 'HLT':
        return '1111'
    else:
        return hex_to_int(mnemonic)


def hexdump(prog):
    for line in prog:
        bin = int(line, 2)
        print(hex(bin))


if __name__ == '__main__':
    prog = assemble('prog.txt')
    hexdump(prog)
    # print(hex_to_int('FH'))
