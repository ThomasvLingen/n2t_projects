__author__ = 'mafn'

class CodeWriterCore():
    def __init__(self, target_output):
        self.output = target_output

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