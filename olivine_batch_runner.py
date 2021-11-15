import glob
import multiprocessing
import os
import sys
from typing import List

from olivine_helpers import (
    OLIVINE_BASEPATH,
    OLIVINE_SLAVE_OUTPUT_DIR_PREFIX,
    REDIS_PORT,
    TIMEOUT,
    cmd_with_time_logging,
    execute,
    get_fuzz_target_flags,
    get_fuzz_target_path,
    v8_metrics_info,
    wait_until_tmux_session_closed,
)

# Usage:
# python3 olivine_batch_runner.py start {jitCompilerCode} {untilNInputs} {seed}
# python3 olivine_batch_runner.py populate {jitCompilerCode} {untilNInputs} {seed}
# python3 olivine_batch_runner.py prune-v8-corpus {jitCompilerCode} {untilNInputs} {seed}
# python3 olivine_batch_runner.py populate-with-slave {n} {jitCompilerCode} {untilNInputs} {seed}
# python3 olivine_batch_runner.py fuzz {jitCompilerCode} {untilNInputs} {seed}


def get_lib_string(jit_compiler_code: str):
    die_corpus_path = '/home/jfmcoronel/die/DIE-corpus/'

    if jit_compiler_code == 'ch':
        return f'-lib={die_corpus_path}/lib.js -lib={die_corpus_path}/jsc.js -lib={die_corpus_path}/v8.js -lib={die_corpus_path}/ffx.js -lib={die_corpus_path}/chakra.js'

    return f'{die_corpus_path}/lib.js {die_corpus_path}/jsc.js {die_corpus_path}/v8.js {die_corpus_path}/ffx.js {die_corpus_path}/chakra.js'


def run_windowed_slaves_in_current_session(cmds: List[str], prefix: str, persist: bool):
    slave_count = multiprocessing.cpu_count()
    cmd = ' ; '.join(cmd for cmd in cmds if cmd)

    # Start from 01
    for n in range(1, slave_count + 1):
        n = str(n).zfill(2)

        new_cmd = cmd.replace('OLIVINE_SLAVE_OUTPUT_PATH', f'{OLIVINE_SLAVE_OUTPUT_DIR_PREFIX}{n}') \
                     .format(SLAVENUMBER=n)

        if persist:
            execute(f"tmux new-window -n {prefix}-{n} '{new_cmd}; /bin/bash'")
        else:
            execute(f"tmux new-window -n {prefix}-{n} '{new_cmd}'")


def start(jit_compiler_code: str, until_n_inputs: int, seed: int):
    # Enables running each phase in a new tmux session
    execute(f'tmux new-session -s populate -d "python3 {OLIVINE_BASEPATH}/olivine_batch_runner.py populate {jit_compiler_code} {until_n_inputs} {seed}"')

    # Must wait for all slaves to finish
    wait_until_tmux_session_closed('populate', 60)

    execute(f'tmux new-session -s fuzz -d "python3 {OLIVINE_BASEPATH}/olivine_batch_runner.py fuzz {jit_compiler_code} {until_n_inputs} {seed}"')


def populate(jit_compiler_code: str, until_n_inputs: int, seed: int):
    execute(f'echo FLUSHALL | redis-cli -p {REDIS_PORT}')
    execute(f'cd {OLIVINE_BASEPATH} && rm -rf {OLIVINE_BASEPATH}/corpus/ && python3 ./fuzz/scripts/make_initial_corpus.py ./DIE-corpus ./corpus')
    execute('echo core | sudo tee /proc/sys/kernel/core_pattern')

    pre_cmds: List[str] = [
        f'cd {OLIVINE_BASEPATH} && rm -rf {OLIVINE_BASEPATH}/OLIVINE_SLAVE_OUTPUT_PATH',
        f'mkdir {OLIVINE_BASEPATH}/OLIVINE_SLAVE_OUTPUT_PATH',
    ]

    prune_cmds: List[str] = [
        f'tmux rename-window -t populate-{{SLAVENUMBER}} prune-{{SLAVENUMBER}}',
        cmd_with_time_logging(
            # -u: Must be unbuffered for realtime stdout
            f'python3 -u {OLIVINE_BASEPATH}/olivine_batch_runner.py prune-v8-corpus {{SLAVENUMBER}} {jit_compiler_code} {until_n_inputs} {seed}',
            f'{OLIVINE_BASEPATH}/OLIVINE_SLAVE_OUTPUT_PATH/log-prune.txt',
            should_log_all_output=True,
            must_have_double_braces=True,
        ),
    ]

    populate_cmds: List[str] = [
        f'tmux rename-window -t prune-{{SLAVENUMBER}} populate-{{SLAVENUMBER}}',
        f'python3 {OLIVINE_BASEPATH}/olivine_batch_runner.py populate-with-slave {{SLAVENUMBER}} {jit_compiler_code} {until_n_inputs} {seed}',
    ]

    cmds: List[str] = [*pre_cmds, *prune_cmds, *populate_cmds] if jit_compiler_code == 'v8' \
                      else [*pre_cmds, *populate_cmds]

    run_windowed_slaves_in_current_session(cmds, 'populate', False)


