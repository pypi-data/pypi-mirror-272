import subprocess
import os

nand2tetris_path = "C://Users/brand/projects/nand2tetris/nand2tetris/"
cpu_emulator_path = nand2tetris_path + "tools/CPUEmulator.bat"


def run_test(
    vm_code_path,
    assembly_output_path,
    cpu_emulator_path,
    test_file_path,
    test_output_path,
    test_compare_path,
):
    # Run the VMTranslator just as we would from the command line
    subprocess.run(
        [
            "python",
            "VMTranslator/translator.py",
            vm_code_path,
            "--dest",
            assembly_output_path,
        ]
    )
    subprocess.run([cpu_emulator_path, test_file_path])
    ## read the output file and compare it to the expected output
    with open(test_output_path, "r") as f:
        output = f.read()

    with open(test_compare_path, "r") as f:
        expected_output = f.read()

    assert output == expected_output
    try:
        os.remove(test_output_path)
        os.remove(assembly_output_path)
    except PermissionError as e:
        print(f"Unable to cleanup either {test_output_path} or {assembly_output_path}")


def test_basic():
    test_path = nand2tetris_path + "projects/7/MemoryAccess/BasicTest/"
    test_file_path = test_path + "BasicTest.tst"
    vm_code_path = test_path + "BasicTest.vm"
    # the default test files expect the assembly file to be in the same directory as the test file
    assembly_output_path = test_path + "BasicTest.asm"
    test_output_path = test_path + "BasicTest.out"
    test_compare_path = test_path + "BasicTest.cmp"
    run_test(
        vm_code_path,
        assembly_output_path,
        cpu_emulator_path,
        test_file_path,
        test_output_path,
        test_compare_path,
    )


def test_static():
    test_path = nand2tetris_path + "projects/7/MemoryAccess/StaticTest/"
    test_file_path = test_path + "StaticTest.tst"
    vm_code_path = test_path + "StaticTest.vm"
    # the default test files expect the assembly file to be in the same directory as the test file
    assembly_output_path = test_path + "StaticTest.asm"
    test_output_path = test_path + "StaticTest.out"
    test_compare_path = test_path + "StaticTest.cmp"
    run_test(
        vm_code_path,
        assembly_output_path,
        cpu_emulator_path,
        test_file_path,
        test_output_path,
        test_compare_path,
    )


def test_pointer():
    test_path = nand2tetris_path + "projects/7/MemoryAccess/PointerTest/"
    test_file_path = test_path + "PointerTest.tst"
    vm_code_path = test_path + "PointerTest.vm"
    # the default test files expect the assembly file to be in the same directory as the test file
    assembly_output_path = test_path + "PointerTest.asm"
    test_output_path = test_path + "PointerTest.out"
    test_compare_path = test_path + "PointerTest.cmp"
    run_test(
        vm_code_path,
        assembly_output_path,
        cpu_emulator_path,
        test_file_path,
        test_output_path,
        test_compare_path,
    )


def test_simple_add():
    test_path = nand2tetris_path + "projects/7/StackArithmetic/SimpleAdd/"
    test_file_path = test_path + "SimpleAdd.tst"
    vm_code_path = test_path + "SimpleAdd.vm"
    # the default test files expect the assembly file to be in the same directory as the test file
    assembly_output_path = test_path + "SimpleAdd.asm"
    test_output_path = test_path + "SimpleAdd.out"
    test_compare_path = test_path + "SimpleAdd.cmp"
    run_test(
        vm_code_path,
        assembly_output_path,
        cpu_emulator_path,
        test_file_path,
        test_output_path,
        test_compare_path,
    )
