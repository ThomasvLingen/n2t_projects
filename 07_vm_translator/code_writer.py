__author__ = 'mafn'

from command_type import CommandType


class CodeWriter():
    def __init__(self, output):
        self.output = output

        self.arith_label_counter = 0

    def write_program_init(self):
        self._write_set_register("SP", 256)

    def write_push_pop(self, command, segment, index):
        if segment == "constant":
            self._write_stack(index)

        if command == CommandType.C_PUSH:
            self._write_increment_sp()

    def write_arithmetic(self, command):
        if command not in ["neg", "not"]:
            self._load_stack_top_2()
        else:
            self._load_stack_top_1()

        if command in ["eq", "gt", "lt"]:
            arith_label = self._generate_arith_label()

        if command == "add":
            self._write_commands("M=M+D")
        if command == "sub":
            self._write_commands("M=M-D")
        if command == "neg":
            self._write_commands("M=-M")
        if command == "and":
            self._write_commands("M=M&D")
        if command == "or":
            self._write_commands("M=M|D")
        if command == "not":
            self._write_commands("M=!M")
        if command == "eq":
            self._write_commands(
                "D=M-D",
                "M=-1",
                "@{}".format(arith_label),
                "D;JEQ"
            )
            self._write_set_address_to_sp()
            self._write_commands(
                "M=0",
                "({})".format(arith_label)
            )
        if command == "gt":
            self._write_commands(
                "D=M-D",
                "M=-1",
                "@{}".format(arith_label),
                "D;JGT"
            )
            self._write_set_address_to_sp()
            self._write_commands(
                "M=0",
                "({})".format(arith_label)
            )
        if command == "lt":
            self._write_commands(
                "D=D-M",
                "M=-1",
                "@{}".format(arith_label),
                "D;JGT"
            )
            self._write_set_address_to_sp()
            self._write_commands(
                "M=0",
                "({})".format(arith_label)
            )

        self._write_increment_sp()

    def _load_stack_top_2(self):
        # Put top number in D
        self._write_decrement_sp()
        self._write_set_address_to_sp()
        self._write_commands("D=M")
        self._load_stack_top_1()

    def _load_stack_top_1(self):
        # Put bottom number in M
        self._write_decrement_sp()
        self._write_set_address_to_sp()

    def _generate_arith_label(self):
        label = "al_" + str(self.arith_label_counter)
        self.arith_label_counter += 1
        return label

    def _write_increment_register(self, register):
        self._write_commands(
            "@" + register,
            "M=M+1"
        )

    def _write_decrement_register(self, register):
        self._write_commands(
            "@" + register,
            "M=M-1"
        )

    def _write_set_register(self, register, value):
        self._write_commands(
            "@" + str(value),
            "D=A",
            "@" + register,
            "M=D"
        )

    def _write_stack(self, value):
        self._write_commands(
            "@" + str(value),
            "D=A",
            "@SP",
            "A=M",
            "M=D"
        )

    def _write_increment_sp(self):
        self._write_increment_register("SP")

    def _write_decrement_sp(self):
        self._write_decrement_register("SP")

    def _write_set_address_to_sp(self):
        self._write_commands("@SP", "A=M")

    def _write_commands(self, *arg):
        for command in arg:
            self._write_command(command)

    def _write_command(self, command):
        self.output.append(command)