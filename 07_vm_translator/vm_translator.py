__author__ = 'mafn'

from translator import Translator
from enum import Enum

class CommandType(Enum):
    C_ARITH = 1
    C_PUSH = 2
    C_POP = 3
    C_LABEL = 4
    C_GOTO = 5
    C_IF = 6
    C_FUNCTION = 7
    C_RETURN = 8
    C_CALL = 9

class VmTranslator(Translator):

    arithmetic_keywords = ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]

    def __init__(self, input_file_path):
        super().__init__(input_file_path)

        self.output_file_path = self.get_out_path(input_file_path, ".vm.asm")

        self.preprocess()
        self.translate()

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

    def translate(self):
        while self.has_more_commands():
            self.current_command = self.current_line().split(' ')

            if len(self.current_command) > 0:
                command_type = self.get_command_type()

                if not command_type == CommandType.C_RETURN:
                    arg1 = self.get_arg1(command_type)
                else:
                    arg1 = ""

                if command_type in [CommandType.C_PUSH, CommandType.C_PUSH, CommandType.C_FUNCTION, CommandType.C_CALL]:
                    arg2 = self.get_arg2(command_type)
                else:
                    arg2 = ""

                if arg1 and arg2:
                    print("{}({} {})".format(command_type, arg1, arg2))
                elif arg1 and not arg2:
                    print("{}({})".format(command_type, arg1))
                elif not arg1 and not arg2:
                    print("{}()".format(command_type))

            self.current_line_index += 1

    def get_command_type(self):
        if len(self.current_command) == 1 and self.current_command[0] in self.arithmetic_keywords:
            return CommandType.C_ARITH

        if self.current_command[0] == "push":
            return CommandType.C_PUSH

        if self.current_command[0] == "pop":
            return CommandType.C_POP

        print("Can't identify the command on line {}".format(self.current_line_index))

    def get_arg1(self, command_type):
        if command_type == CommandType.C_RETURN:
            print("WARNING: arg1 SHOULD NOT BE CALLED! LINE: {}".format(self.current_line_index))

        if command_type == CommandType.C_ARITH:
            return self.current_command[0]
        else:
            return self.current_command[1]

    def get_arg2(self, command_type):
        if command_type not in [CommandType.C_PUSH, CommandType.C_PUSH, CommandType.C_FUNCTION, CommandType.C_CALL]:
            print("WARNING: arg2 SHOULD NOT BE CALLED! LINE: {}".format(self.current_line_index))

        if self.current_command[2].isdigit():
            return self.current_command[2]