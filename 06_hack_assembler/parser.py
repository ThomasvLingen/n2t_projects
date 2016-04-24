__author__ = 'mafn'

import os
import copy

from instruction import Instruction
from symbol_table import SymbolTable

class HackParser():

    instruction = Instruction()
    symbol_table = SymbolTable()

    def __init__(self, input_file_path):
        input_file = open(input_file_path, 'r')
        self.input = input_file.readlines()
        input_file.close()

        self.output_file_path = os.path.splitext(input_file_path)[0] + ".hack"
        self.output = []

        self.current_line_index = 0

        self.preprocess()
        self.assemble()

    def preprocess(self):
        # Strip comments
        for i in range(len(self.input)):
            comment_index = self.input[i].find("//")

            if comment_index != -1:
                self.input[i] = self.input[i][0:comment_index]
        # Strip empty newlines
        self.input = [line for line in self.input if line != "\n"]
        # Strip trailing whitespace
        self.input = [line.rstrip() for line in self.input]
        # Strip leading whitespace
        self.input = [line.lstrip() for line in self.input]
        # Strip empty lines
        self.input = [line for line in self.input if line != ""]

        self.process_labels()
        self.process_variables()

    def process_labels(self):
        while self.has_more_commands():
            if self.command_type() == "L":
                self.process_label()

            self.current_line_index += 1

        self.current_line_index = 0

    def process_label(self):
        line = self.current_line()
        label = line[1:-1]

        self.symbol_table.add_label(label, self.current_line_index)

        self.input.remove(line)
        self.current_line_index -= 1

    def process_variables(self):
        while self.has_more_commands():
            if self.command_type() == "A":
                self.process_variable()

            self.current_line_index += 1

        self.current_line_index = 0

    def process_variable(self):
        line = self.current_line()
        symbol = line[1:]

        if not symbol.isdigit():
            if not self.symbol_table.contains(symbol):
                self.symbol_table.add_variable(symbol)

            address = self.symbol_table.get_address(symbol)
            self.input[self.current_line_index] = "@" + str(address)

    def assemble(self):
        parse_functions = {
            "A": self.parse_A,
            "C": self.parse_C
        }

        while self.has_more_commands():
            output_line = parse_functions[self.command_type()]()
            self.output.append(output_line)

            self.current_line_index += 1

        self.save_to_file()

    def parse_A(self):
        address = int(self.current_line()[1:])
        address = "{0:015b}".format(address)

        return "0" + address

    def parse_C(self):
        line = copy.deepcopy(self.current_line())
        dest = ""
        jump = ""

        equals_index = line.find('=')
        semicolon_index = line.find(';')

        if equals_index != -1:
            dest = line[0:equals_index]
            line = line[equals_index+1:]

        if semicolon_index != -1:
            comp = line[0:semicolon_index]
            line = line[semicolon_index+1:]
            jump = line
        else:
            comp=line

        dest_component = self.instruction.dest(dest)
        comp_component = self.instruction.comp(comp)
        jump_component = self.instruction.jump(jump)

        if jump_component == "ERROR":
            jump_component = "000"

        if dest_component == "ERROR":
            dest_component = "000"

        return "111" + comp_component + dest_component + jump_component

    def command_type(self):
        if "@" in self.current_line():
            return "A"
        elif "(" in self.current_line():
            return "L"
        else:
            return "C"

    def current_line(self):
        return self.input[self.current_line_index]

    def has_more_commands(self):
        return self.current_line_index < len(self.input)

    def save_to_file(self):
        output_file = open(self.output_file_path, 'w')

        for line in self.output:
            output_file.write("{}\n".format(line))