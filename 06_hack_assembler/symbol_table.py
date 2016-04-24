__author__ = 'mafn'

class SymbolTable:
    def __init__(self):
        self.table = {}
        self.current_variable_address = 16

        self.add_presets()

    def add_presets(self):
        self.table.update({
            "R0" : 0,
            "R1" : 1,
            "R2" : 2,
            "R3" : 3,
            "R4" : 4,
            "R5" : 5,
            "R6" : 6,
            "R7" : 7,
            "R8" : 8,
            "R9" : 9,
            "R10": 10,
            "R11": 11,
            "R12": 12,
            "R13": 13,
            "R14": 14,
            "R15": 15,
            "SCREEN": 16384,
            "KBD": 24576,
            "SP": 0,
            "LCL": 1,
            "ARG": 2,
            "THIS": 3,
            "THAT": 4
        })

    def add_variable(self, symbol):
        if not self.contains(symbol):
            self.table[symbol] = self.current_variable_address

            self.current_variable_address += 1

    def add_label(self, symbol, address):
        if not self.contains(symbol):
            self.table[symbol] = address

    def contains(self, symbol):
        return symbol in self.table

    def get_address(self, symbol):
        if self.contains(symbol):
            return self.table[symbol]
        else:
            return -1
