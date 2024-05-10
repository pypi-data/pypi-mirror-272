import argparse
import os
from typing import Tuple
from virtual_commands import (
    comment,
    whitespace,
    binary_operations,
    push,
    pop,
    push_constant,
    push_pointer,
    pop_pointer,
)

parser = argparse.ArgumentParser(
    prog="Nand2Tetris Virtual Machine Translator",
    description="Translates a toy VM language into the Hack Assembly language",
)

parser.add_argument("src", help="The source .vm file to translate")
parser.add_argument("--dest", help="The destination .asm file")


def convert_to_asm(line: str) -> str:
    """
    Dispatches a line of VM code to the proper
    assembly translation function and returns the result.

    Args:
        line (str) - a line of VM code

    Returns:
        str - the equivalent line of Hack Assembly code

    """
    if line.strip().startswith("//"):
        return comment(line)
    if line.strip() == "":
        return whitespace()
    if line in ("add", "sub", "eq", "lt", "gt", "neg", "and", "or", "not"):
        return binary_operations(line)
    command, array_name, val = line.split(" ")
    val = int(val)
    if command == "push" and array_name == "constant":
        return push_constant(val)
    if command == "push" and array_name == "pointer":
        return push_pointer(val)
    if command == "push":
        return push(array_name, val)
    if command == "pop" and array_name == "pointer":
        return pop_pointer(val)
    if command == "pop":
        return pop(array_name, val)


def main():
    args = parser.parse_args()

    assert os.path.isfile(args.src), "provided source file (src) does not exist"
    assert args.src[-3:] == ".vm", 'can only parse files with extension ".vm"'

    if not args.dest:
        args.dest = args.src[:-3] + ".asm"

    with open(args.src, "r") as f:
        program = f.read().splitlines()

    output = "\n\n".join(convert_to_asm(line) for line in program)
    with open(args.dest, "w") as f:
        f.write(output)


if __name__ == "__main__":
    main()
