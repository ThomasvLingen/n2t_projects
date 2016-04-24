#! /usr/bin/env python3
__author__ = 'mafn'

from parser import HackParser
import sys

if __name__ == "__main__":
    if not len(sys.argv) == 2:
        print("usage: HACKassembler.py [.asm file]")
        exit(-1)

    filename = sys.argv[1]

    parser = HackParser(filename)