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
    get_fuzz_target_string_with_flags,
    wait_until_tmux_session_closed,
)

# Usage:
# python3 olivine_batch_runner.py start {jitCompilerCode} {untilNInputs} {seed}
# python3 olivine_batch_runner.py process-corpus {jitCompilerCode} {untilNInputs} {seed}
# python3 olivine_batch_runner.py prune-corpus-with-slave {n} {jitCompilerCode}
# python3 olivine_batch_runner.py populate-with-slave {n} {jitCompilerCode} {untilNInputs} {seed}
# python3 olivine_batch_runner.py fuzz {jitCompilerCode} {untilNInputs} {seed}


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
    execute(f'tmux new-session -s corpus -d "python3 {OLIVINE_BASEPATH}/olivine_batch_runner.py process-corpus {jit_compiler_code} {until_n_inputs} {seed}"')

    # Must wait for all slaves to finish
    wait_until_tmux_session_closed('corpus', 10)

    execute(f'tmux new-session -s fuzz -d "python3 {OLIVINE_BASEPATH}/olivine_batch_runner.py fuzz {jit_compiler_code} {until_n_inputs} {seed}"')


def process_corpus(jit_compiler_code: str, until_n_inputs: int, seed: int, populate_only: bool):
    execute(f'echo FLUSHALL | redis-cli -p {REDIS_PORT}')

    if not populate_only:
        execute(f'cd {OLIVINE_BASEPATH} && rm -rf {OLIVINE_BASEPATH}/corpus/ && python3 ./fuzz/scripts/make_initial_corpus.py ./DIE-corpus ./corpus')

    execute('echo core | sudo tee /proc/sys/kernel/core_pattern')

    pre_cmds: List[str] = [
        f'cd {OLIVINE_BASEPATH} && rm -rf {OLIVINE_BASEPATH}/OLIVINE_SLAVE_OUTPUT_PATH',
        f'mkdir {OLIVINE_BASEPATH}/OLIVINE_SLAVE_OUTPUT_PATH',
    ]

    prune_cmds: List[str] = [
        f'tmux rename-window -t corpus-{{SLAVENUMBER}} prune-{{SLAVENUMBER}}',
        cmd_with_time_logging(
            # -u: Must be unbuffered for realtime stdout
            f'python3 -u {OLIVINE_BASEPATH}/olivine_batch_runner.py prune-corpus-with-slave {{SLAVENUMBER}} {jit_compiler_code}',
            f'{OLIVINE_BASEPATH}/OLIVINE_SLAVE_OUTPUT_PATH/log-prune.txt',
            should_log_all_output=True,
            must_have_double_braces=True,
        ),
    ] if not populate_only else []

    populate_cmds: List[str] = [
        f'tmux rename-window -t prune-{{SLAVENUMBER}} populate-{{SLAVENUMBER}}',
        f'python3 {OLIVINE_BASEPATH}/olivine_batch_runner.py populate-with-slave {{SLAVENUMBER}} {jit_compiler_code} {until_n_inputs} {seed}',
    ]

    cmds: List[str] = [*pre_cmds, *prune_cmds, *populate_cmds]

    run_windowed_slaves_in_current_session(cmds, 'corpus', False)


def prune_corpus_with_slave(n: str, jit_compiler_code: str):
    js_files = sorted(glob.glob(f'{OLIVINE_BASEPATH}/corpus/{OLIVINE_SLAVE_OUTPUT_DIR_PREFIX}{n}/*.js'))
    remaining = len(js_files)
    dump_suffix = f'2>&1; echo -e "\\n$?"'

    assert jit_compiler_code == 'v8', f'Pruning of corpus via {jit_compiler_code} is not yet supported'

    prune_dir = f'{OLIVINE_BASEPATH}/{OLIVINE_SLAVE_OUTPUT_DIR_PREFIX}{n}/@prune-log'
    os.makedirs(prune_dir)

    full_fuzz_target_str = get_fuzz_target_string_with_flags(jit_compiler_code)

    for full_js_path in js_files:
        actual_cmd = f'timeout {TIMEOUT} {full_fuzz_target_str} {full_js_path} {dump_suffix}'
        basename = os.path.basename(full_js_path)
        print(actual_cmd)

        result = os.popen(actual_cmd).read().strip()
        dump_filename = f'added.{basename}.txt'

        if ' by reducer ' not in result:
            print(f'Deleting {full_js_path} ({remaining} seeds left)')
            os.remove(full_js_path)
            remaining -= 1
            dump_filename = f'pruned.{basename}.txt'

        with open(os.path.join(prune_dir, dump_filename), 'w') as f:
            f.write(result)

    print('Remaining seeds:', remaining)


