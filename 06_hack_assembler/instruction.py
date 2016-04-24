__author__ = 'mafn'

class Instruction:

    dest_mapping = {
        "A": 0,
        "D": 1,
        "M": 2
    }

    jump_mapping = {
        "JGT": "001",
        "JEQ": "010",
        "JGE": "011",
        "JLT": "100",
        "JNE": "101",
        "JLE": "110",
        "JMP": "111"
    }

    comp_mapping = {
        # a bit = 0
        "0"  : "0101010",
        "1"  : "0111111",
        "-1" : "0111010",
        "D"  : "0001100",
        "A"  : "0110000",
        "!D" : "0001101",
        "!A" : "0110001",
        "-D" : "0001111",
        "-A" : "0110011",
        "D+1": "0011111",
        "A+1": "0110111",
        "D-1": "0001110",
        "A-1": "0110010",
        "D+A": "0000010",
        "A+D": "0000010",
        "D-A": "0010011",
        "A-D": "0000111",
        "D&A": "0000000",
        "A&D": "0000000",
        "D|A": "0010101",
        "A|D": "0010101",
        # a bit = 1
        "M"  : "1110000",
        "!M" : "1110001",
        "-M" : "1110011",
        "M+1": "1110111",
        "M-1": "1110010",
        "D+M": "1000010",
        "M+D": "1000010",
        "D-M": "1010011",
        "M-D": "1000111",
        "D&M": "1000000",
        "M&D": "1000000",
        "D|M": "1010101",
        "M|D": "1010101"
    }

    def dest(self, dest):
        d = ['0', '0', '0']

        for key, value in self.dest_mapping.items():
            if key in dest:
                d[value] = '1'

        return "".join(d)

    def jump(self, jump):
        if jump in self.jump_mapping:
            return self.jump_mapping[jump]
        else:
            return "ERROR"

    def comp(self, comp):
        if comp in self.comp_mapping:
            return self.comp_mapping[comp]
        else:
            return "ERROR"