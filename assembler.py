def assemble(path):
    progam = [[0 for a in range(8)] for a in range(16)]
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
                    operand = [0, 0, 0, 0]
                progam[i] = opcode + operand
                i += 1
    return progam


def opcode_lookup(mnemonic):
    if mnemonic == 'LDA':
        return [0, 0, 0, 0]
    if mnemonic == 'ADD':
        return [0, 0, 0, 1]
    if mnemonic == 'SUB':
        return [0, 0, 1, 0]
    if mnemonic == 'OUT':
        return [1, 1, 1, 0]
    if mnemonic == 'HLT':
        return [1, 1, 1, 1]
    else:
        return hex_to_int(mnemonic)


def hex_to_bin(hex, bits):
    _b = list(hex)
    _b = int(_b[0], 16)
    return int_to_bin_list(_b, bits)


def hex_to_int(hex):
    _b = list(hex)
    _b = int(_b[0], 16)
    return _b


def int_to_bin_list(b, bits):
    if bits == 4:
        return [int(d) for d in str(format(b, '#06b'))[2:]]
    return [int(d) for d in str(format(b, '#010b'))[2:]]


if __name__ == '__main__':
    print(assemble('prog.txt'))
    # print(hex_to_int('FH'))