def prune_v8_corpus_with_slave(n: str):
    js_files = sorted(glob.glob(f'/home/jfmcoronel/die/corpus/{OLIVINE_SLAVE_OUTPUT_DIR_PREFIX}{n}/*.js'))
    remaining = len(js_files)
    dump_suffix = f'2>&1; echo -e "\\n$?"'

    for full_js_path in js_files:
        actual_cmd = f'timeout {TIMEOUT} {v8_metrics_info.fuzz_target_path} {v8_metrics_info.optset_flags} {full_js_path} {dump_suffix}'
        print(actual_cmd)

        result = os.popen(actual_cmd).read().strip()
        lines = result.rsplit('\n', maxsplit=1)
        status_code = int(lines[-1])

        if status_code != 0 or ' by reducer ' not in result:
            print(f'Deleting {full_js_path} ({remaining} seeds left)')
            os.remove(full_js_path)
            remaining -= 1

    print('Remaining seeds:', remaining)


def populate_with_slave(n: str, fuzz_target_path: str, jit_compiler_code: str, until_n_inputs: int, seed: int):
    populate_cmd = cmd_with_time_logging(
        f'''./fuzz/afl/afl-fuzz -C -s {seed} -e {until_n_inputs} -j {jit_compiler_code} -m none -o {OLIVINE_SLAVE_OUTPUT_DIR_PREFIX}{n} -i ./corpus/{OLIVINE_SLAVE_OUTPUT_DIR_PREFIX}{n} '{fuzz_target_path}' @@''',
        f'{OLIVINE_BASEPATH}/{OLIVINE_SLAVE_OUTPUT_DIR_PREFIX}{n}/log-populate.txt',
        should_log_all_output=True,
        must_have_double_braces=False,
    )

    execute(populate_cmd)


def fuzz(jit_compiler_code: str, until_n_inputs: int, seed: int):
    fuzz_target_path = get_fuzz_target_path(jit_compiler_code)
    fuzz_target_flags = get_fuzz_target_flags(jit_compiler_code)

    execute('echo core | sudo tee /proc/sys/kernel/core_pattern')

    fuzz_cmd = cmd_with_time_logging(
        f'''./fuzz/afl/afl-fuzz -s {seed} -e {until_n_inputs} -j {jit_compiler_code} -m none -o OLIVINE_SLAVE_OUTPUT_PATH '{fuzz_target_path}' {fuzz_target_flags} @@''',
        f'{OLIVINE_BASEPATH}/OLIVINE_SLAVE_OUTPUT_PATH/log-fuzz.txt',
        should_log_all_output=False,
        must_have_double_braces=True,
    )

    optset_cmd = cmd_with_time_logging(
        f'python3 {OLIVINE_BASEPATH}/olivine_slave_analysis.py optset {{SLAVENUMBER}} {jit_compiler_code}',
        f'{OLIVINE_BASEPATH}/OLIVINE_SLAVE_OUTPUT_PATH/log-analyze-optset.txt',
        should_log_all_output=True,
        must_have_double_braces=True,
        show_errors_on_screen=False,
    )

    coverage_cmd = cmd_with_time_logging(
        f'python3 {OLIVINE_BASEPATH}/olivine_slave_analysis.py coverage {{SLAVENUMBER}} {jit_compiler_code}',
        f'{OLIVINE_BASEPATH}/OLIVINE_SLAVE_OUTPUT_PATH/log-analyze-coverage.txt',
        should_log_all_output=True,
        must_have_double_braces=True,
        show_errors_on_screen=False,
    )

    cmds: List[str] = [
        f'cd {OLIVINE_BASEPATH}',
        fuzz_cmd,
        optset_cmd,
        coverage_cmd,
    ]

    run_windowed_slaves_in_current_session(cmds, 'fuzz', True)


def main():
    cmd = sys.argv[1]
    print(cmd)

    if cmd == 'start':
        # Update self first
        updater_cmd = cmd_with_time_logging(
            f'cd {OLIVINE_BASEPATH} && git pull && ./compile.sh',
            f'~/log-start.txt',
            should_log_all_output=True,
            must_have_double_braces=False,
        )
        execute(updater_cmd)

        afl_path = os.path.join(OLIVINE_BASEPATH, 'fuzz', 'afl', 'afl-fuzz')

        if not os.path.exists(afl_path):
            with open(os.path.expanduser('~/log-start.txt'), 'r') as f:
                print(f.read())

            print(afl_path)
            print('\nAFL executable does not exist')
            exit(-1)

        # Reexecute self
        execute(f"python3 {sys.argv[0]} true-start {' '.join(sys.argv[2:])}")

    elif cmd == 'true-start':
        jit_compiler_code, until_n_inputs, seed = sys.argv[2:]

        seed = int(seed)
        until_n_inputs = int(until_n_inputs)

        start(jit_compiler_code, until_n_inputs, seed)

    elif cmd == 'populate':
        jit_compiler_code, until_n_inputs, seed = sys.argv[2:]

        seed = int(seed)
        until_n_inputs = int(until_n_inputs)

        populate(jit_compiler_code, until_n_inputs, seed)

    elif cmd == 'prune-v8-corpus':
        n = sys.argv[2]

        prune_v8_corpus_with_slave(n)

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
