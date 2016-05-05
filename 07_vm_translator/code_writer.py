__author__ = 'mafn'

from command_type import CommandType
from arithmetic_writer import ArithMethicWriter
from code_writer_core import CodeWriterCore

class CodeWriter(CodeWriterCore):

    base_pointer_map = {
        "local": "LCL",
        "argument": "ARG",
        "this": "THIS",
        "that": "THAT",
        "temp": "temp"
    }

    def __init__(self, output):
        super().__init__(output)
        self.output = output

        self.arith_writer = ArithMethicWriter(self.output)

    def write_program_init(self):
        self._write_set_register("SP", 256)
        self._write_set_register("LCL", 300)
        self._write_set_register("ARG", 400)
        self._write_set_register("THIS", 3000)
        self._write_set_register("THAT", 3010)

    def write_push_pop(self, command, segment, index):
        if command == CommandType.C_POP:
            self._write_decrement_sp()

        if segment == "constant":
            self._write_stack(index)

        if segment in ["local", "argument", "this", "that", "temp"]:
            base_pointer = self._get_base_pointer(segment)

            if command == CommandType.C_POP:
                self._write_segment_from_stack(base_pointer, index)
            if command == CommandType.C_PUSH:
                self._write_segment_to_stack(base_pointer, index)

        if command == CommandType.C_PUSH:
            self._write_increment_sp()

    def write_arithmetic(self, command):
        self.arith_writer.write_arithmetic(command)

    def _get_base_pointer(self, segment):
        return self.base_pointer_map[segment]

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

    def _write_segment_from_stack(self, base, index):
        self._write_dest_in_r15(base, index)
        self._write_set_address_to_sp()
        self._write_commands(
            "D=M",          # D = stack value
            "@R15",
            "A=M",          # A = dest
            "M=D"           # destination = stack value
        )

    def _write_dest_in_r15(self, base, index):
        if base in ["LCL", "ARG", "THIS", "THAT"]:
            self._write_commands(
                "@" + index,
                "D=A",          # load index into D
                "@" + base,     # Go to current base
                "D=D+M",        # D = index + base
                "@R15",
                "M=D"           # R15 = destination address
            )
        if base == "temp":
            destination_address = 5 + int(index)
            self._write_commands(
                "@" + str(destination_address),
                "D=A",
                "@R15",
                "M=D"
            )

    def _write_segment_to_stack(self, base, index):
        self._write_dest_contents_in_D(base, index)
        self._write_set_address_to_sp()
        self._write_commands(
            "M=D"
        )

    def _write_dest_contents_in_D(self, base, index):
        if base in ["LCL", "ARG", "THIS", "THAT"]:
            self._write_commands(
                "@" + index,
                "D=A",          # load index into D
                "@" + base,     # Go to current base
                "A=M+D",        # A = destination address
                "D=M"           # D = destination contents
            )
        if base == "temp":
            destination_address = 5 + int(index)
            self._write_commands(
                "@" + str(destination_address),
                "D=M"
            )
