#! /usr/bin/env python3
__author__ = 'mafn'

import sys
from vm_file_translator import VmFileTranslator

if __name__ == "__main__":
    if not len(sys.argv) == 2:
        print("usage: VM_TO_HACK.py [.asm file]")
        exit(-1)

    filename = sys.argv[1]

    translator = VmFileTranslator(filename)