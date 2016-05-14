__author__ = 'mafn'

import os

class Translator:
    def __init__(self, input_file_path):
        input_file = open(input_file_path, 'r')
        self.input = input_file.readlines()
        input_file.close()

        self.output_file_path = ""
        self.output = []

        self.current_line_index = 0

    def get_out_path(self, input_file_path, extension):
        output_file_path = os.getcwd()
        output_file_path += os.path.sep
        output_file_path += self.get_filename(input_file_path) + extension
        return output_file_path

    def get_filename(self, input_file_path):
        return os.path.splitext(os.path.basename(input_file_path))[0]

    def current_line(self):
        return self.input[self.current_line_index]

    def has_more_commands(self):
        return self.current_line_index < len(self.input)

    def save_to_file(self):
        output_file = open(self.output_file_path, 'w')

        for line in self.output:
            output_file.write("{}\n".format(line))