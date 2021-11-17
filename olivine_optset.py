import os
import subprocess
import sys

from olivine_helpers import get_fuzz_target_string_with_flags
from olivine_hook import (
    get_ch_has_optset,
    get_ch_key,
    get_jsc_has_optset,
    get_jsc_key,
    get_v8_has_optset,
    get_v8_key,
)


if __name__ == '__main__':
    jit_compiler_code, fuzz_input_path = sys.argv[1:]
    os.system(f'cat {fuzz_input_path}')

    input('-- Press ENTER to start --')

    full_fuzz_target_str = get_fuzz_target_string_with_flags(jit_compiler_code)
    cmd = f'time {full_fuzz_target_str} {fuzz_input_path}'

    print(cmd)

    output = subprocess.check_output(cmd, shell=True).decode('utf8', errors='ignore')
    print(output)

    print()
    input('-- Press ENTER to continue --')

    print()

    key_map = {
        'jsc': get_jsc_key,
        'v8': get_v8_key,
        'ch': get_ch_key,
    }

    has_optset_map = {
        'jsc': get_jsc_has_optset,
        'v8': get_v8_has_optset,
        'ch': get_ch_has_optset,
    }

    if jit_compiler_code in has_optset_map:
        if has_optset_map[jit_compiler_code](output):
            print(key_map[jit_compiler_code](output.split('\n')))
        else:
            print('No JIT dump')
    else:
        assert False, f'{jit_compiler_code} not supported'

