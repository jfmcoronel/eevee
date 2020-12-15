import os
from collections import Counter

JSC_ENV = "JSC_useConcurrentJIT=false JSC_logCompilationChanges=true"
JSC_BIN_PATH = "timeout 10 /home/jfmcoronel/jsc"
CURRENT_INPUT_PATH = "/home/jfmcoronel/die/output-0/.cur_input"
OUTPUT_FILEPATH = "/home/jfmcoronel/die/output-0/.eevee_dump"

JSC_CMD = f"{JSC_ENV} {JSC_BIN_PATH} {CURRENT_INPUT_PATH} 2> {OUTPUT_FILEPATH}"


def emit_key():
    with open(OUTPUT_FILEPATH, "r") as f:
        lines = f.readlines()

    ctr = Counter()

    for line in lines:
        line = line.strip()
        if "changed the IR" in line:
            ctr[line] += 1

    key_parts = []
    for key in ctr:
        new_key = key.replace("Phase ", "").replace(" changed the IR.", "").replace(" ", "")
        key_parts.append(f"{new_key}{ctr[key]}")

    key = "".join(key_parts) + "\0"

    with open(OUTPUT_FILEPATH, "w") as f:
        f.write(key)


os.system(JSC_CMD)
emit_key()
