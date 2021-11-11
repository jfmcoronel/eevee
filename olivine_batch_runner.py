import multiprocessing
import os
import sys
import time

# Usage:
# python3 olivine_batch_runner.py start {jitCompilerCode} {seed} {untilNInputs}
# python3 olivine_batch_runner.py populate {jitCompilerCode} {seed} {untilNInputs}
# python3 olivine_batch_runner.py fuzz {jitCompilerCode} {seed} {untilNInputs}

# TODO: Timing

def execute(cmd: str):
    print(cmd)
    os.system(cmd)

def get_lib_string(jit_compiler_code: str):
    die_corpus_path = '/home/jfmcoronel/die/DIE-corpus/'

    if jit_compiler_code == 'ch':
        return f'-lib={die_corpus_path}/lib.js -lib={die_corpus_path}/jsc.js -lib={die_corpus_path}/v8.js -lib={die_corpus_path}/ffx.js -lib={die_corpus_path}/chakra.js'

    return f'{die_corpus_path}/lib.js {die_corpus_path}/jsc.js {die_corpus_path}/v8.js {die_corpus_path}/ffx.js {die_corpus_path}/chakra.js'


def get_fuzz_target_path(jit_compiler_code: str):
    if jit_compiler_code == 'jsc':
        return '/home/jfmcoronel/jsc'
    elif jit_compiler_code == 'v8':
        return '/home/jfmcoronel/d8'
    elif jit_compiler_code == 'ch':
        return '/home/jfmcoronel/ch'
    else:
        assert False, f'Invalid JIT compiler code: {jit_compiler_code}'


def run_slaves(cmd: str, prefix: str):
    slave_count = multiprocessing.cpu_count()

    for n in range(slave_count):
        new_cmd = cmd.replace('output', f'output-{n}')
        print(new_cmd)
        execute(f'tmux new-window -n {prefix}-slave-{n} "AFL_NO_UI=1 {new_cmd}; /bin/bash"')


def start(jit_compiler_code: str, seed: int, until_n_inputs: int):
    cmd = f'tmux new-session -s populate -d "~/die/olivine_batch_runner.py populate {jit_compiler_code} {seed} {until_n_inputs}"'
    execute(cmd)

    # Must wait for all slaves to finish
    while True:
        time.sleep(60)
        output = os.popen('tmux ls').read()
        print(output)

        if 'populate' not in output:
            break

    cmd = f'tmux new-session -s fuzz -d "python3 ~/die/olivine_batch_runner.py fuzz {jit_compiler_code} {seed} {until_n_inputs}"'
    execute(cmd)


def populate(fuzz_target_path: str, jit_compiler_code: str, seed: int, until_n_inputs: int):
    lib_string = get_lib_string(jit_compiler_code)
    cmd = f'{{ time ./fuzz/afl/afl-fuzz -s {seed} -e {until_n_inputs} -m none -o output -i ./corpus/output "{fuzz_target_path}" {lib_string} @@ }} 2> >(tee ~/die/output/time-populate.txt >&2)'
    run_slaves(cmd, 'populate')


def fuzz(fuzz_target_path: str, jit_compiler_code: str, seed: int, until_n_inputs: int):
    lib_string = get_lib_string(jit_compiler_code)
    cmd = f'{{ time ./fuzz/afl/afl-fuzz -s {seed} -e {until_n_inputs} -m none -o output "{fuzz_target_path}" {lib_string} @@ }} 2> >(tee ~/die/output/time-fuzz.txt >&2)'
    cmd += f' ; tmux rename-window analysis'
    cmd += f' ; {{ time python3 ~/die/olivine_slave_analysis.py }} 2> >(tee ~/die/output/time-analyze.txt >&2)'
    cmd += f' ; tmux rename-window done'
    cmd += f' ; /bin/bash'
    run_slaves(cmd, 'fuzz')


def main():
    cmd = sys.argv[1]
    print(cmd)

    if cmd == 'start':
        jit_compiler_code, seed, until_n_inputs = sys.argv[2:]

        seed = int(seed)
        until_n_inputs = int(until_n_inputs)

        start(jit_compiler_code, seed, until_n_inputs)

    elif cmd == 'populate':
        jit_compiler_code, seed, until_n_inputs = sys.argv[2:]

        seed = int(seed)
        until_n_inputs = int(until_n_inputs)
        fuzz_target_path = get_fuzz_target_path(jit_compiler_code)

        populate(fuzz_target_path, jit_compiler_code, seed, until_n_inputs)

    elif cmd == 'populate':
        jit_compiler_code, seed, until_n_inputs = sys.argv[2:]

        seed = int(seed)
        until_n_inputs = int(until_n_inputs)
        fuzz_target_path = get_fuzz_target_path(jit_compiler_code)

        fuzz(fuzz_target_path, jit_compiler_code, seed, until_n_inputs)

    else:
        assert False, f'Invalid arguments: {sys.argv}'


if __name__ == '__main__':
    main()
