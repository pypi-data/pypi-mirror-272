array_name_to_pointer_addr = {
    "sp": 0,
    "local": 1,
    "argument": 2,
    "this": 3,
    "that": 4,
}

array_name_to_array_addr = {"temp": 5, "static": 16}


def decrement_stack_pointer():
    return f"""\
//Decrement stack pointer
@0
M=M-1
"""


def increment_stack_pointer():
    return f"""\
//Increment stack pointer
@0
M=M+1
"""


def put_D_on_top_of_stack():
    return f"""\
//Put D on top of stack
@0
A=M
M=D
"""


def put_value_at_stack_pointer_on_D():
    return f"""\
//Put value at stack pointer on D
@0
A=M
D=M
"""


def put_array_value_on_D(array_name, index):
    if array_name in array_name_to_pointer_addr:
        pointer_addr = array_name_to_pointer_addr[array_name]
        return f"""\
// Put array value on D (using pointer)
@{pointer_addr}
D=M
@{index}
A=A+D
D=M
"""
    elif array_name in array_name_to_array_addr:
        array_addr = array_name_to_array_addr[array_name]
        return f"""\
// Put array value on D (using base address)
@{array_addr + index}
D=M
"""


def put_D_on_array(array_name, index):
    if array_name in array_name_to_pointer_addr:
        pointer_addr = array_name_to_pointer_addr[array_name]
        return f"""\
// Put D on array (using pointer)
// save D in R13
@13
M=D
// Calculate the write address and save to R14
@{pointer_addr}
D=M
@{index}
D=D+A
@14
M=D
// Write original D onto write_address
@13
D=M
@14
A=M
M=D
"""
    elif array_name in array_name_to_array_addr:
        array_addr = array_name_to_array_addr[array_name]
        return f"""\
// Put D on array (using base address)
@{array_addr+index}
M=D
"""
