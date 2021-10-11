import os
from collections import Counter

JIT_COMPILER_ENV = ""
JIT_COMPILER_BIN_PATH = "timeout 10 /home/jfmcoronel/d8 "
JIT_COMPILER_FLAGS = "--trace-turbo-reduction"
CURRENT_FUZZ_INPUT_PATH = "/home/jfmcoronel/die/output-0/.cur_input"
JIT_COMPILER_FEEDBACK_FILEPATH = "/home/jfmcoronel/die/output-0/.eevee_dump"
JIT_COMPILER_FEEDBACK_CMD = f"{JIT_COMPILER_ENV} {JIT_COMPILER_BIN_PATH} {JIT_COMPILER_FLAGS} {CURRENT_FUZZ_INPUT_PATH} 2>&1 {JIT_COMPILER_FEEDBACK_FILEPATH}"


def emit_key():
    ctr = Counter()

    with open(JIT_COMPILER_FEEDBACK_FILEPATH, "r") as f:
        lines = f.readlines()

    for line in lines:
        reducer = line.rsplit(' ', maxsplit=1)[-1].strip()
        ctr[reducer] += 1

    key_parts = []
    for key in ctr:
        key = key.strip().rsplit(' ', maxsplit=1)[-1].strip()
        key_parts.append(f"{key}{ctr[key]}")

    final_key = "".join(key_parts) + "\0"

    with open(JIT_COMPILER_FEEDBACK_FILEPATH, "w") as f:
        f.write(final_key)

os.system(JIT_COMPILER_FEEDBACK_CMD)
emit_key()
