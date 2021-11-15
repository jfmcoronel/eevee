import glob
import os
import sys
from typing import List

from olivine_helpers import (
    MetricsInfo,
    OLIVINE_BASEPATH,
    OLIVINE_SLAVE_OUTPUT_DIR_PREFIX,
    TIMEOUT,
    execute,
    get_metrics_info,
    wait_until_tmux_windows_closed,
)

# Usage:
# python3 olivine_slave_analysis.py optset <n> <jit_compiler_code>
# python3 olivine_slave_analysis.py coverage <n> <jit_compiler_code>

def generate_optsets(n: str, metrics_info: MetricsInfo):
    def generate_for(input_basepath: str, prefix: str):
        for full_js_path in sorted(glob.glob(input_basepath)):
            js_name_ext = os.path.basename(full_js_path)
            js_basename = os.path.splitext(js_name_ext)[0]
            optset_output_path = os.path.join(output_basepath, f'{prefix}{js_basename}.txt')

            dump_suffix = f'>{optset_output_path} 2>&1; echo -e "\\n$?" >> {optset_output_path}'
            actual_cmd = f'timeout {TIMEOUT} {metrics_info.fuzz_target_path} {metrics_info.optset_flags} {full_js_path} {dump_suffix}'

            execute(actual_cmd)

    output_basepath = f'{OLIVINE_BASEPATH}/{OLIVINE_SLAVE_OUTPUT_DIR_PREFIX}{n}/@optset'
    generated_inputs_basepath = f'/home/jfmcoronel/die/{OLIVINE_SLAVE_OUTPUT_DIR_PREFIX}{n}/@generated_inputs/*.js'
    selected_inputs_basepath = f'/home/jfmcoronel/die/{OLIVINE_SLAVE_OUTPUT_DIR_PREFIX}{n}/@selected_inputs/*.js'

    cmd: List[str] = [
        f'rm -rf {output_basepath}',
        f'mkdir {output_basepath}',
        f'cd {output_basepath}',
    ]
    execute(' ; '.join(cmd))

    generate_for(generated_inputs_basepath, 'generated_')
    generate_for(selected_inputs_basepath, 'selected_')


def generate_own_coverage(n: str, metrics_info: MetricsInfo):
    def generate_for(input_basepath: str):
        for full_js_path in sorted(glob.glob(input_basepath)):
            actual_cmd = f'timeout {TIMEOUT} {metrics_info.cov_target_path} {full_js_path}'
            execute(actual_cmd)

    n = str(n).zfill(2)

    generate_for(f'/home/jfmcoronel/die/{OLIVINE_SLAVE_OUTPUT_DIR_PREFIX}{n}/@generated_inputs/*.js')
    generate_for(f'/home/jfmcoronel/die/{OLIVINE_SLAVE_OUTPUT_DIR_PREFIX}{n}/@selected_inputs/*.js')



def generate_coverage_summary(metrics_info: MetricsInfo):
    output_basepath = f'{OLIVINE_BASEPATH}/{OLIVINE_SLAVE_OUTPUT_DIR_PREFIX}summary/'

    cmd_before: List[str] = [
        f'rm -rf {output_basepath}',
        f'mkdir {output_basepath}',
        f'cd {output_basepath}',
    ]
    execute(' ; '.join(cmd_before))

    lcovinfo_path = os.path.join(output_basepath, '.lcovinfo')

    cmd_after: List[str] = [
        f'cd {metrics_info.cov_source_code_path}',
        f'/usr/bin/lcov --capture --no-checksum --directory {metrics_info.cov_source_code_path} --output-file {lcovinfo_path} --gcov-tool {OLIVINE_BASEPATH}/gcov_for_clang.sh',
        f'genhtml {lcovinfo_path} --output-directory {output_basepath} --ignore-errors=source',
        f'{{ echo keys "*" | redis-cli ; }} > {output_basepath}/keys.txt',
    ]
    execute(' ; '.join(cmd_after))


def main():
    cmd, n, jit_compiler_code = sys.argv[1:]
    n = n.zfill(2)
    metrics_info = get_metrics_info(jit_compiler_code)

    if cmd == 'optset':
        execute(f'tmux rename-window -t fuzz-{n} optset-{n}')
        generate_optsets(n, metrics_info)
        execute(f'tmux rename-window -t optset-{n} done-{n}')

    elif cmd == 'coverage':
        execute(f'tmux rename-window -t done-{n} coverage-{n}')
        generate_own_coverage(n, metrics_info)

        if int(n) == 1:
            execute(f'tmux rename-window -t coverage-{n} summary-{n}')

            wait_until_tmux_windows_closed('fuzz', 20)
            wait_until_tmux_windows_closed('optset', 20)
            wait_until_tmux_windows_closed('coverage', 20)

            generate_coverage_summary(metrics_info)
            execute(f'tmux rename-window -t summary-{n} done-{n}')

        else:
            execute(f'tmux rename-window -t coverage-{n} done-{n}')

    else:
        assert False, f'Invalid arguments: {sys.argv}'


if __name__ == '__main__':
    main()
