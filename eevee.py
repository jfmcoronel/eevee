import os
from collections import Counter

JIT_COMPILER_ENV = ""
JIT_COMPILER_BIN_PATH = "timeout 10 /home/jfmcoronel/ch"
JIT_COMPILER_FLAGS = "-bgjit- -dump:backend"
CURRENT_FUZZ_INPUT_PATH = "/home/jfmcoronel/die/output-0/.cur_input"
JIT_COMPILER_FEEDBACK_FILEPATH = "/home/jfmcoronel/die/output-0/.eevee_dump"
JIT_COMPILER_FEEDBACK_CMD = f"{JIT_COMPILER_ENV} {JIT_COMPILER_BIN_PATH} {JIT_COMPILER_FLAGS} {CURRENT_FUZZ_INPUT_PATH} > {JIT_COMPILER_FEEDBACK_FILEPATH}"

FEEDBACK_PATH = "/Users/jfmcoronel/Desktop/dcs/cs300/logs/chakra/backend.txt.3"
IGNORE_PHASES = ('Emitter', 'BackEnd')


def emit_key():
    with open(JIT_COMPILER_FEEDBACK_FILEPATH, 'r') as f:
        lines = f.readlines()

    a = None
    a_count = None
    b = None
    b_count = None
    
    ctr = Counter()

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
            if a in IGNORE_PHASES or b in IGNORE_PHASES:
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

    key = ''.join(f"{phase}{ctr[phase]}" for phase in ctr) + '\0'

    with open(JIT_COMPILER_FEEDBACK_FILEPATH, "w") as f:
        f.write(key)

os.system(JIT_COMPILER_FEEDBACK_CMD)
emit_key()
