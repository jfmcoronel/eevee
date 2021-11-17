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
keycount_path = os.path.join(output_basepath, ".olivine_keycount")
key_log_path = os.path.join(output_basepath, "log-keys.txt")


def get_jsc_key(lines: List[str]):
    ctr = Counter()  # type: Counter[str]

    for line in lines:
        line = line.strip()
        if ' changed the IR.' in line:
            ctr[line] += 1

    key_parts: List[str] = []
    for key in ctr:
        new_key = key.replace("Phase ", "").replace(" changed the IR.", "").replace(" ", "").strip()
        key_parts.append(f"{new_key}{ctr[key]}")

    return "".join(key_parts)


def get_jsc_has_optset(dump: str):
    return ' changed the IR.' in dump


def get_v8_key(lines: List[str]):
    ctr = Counter()  # type: Counter[str]

    for line in lines:
        if ' by reducer ' in line:
            reducer = line.rsplit(' ', maxsplit=1)[-1].strip()
            ctr[reducer] += 1

    key_parts: List[str] = [f"{key}{ctr[key]}" for key in ctr]

    return "".join(key_parts)


def get_v8_has_optset(dump: str):
    return ' by reducer ' in dump


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


def get_ch_has_optset(dump: str):
    return 'IR after' in dump


if __name__ == '__main__':
    key_map = {
        JSC: get_jsc_key,
        V8: get_v8_key,
        CH: get_ch_key,
    }

    has_optset_map = {
        JSC: get_jsc_has_optset,
        V8: get_v8_has_optset,
        CH: get_ch_has_optset,
    }

    key_fn = key_map[jit_compiler_type_number]
    has_optset = has_optset_map[jit_compiler_type_number]


    with open(jit_compiler_feedback_filepath, "r", errors="ignore") as f:
        dump = f.read()


    if has_optset(dump):
        key = '@@@' + key_fn(dump.split('\n'))

        r = redis.Redis(host='localhost', port=6379, db=0)
        count = r.incr(key, 1)

        with open(keycount_path, 'wb') as f:
            f.write(count.to_bytes(8, 'little'))

        with open(key_log_path, 'a') as f:
            f.write(f'{key} {count}\n')

    else:
        with open(keycount_path, 'wb') as f:
            f.write((0).to_bytes(8, 'little'))
