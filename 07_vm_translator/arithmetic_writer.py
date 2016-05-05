__author__ = 'mafn'

from code_writer_core import CodeWriterCore

class ArithMethicWriter(CodeWriterCore):

    def __init__(self, parent_output):
        super().__init__(parent_output)

        self._arith_commands_map = {
            "add": self._write_add,
            "sub": self._write_sub,
            "neg": self._write_neg,
            "and": self._write_and,
            "or" : self._write_or,
            "not": self._write_not,
            "eq" : self._write_eq,
            "gt" : self._write_gt,
            "lt" : self._write_lt
        }

        self.arith_label_counter = 0

    def write_arithmetic(self, command):
        if command not in ["neg", "not"]:
            self._load_stack_top_2()
        else:
            self._load_stack_top_1()

        if command in ["eq", "gt", "lt"]:
            arith_label = self._generate_arith_label()
        else:
            arith_label = ""

        write_function = self._arith_commands_map[command]
        write_function(arith_label)

        self._write_increment_sp()

    def _write_add(self, arithmetic_label):
        self._write_commands("M=M+D")

    def _write_sub(self, arithmetic_label):
        self._write_commands("M=M-D")

    def _write_neg(self, arithmetic_label):
        self._write_commands("M=-M")

    def _write_and(self, arithmetic_label):
        self._write_commands("M=M&D")

    def _write_or(self, arithmetic_label):
        self._write_commands("M=M|D")

    def _write_not(self, arithmetic_label):
        self._write_commands("M=!M")

    def _write_eq(self, arithmetic_label):
        self._write_commands(
            "D=M-D",
            "M=-1",
            "@{}".format(arithmetic_label),
            "D;JEQ"
        )
        self._write_set_address_to_sp()
        self._write_commands(
            "M=0",
            "({})".format(arithmetic_label)
        )

    def _write_gt(self, arithmetic_label):
        self._write_commands(
            "D=M-D",
            "M=-1",
            "@{}".format(arithmetic_label),
            "D;JGT"
        )
        self._write_set_address_to_sp()
        self._write_commands(
            "M=0",
            "({})".format(arithmetic_label)
        )

    def _write_lt(self, arithmetic_label):
        self._write_commands(
            "D=D-M",
            "M=-1",
            "@{}".format(arithmetic_label),
            "D;JGT"
        )
        self._write_set_address_to_sp()
        self._write_commands(
            "M=0",
            "({})".format(arithmetic_label)
        )

    def _generate_arith_label(self):
        label = "al_" + str(self.arith_label_counter)
        self.arith_label_counter += 1
        return label