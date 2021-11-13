from collections import Counter
import os
import sys
from typing import List

import redis


JSC = 1
V8 = 2
CH = 3

jit_compiler_type_number = int(sys.argv[1])
output_basepath = os.path.dirname(sys.argv[2])
jit_compiler_feedback_filepath = sys.argv[2]
current_fuzz_input_filepath = os.path.join(output_basepath, ".cur_input")


def get_jsc_key(lines: List[str]):
    ctr = Counter()  # type: Counter[str]

    for line in lines:
        line = line.strip()
        if "changed the IR" in line:
            ctr[line] += 1

    key_parts: List[str] = []
    for key in ctr:
        new_key = key.replace("Phase ", "").replace(" changed the IR.", "").replace(" ", "")
        key_parts.append(f"{new_key}{ctr[key]}")

    return "".join(key_parts)


def get_v8_key(lines: List[str]):
    ctr = Counter()  # type: Counter[str]

    for line in lines:
        reducer = line.rsplit(' ', maxsplit=1)[-1].strip()
        ctr[reducer] += 1

    key_parts: List[str] = []
    for key in ctr:
        key = key.strip().rsplit(' ', maxsplit=1)[-1].strip()
        key_parts.append(f"{key}{ctr[key]}")

    return "".join(key_parts)


def get_ch_key(lines: List[str]):
    ignore_phases = ('Emitter', 'BackEnd')

    a = None
    a_count = None
    b = None
    b_count = None

    ctr = Counter()  # type: Counter[str]

    for line in lines:
        if 'IR after' in line:
            _, right = line.split('IR after', maxsplit=1)
            phase, _ = right.strip().split(' ', maxsplit=1)

            if a is None:
                a = phase
            elif phase == 'BackEnd':
                a = None
                a_count = None
                b = None
                b_count = None
            else:
                a = b
                a_count = b_count
                b = phase
                b_count = None

        elif 'Instr Count:' in line:
            if a in ignore_phases or b in ignore_phases:
                continue

            _, right = line.split('Instr Count:')
            # if 'Size:' in right:
            #     # 2nd count of Emitter
            #     continue

            count = right.strip()

            if a and not b:
                a_count = count
            elif a and b:
                b_count = count
                if a_count != b_count:
                    ctr[b] += 1

    return ''.join(f"{phase}{ctr[phase]}" for phase in ctr)


def get_jit_compiler_feedback_cmd(jit_compiler_env: str, jit_compiler_bin_path: str, jit_compiler_flags: str, current_fuzz_input_filepath: str, jit_compiler_feedback_filepath: str):
    return f"{jit_compiler_env} {jit_compiler_bin_path} {jit_compiler_flags} {current_fuzz_input_filepath} > {jit_compiler_feedback_filepath}"


if jit_compiler_type_number == JSC:
    jit_compiler_env = "JSC_useConcurrentJIT=false JSC_logCompilationChanges=true"
    jit_compiler_bin_path = "timeout 10 /home/jfmcoronel/jsc"
    jit_compiler_flags = ""

    jit_compiler_feedback_cmd = get_jit_compiler_feedback_cmd(jit_compiler_env, jit_compiler_bin_path, jit_compiler_flags, current_fuzz_input_filepath, jit_compiler_feedback_filepath)
    key_fn = get_jsc_key

elif jit_compiler_type_number == V8:
    jit_compiler_env = ""
    jit_compiler_bin_path = "timeout 10 /home/jfmcoronel/v8-afl-dir/v8/out/Debug/d8"
    jit_compiler_flags = "--trace-turbo-reduction"
    current_fuzz_input_path = "/home/jfmcoronel/die/output-0/.cur_input"

    jit_compiler_feedback_cmd = get_jit_compiler_feedback_cmd(jit_compiler_env, jit_compiler_bin_path, jit_compiler_flags, current_fuzz_input_filepath, jit_compiler_feedback_filepath)
    key_fn = get_v8_key

elif jit_compiler_type_number == CH:
    jit_compiler_env = ""
    jit_compiler_bin_path = "timeout 10 /home/jfmcoronel/ch"
    jit_compiler_flags = "-bgjit- -dump:backend"
    current_fuzz_input_path = "/home/jfmcoronel/die/output-0/.cur_input"

    jit_compiler_feedback_cmd = get_jit_compiler_feedback_cmd(jit_compiler_env, jit_compiler_bin_path, jit_compiler_flags, current_fuzz_input_filepath, jit_compiler_feedback_filepath)
    key_fn = get_ch_key

else:
    print('Error')
    sys.exit(-1)


# Execute JIT compiler for feedback
print(jit_compiler_feedback_cmd)
os.system(jit_compiler_feedback_cmd)

with open(jit_compiler_feedback_filepath, "r") as f:
    lines = f.readlines()

key = '@@@' + key_fn(lines)

r = redis.Redis(host='localhost', port=6379, db=0)
count = r.incr(key, 1)

with open(jit_compiler_feedback_filepath, 'wb') as f:
    f.write(count.to_bytes(8, 'little'))