def populate_with_slave(n: str, jit_compiler_code: str, until_n_inputs: int, seed: int):
    full_fuzz_target_str = get_fuzz_target_string_with_flags(jit_compiler_code)

    populate_cmd = cmd_with_time_logging(
        f'''./fuzz/afl/afl-fuzz -C -s {seed} -e {until_n_inputs} -j {jit_compiler_code} -m none -o {OLIVINE_SLAVE_OUTPUT_DIR_PREFIX}{n} -i ./corpus/{OLIVINE_SLAVE_OUTPUT_DIR_PREFIX}{n} {full_fuzz_target_str} @@''',
        f'{OLIVINE_BASEPATH}/{OLIVINE_SLAVE_OUTPUT_DIR_PREFIX}{n}/log-populate.txt',
        should_log_all_output=True,
        must_have_double_braces=False,
    )

    execute(populate_cmd)


def fuzz(jit_compiler_code: str, until_n_inputs: int, seed: int):
    full_fuzz_target_str = get_fuzz_target_string_with_flags(jit_compiler_code)

    execute('echo core | sudo tee /proc/sys/kernel/core_pattern')

    fuzz_cmd = cmd_with_time_logging(
        f'''./fuzz/afl/afl-fuzz -s {seed} -e {until_n_inputs} -j {jit_compiler_code} -m none -o OLIVINE_SLAVE_OUTPUT_PATH {full_fuzz_target_str} @@''',
        f'{OLIVINE_BASEPATH}/OLIVINE_SLAVE_OUTPUT_PATH/log-fuzz.txt',
        should_log_all_output=False,
        must_have_double_braces=True,
    )

    single_pass_optset_coverage_cmd = cmd_with_time_logging(
        f'python3 {OLIVINE_BASEPATH}/olivine_slave_analysis.py analysis-singlepass {{SLAVENUMBER}} {jit_compiler_code}',
        f'{OLIVINE_BASEPATH}/OLIVINE_SLAVE_OUTPUT_PATH/log-analysis-singlepass.txt',
        should_log_all_output=True,
        must_have_double_braces=True,
        show_errors_on_screen=False,
    )

    cmds: List[str] = [
        f'cd {OLIVINE_BASEPATH}',
        fuzz_cmd,
        single_pass_optset_coverage_cmd,
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

        # TODO: Remove when orchestrator is updated
        execute('pip3 install hiredis')

        # Reexecute self
        execute(f"python3 {sys.argv[0]} true-start {' '.join(sys.argv[2:])}")

    elif cmd == 'true-start':
        jit_compiler_code, until_n_inputs, seed = sys.argv[2:]

        seed = int(seed)
        until_n_inputs = int(until_n_inputs)

        start(jit_compiler_code, until_n_inputs, seed)

    elif cmd == 'process-corpus':
        populate_only = False

        if len(sys.argv) == 5:
            jit_compiler_code, until_n_inputs, seed = sys.argv[2:]
        elif len(sys.argv) == 6:
            jit_compiler_code, until_n_inputs, seed, populate_only_arg = sys.argv[2:]

            if populate_only_arg == 'populate':
                populate_only = True
        else:
            assert False, f'Incorrect number of arguments: {sys.argv}'

        seed = int(seed)
        until_n_inputs = int(until_n_inputs)

        process_corpus(jit_compiler_code, until_n_inputs, seed, populate_only)

    elif cmd == 'prune-corpus-with-slave':
        n, jit_compiler_code = sys.argv[2:]

        prune_corpus_with_slave(n, jit_compiler_code)

    elif cmd == 'populate-with-slave':
        n, jit_compiler_code, until_n_inputs, seed = sys.argv[2:]

        seed = int(seed)
        until_n_inputs = int(until_n_inputs)

        populate_with_slave(n, jit_compiler_code, until_n_inputs, seed)

    elif cmd == 'fuzz':
        jit_compiler_code, until_n_inputs, seed = sys.argv[2:]

        until_n_inputs = int(until_n_inputs)
        seed = int(seed)

        fuzz(jit_compiler_code, until_n_inputs, seed)

    else:
        assert False, f'Invalid arguments: {sys.argv}'


if __name__ == '__main__':
    main()
