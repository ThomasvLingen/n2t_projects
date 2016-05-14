__author__ = 'mafn'

from CodeWriter.code_writer_core import CodeWriterCore

from CodeWriter.arithmetic_writer import ArithMethicWriter
from CodeWriter.push_pop_writer import PushPopWriter

class CodeWriter(CodeWriterCore):

    def __init__(self, output, filename):
        super().__init__(output)
        self.output = output
        self.filename = filename

        self.arith_writer = ArithMethicWriter(self.output)
        self.push_pop_writer = PushPopWriter(self.output, filename)

    def write_program_init(self):
        self._write_set_register("SP", 256)
        self._write_set_register("LCL", 300)
        self._write_set_register("ARG", 400)
        self._write_set_register("THIS", 3000)
        self._write_set_register("THAT", 3010)

    def write_push_pop(self, command, segment, index):
        self.push_pop_writer.write_push_pop(command, segment, index)

    def write_arithmetic(self, command):
        self.arith_writer.write_arithmetic(command)
