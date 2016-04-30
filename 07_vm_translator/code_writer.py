__author__ = 'mafn'

from command_type import CommandType


class CodeWriter():
    def __init__(self, output):
        self.output = output

    def write_program_init(self):
        self._write_set_register("SP", 256)

    def write_push_pop(self, command, segment, index):
        if segment == "constant":
            self._write_stack(index)

        if command == CommandType.C_PUSH:
            self._write_increment_sp()

    def write_arithmetic(self, command):
        # Put top number in D
        self._write_decrement_sp()
        self._write_set_address_to_sp()
        self._write_commands("D=M")
        # Put bottom number in M
        self._write_decrement_sp()
        self._write_set_address_to_sp()

        if command == "add":
            self._write_commands("M=M+D")

        self._write_increment_sp()

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
            "@" + value,
            "D=A",
            "@" + register,
            "M=D"
        )

    def _write_stack(self, value):
        self._write_commands(
            "@" + value,
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