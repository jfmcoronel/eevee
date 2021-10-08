import os
from collections import Counter

V8_ENV = ""
V8_BIN_PATH = "timeout 10 /home/jfmcoronel/die/engines/v8/v8/out/x64.release/d8 --trace-turbo-reduction"
CURRENT_INPUT_PATH = "/home/jfmcoronel/die/output-0/.cur_input"
OUTPUT_FILEPATH = "/home/jfmcoronel/die/output-0/.eevee_dump"

V8_CMD = f"{V8_ENV} {V8_BIN_PATH} {CURRENT_INPUT_PATH} 2> {OUTPUT_FILEPATH}"


def emit_key():
    ctr = Counter()

    with open(OUTPUT_FILEPATH, "r") as f:
        lines = f.readlines()

    for line in lines:
        reducer = line.rsplit(' ', maxsplit=1)[-1].strip()
        ctr[reducer] += 1

    key_parts = []
    for key in ctr:
        key = key.strip().rsplit(' ', maxsplit=1)[-1].strip()
        key_parts.append(f"{key}{ctr[key]}")

    final_key = "".join(key_parts) + "\0"
    print(final_key)


os.system(V8_CMD)
emit_key()
