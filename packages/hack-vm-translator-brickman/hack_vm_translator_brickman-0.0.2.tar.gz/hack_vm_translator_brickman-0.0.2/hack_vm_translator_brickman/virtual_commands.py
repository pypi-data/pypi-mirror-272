from atomic_commands import (
    decrement_stack_pointer,
    increment_stack_pointer,
    put_D_on_top_of_stack,
    put_value_at_stack_pointer_on_D,
    put_array_value_on_D,
    put_D_on_array,
)


def comment(comment: str):
    return f"// SRC COMMENT: {comment}"


def whitespace():
    return f""


def push_constant(const):
    return f"""\
@{const}
D=A
{put_D_on_top_of_stack()}
{increment_stack_pointer()}
"""


def push(stack_name, offset):
    return f"""\
{put_array_value_on_D(stack_name, offset)}
{put_D_on_top_of_stack()}
{increment_stack_pointer()}
"""


def pop(stack_name, offset):
    return f"""\
{decrement_stack_pointer()}
{put_value_at_stack_pointer_on_D()}
{put_D_on_array(stack_name, offset)}
"""


pointer_code_to_addr = {0: 3, 1: 4}


def push_pointer(code):
    addr = pointer_code_to_addr[code]
    return f"""\
@{addr}
D=M
{put_D_on_top_of_stack()}
{increment_stack_pointer()}
"""


def pop_pointer(code):
    addr = pointer_code_to_addr[code]
    return f"""\
{decrement_stack_pointer()}
{put_value_at_stack_pointer_on_D()}
@{addr}
M=D
"""


def binary_operations(op):
    # M op D
    opcode_to_assembly = {
        "add": "D=M+D",
        "sub": "D=M-D",
        "and": "D=D&M",
        "or": "D=D|M",
    }
    return f"""\
// put last value in stack into D
@0
A=M
A=A-1
D=M
// set second to last value into M
A=A-1
// run operation {op} and save to D
{opcode_to_assembly[op]}
// decrement stack pointer once (two values have become one)
@0
M=M-1
// Replace value on top of stack
@0
A=M
A=A-1
M=D
"""
