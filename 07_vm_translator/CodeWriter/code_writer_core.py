__author__ = 'mafn'

class CodeWriterCore():
    base_pointer_map = {
        "local": "LCL",
        "argument": "ARG",
        "this": "THIS",
        "that": "THAT",
        "temp": "temp",
        "pointer": "pointer",
        "static": "static"
    }

    def __init__(self, target_output):
        self.output = target_output

    def _get_base_pointer(self, segment):
        return self.base_pointer_map[segment]

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

    def _write_stack(self, value):
        self._write_commands(
            "@" + str(value),
            "D=A",
            "@SP",
            "A=M",
            "M=D"
        )

    def _write_set_register(self, register, value):
        self._write_commands(
            "@" + str(value),
            "D=A",
            "@" + register,
            "M=D"
        )

    def _write_address_contents_in_D(self, address):
        self._write_commands(
            "@" + str(address),
            "D=M"
        )