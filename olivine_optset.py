import os
import sys

from olivine_helpers import get_fuzz_target_string_with_flags


if __name__ == '__main__':
    jit_compiler_code, fuzz_input_path = sys.argv[1:]

    full_fuzz_target_str = get_fuzz_target_string_with_flags(jit_compiler_code)
    cmd = f'{full_fuzz_target_str} {fuzz_input_path}'

    print(cmd)
    os.system(cmd)
