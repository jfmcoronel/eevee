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


def run_slaves(cmd: str, prefix: str, persist: bool):
    slave_count = multiprocessing.cpu_count()

    # Start from 01
    for n in range(1, slave_count + 1):
        n = str(n).zfill(2)

        new_cmd = cmd.replace('output', f'output-{n}') \
                     .format(SLAVENUMBER=n)
        print(new_cmd)

        if persist:
            execute(f'tmux new-window -n {prefix}-{n} "{new_cmd}; /bin/bash"')
        else:
            execute(f'tmux new-window -n {prefix}-{n} "{new_cmd}"')


def start(jit_compiler_code: str, until_n_inputs: int, seed: int):
    cmd = f'tmux new-session -s populate -d "python3 ~/die/olivine_batch_runner.py populate {jit_compiler_code} {seed} {until_n_inputs}"'
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


def populate(fuzz_target_path: str, jit_compiler_code: str, until_n_inputs: int, seed: int):
    lib_string = get_lib_string(jit_compiler_code)

    execute(f'cd ~/die && rm -rf ~/die/corpus/ && python3 ./fuzz/scripts/make_initial_corpus.py ./DIE-corpus ./corpus')

    cmd: list[str] = [
        'sudo bash -c "echo core >/proc/sys/kernel/core_pattern"',
        f'cd ~/die && rm -rf ~/die/output',
        f'{{ time ./fuzz/afl/afl-fuzz -s {seed} -e {until_n_inputs} -m none -o output -i ./corpus/output "{fuzz_target_path}" {lib_string} @@ ; }} 2> >(tee ~/die/output/time-populate.txt >&2)',
    ]

    run_slaves(' ; '.join(cmd), 'populate', False)


def fuzz(jit_compiler_code: str, until_n_inputs: int, seed: int):
    lib_string = get_lib_string(jit_compiler_code)
    fuzz_target_path = get_fuzz_target_path(jit_compiler_code)

    cmd: list[str] = [
        'sudo bash -c "echo core >/proc/sys/kernel/core_pattern"',
        'cd ~/die',
        f'{{{{ time ./fuzz/afl/afl-fuzz -s {seed} -e {until_n_inputs} -j {jit_compiler_code} -m none -o output "{fuzz_target_path}" {lib_string} @@ ; }}}} 2> >(tee ~/die/output/time-fuzz.txt >&2)',
        f'{{{{ time python3 ~/die/olivine_slave_analysis.py optset {{SLAVENUMBER}} {jit_compiler_code} ; }}}} 2> >(tee ~/die/output/time-analyze-optset.txt >&2)',
        f'{{{{ time python3 ~/die/olivine_slave_analysis.py coverage {{SLAVENUMBER}} {jit_compiler_code} ; }}}} 2> >(tee ~/die/output/time-analyze-coverage.txt >&2)',
    ]

    run_slaves(' ; '.join(cmd), 'fuzz', True)


def main():
    cmd = sys.argv[1]
    print(cmd)

    if cmd == 'start':
        jit_compiler_code, until_n_inputs, seed = sys.argv[2:]

        seed = int(seed)
        until_n_inputs = int(until_n_inputs)

        start(jit_compiler_code, until_n_inputs, seed)

    elif cmd == 'populate':
        jit_compiler_code, until_n_inputs, seed = sys.argv[2:]

        seed = int(seed)
        until_n_inputs = int(until_n_inputs)
        fuzz_target_path = get_fuzz_target_path(jit_compiler_code)

        populate(fuzz_target_path, jit_compiler_code, until_n_inputs, seed)

    elif cmd == 'fuzz':
        jit_compiler_code, until_n_inputs, seed = sys.argv[2:]

        until_n_inputs = int(until_n_inputs)
        seed = int(seed)

        fuzz(jit_compiler_code, until_n_inputs, seed)

    else:
        assert False, f'Invalid arguments: {sys.argv}'


if __name__ == '__main__':
    main()
