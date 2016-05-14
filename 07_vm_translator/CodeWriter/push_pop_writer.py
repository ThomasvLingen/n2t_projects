__author__ = 'mafn'

from CodeWriter.code_writer_core import CodeWriterCore
from command_type import CommandType

class PushPopWriter(CodeWriterCore):
    def __init__(self, parent_output, filename):
        super().__init__(parent_output)
        self.filename = filename

    def write_push_pop(self, command, segment, index):
        if command == CommandType.C_POP:
            self._write_decrement_sp()

        if segment == "constant":
            self._write_stack(index)

        if segment in ["local", "argument", "this", "that", "temp", "pointer", "static"]:
            base_pointer = self._get_base_pointer(segment)

            if command == CommandType.C_POP:
                self._write_segment_from_stack(base_pointer, index)
            if command == CommandType.C_PUSH:
                self._write_segment_to_stack(base_pointer, index)

        if command == CommandType.C_PUSH:
            self._write_increment_sp()

    def _write_segment_from_stack(self, base, index):
        self._write_dest_in_r15(base, index)
        self._write_set_address_to_sp()
        self._write_commands(
            "D=M",          # D = stack value
            "@R15",
            "A=M",          # A = dest
            "M=D"           # destination = stack value
        )

    def _write_to_r15(self, value):
        self._write_commands(
                "@" + str(value),
                "D=A",
                "@R15",
                "M=D"
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
            self._write_to_r15(destination_address)
        if base == "pointer":
            if int(index) == 0:
                self._write_to_r15(3)
            if int(index) == 1:
                self._write_to_r15(4)
        if base == "static":
            destination_address = str("{}.{}".format(self.filename, index))
            self._write_to_r15(destination_address)

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
        if base == "pointer":
            if int(index) == 0:
                self._write_address_contents_in_D(3)
            if int(index) == 1:
                self._write_address_contents_in_D(4)
        if base == "static":
            destination_address = str("{}.{}".format(self.filename, index))
            self._write_address_contents_in_D(destination_address)
