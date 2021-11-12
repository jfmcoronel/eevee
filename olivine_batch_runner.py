import multiprocessing
import os
import sys
import time

# Usage:
# python3 olivine_batch_runner.py start {jitCompilerCode} {seed} {untilNInputs}
# python3 olivine_batch_runner.py populate {jitCompilerCode} {seed} {untilNInputs}
# python3 olivine_batch_runner.py populate-with-slave {n} {jitCompilerCode} {seed} {untilNInputs}
# python3 olivine_batch_runner.py fuzz {jitCompilerCode} {seed} {untilNInputs}

def execute(cmd: str):
    print(cmd)
    os.system(cmd)

def get_lib_string(jit_compiler_code: str):
    die_corpus_path = '/home/jfmcoronel/die/DIE-corpus/'

    if jit_compiler_code == 'ch':
        return f'-lib={die_corpus_path}/lib.js -lib={die_corpus_path}/jsc.js -lib={die_corpus_path}/v8.js -lib={die_corpus_path}/ffx.js -lib={die_corpus_path}/chakra.js'

    return f'{die_corpus_path}/lib.js {die_corpus_path}/jsc.js {die_corpus_path}/v8.js {die_corpus_path}/ffx.js {die_corpus_path}/chakra.js'


def wait_until_tmux_session_closed(session_name: str, interval: int = 60):
    while True:
        time.sleep(interval)
        output = os.popen('tmux ls').read()
        print(output)

        if session_name not in output:
            break


def get_fuzz_target_path(jit_compiler_code: str):
    if jit_compiler_code == 'jsc':
        return '/home/jfmcoronel/jsc'
    elif jit_compiler_code == 'v8':
        return '/home/jfmcoronel/d8'
    elif jit_compiler_code == 'ch':
        return '/home/jfmcoronel/ch'
    else:
        assert False, f'Invalid JIT compiler code: {jit_compiler_code}'


def run_windowed_slaves(cmd: str, session_name: str, prefix: str, persist: bool):
    slave_count = multiprocessing.cpu_count()

    # Start from 01
    for n in range(1, slave_count + 1):
        n = str(n).zfill(2)

        new_cmd = cmd.replace('output', f'output-{n}') \
                     .format(SLAVENUMBER=n)
        print(new_cmd)

        if persist:
            execute(f'tmux new-window -t {session_name} -n {prefix}-{n} "{new_cmd}; /bin/bash"')
        else:
            execute(f'tmux new-window -t {session_name} -n {prefix}-{n} "{new_cmd}"')


def start(jit_compiler_code: str, until_n_inputs: int, seed: int):
    # Enables running each phase in a new tmux session
    execute(f'tmux new-session -s populate -d "python3 ~/die/olivine_batch_runner.py populate {jit_compiler_code} {seed} {until_n_inputs}"')

    # Must wait for all slaves to finish
    wait_until_tmux_session_closed('populate', 60)

    execute(f'tmux new-session -s fuzz -d "python3 ~/die/olivine_batch_runner.py fuzz {jit_compiler_code} {seed} {until_n_inputs}"')


def populate(jit_compiler_code: str, until_n_inputs: int, seed: int):
    execute(f'cd ~/die && rm -rf ~/die/corpus/ && python3 ./fuzz/scripts/make_initial_corpus.py ./DIE-corpus ./corpus')
    execute('echo core | sudo tee /proc/sys/kernel/core_pattern')

    cmd: list[str] = [
        f'cd ~/die && rm -rf ~/die/output',
        f'mkdir ~/die/output',
        f'python3 ~/die/olivine_batch_runner.py populate-with-slave {{SLAVENUMBER}} {jit_compiler_code} {seed} {until_n_inputs}',
    ]

    run_windowed_slaves(' ; '.join(cmd), 'populate', 'populate', False)


def populate_with_slave(n: str, fuzz_target_path: str, jit_compiler_code: str, until_n_inputs: int, seed: int):
    lib_string = get_lib_string(jit_compiler_code)

    execute(f'{{ time ./fuzz/afl/afl-fuzz -s {seed} -e {until_n_inputs} -m none -o output-{n} -i ./corpus/output-{n} "{fuzz_target_path}" {lib_string} @@ ; }} 2> >(tee ~/die/output/time-populate.txt >&2)')


def fuzz(jit_compiler_code: str, until_n_inputs: int, seed: int):
    lib_string = get_lib_string(jit_compiler_code)
    fuzz_target_path = get_fuzz_target_path(jit_compiler_code)

    execute('echo core | sudo tee /proc/sys/kernel/core_pattern')

    cmd: list[str] = [
        'cd ~/die',
        f'{{{{ time ./fuzz/afl/afl-fuzz -s {seed} -e {until_n_inputs} -j {jit_compiler_code} -m none -o output "{fuzz_target_path}" {lib_string} @@ ; }}}} 2> >(tee ~/die/output/time-fuzz.txt >&2)',
        f'{{{{ time python3 ~/die/olivine_slave_analysis.py optset {{SLAVENUMBER}} {jit_compiler_code} ; }}}} 2> >(tee ~/die/output/time-analyze-optset.txt >&2)',
        f'{{{{ time python3 ~/die/olivine_slave_analysis.py coverage {{SLAVENUMBER}} {jit_compiler_code} ; }}}} 2> >(tee ~/die/output/time-analyze-coverage.txt >&2)',
    ]

    run_windowed_slaves(' ; '.join(cmd), 'fuzz', 'fuzz', True)


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

        populate(jit_compiler_code, until_n_inputs, seed)

    elif cmd == 'populate-with-slave':
        n, jit_compiler_code, until_n_inputs, seed = sys.argv[2:]

        seed = int(seed)
        until_n_inputs = int(until_n_inputs)
        fuzz_target_path = get_fuzz_target_path(jit_compiler_code)

        populate_with_slave(n, fuzz_target_path, jit_compiler_code, until_n_inputs, seed)

    elif cmd == 'fuzz':
        jit_compiler_code, until_n_inputs, seed = sys.argv[2:]

        until_n_inputs = int(until_n_inputs)
        seed = int(seed)

        fuzz(jit_compiler_code, until_n_inputs, seed)

    else:
        assert False, f'Invalid arguments: {sys.argv}'


if __name__ == '__main__':
    main()
