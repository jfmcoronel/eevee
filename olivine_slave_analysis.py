import glob
import os
import sys
from typing import List

from olivine_helpers import (
    OLIVINE_BASEPATH,
    OLIVINE_SLAVE_OUTPUT_DIR_PREFIX,
    OLIVINE_SUMMARY_BASEPATH,
    PathInfo,
    TIMEOUT,
    execute,
    get_fuzz_target_string_with_flags,
    get_path_info,
    wait_until_tmux_windows_closed,
)

# Usage:
# python3 olivine_slave_analysis.py analysis-singlepass <n> <jit_compiler_code>

def do_own_analysis_singlepass(n: str, jit_compiler_code: str):
    full_fuzz_target_str = get_fuzz_target_string_with_flags(jit_compiler_code)

    def generate_for(input_basepath: str, prefix: str):
        for full_js_path in sorted(glob.glob(input_basepath)):
            js_name_ext = os.path.basename(full_js_path)
            js_basename = os.path.splitext(js_name_ext)[0]
            optset_output_path = os.path.join(output_basepath, f'{prefix}{js_basename}.txt')

            dump_suffix = f'>{optset_output_path} 2>&1; echo -e "\\n$?" >> {optset_output_path}'
            actual_cmd = f'timeout {TIMEOUT} {full_fuzz_target_str} {full_js_path} {dump_suffix}'

            execute(actual_cmd)

    slave_output_dir = f'{OLIVINE_BASEPATH}/{OLIVINE_SLAVE_OUTPUT_DIR_PREFIX}{n}'
    output_basepath = f'{slave_output_dir}/@jit_feedback'
    generated_inputs_basepath = f'{slave_output_dir}/@generated_inputs/*.js'
    selected_inputs_basepath = f'{slave_output_dir}/@selected_inputs/*.js'

    cmd: List[str] = [
        f'rm -rf {output_basepath}',
        f'mkdir {output_basepath}',
        f'cd {output_basepath}',
    ]
    execute(' ; '.join(cmd))

    generate_for(generated_inputs_basepath, 'generated_')
    generate_for(selected_inputs_basepath, 'selected_')


def generate_coverage_summary(path_info: PathInfo):
    output_basepath = OLIVINE_SUMMARY_BASEPATH

    cmd_before: List[str] = [
        f'rm -rf {output_basepath}',
        f'mkdir {output_basepath}',
        f'cd {output_basepath}',
    ]
    execute(' ; '.join(cmd_before))

    lcovinfo_path = os.path.join(output_basepath, '.lcovinfo')

    cmd_after: List[str] = [
        f'cd {path_info.cov_source_code_path}',
        f'/usr/bin/lcov --capture --no-checksum --directory {path_info.cov_source_code_path} --output-file {lcovinfo_path} --gcov-tool {OLIVINE_BASEPATH}/gcov_for_clang.sh',
        f'genhtml {lcovinfo_path} --output-directory {output_basepath} --ignore-errors=source',
        f'{{ echo keys "*" | redis-cli ; }} > {output_basepath}/keys.txt',
    ]
    execute(' ; '.join(cmd_after))


def main():
    cmd, n, jit_compiler_code = sys.argv[1:]
    n = n.zfill(2)

    if cmd == 'analysis-singlepass':
        execute(f'tmux rename-window -t done-{n} analysis-{n}')
        do_own_analysis_singlepass(n, jit_compiler_code)

        if int(n) == 1:
            execute(f'tmux rename-window -t analysis-{n} summary-{n}')

            wait_until_tmux_windows_closed('fuzz', 10)
            wait_until_tmux_windows_closed('analysis', 10)

            path_info = get_path_info(jit_compiler_code)

            generate_coverage_summary(path_info)
            execute(f'tmux rename-window -t summary-{n} done-{n}')
            execute('uptime | tee {OLIVINE_SUMMARY_BASEPATH}/time-uptime.txt')

        else:
            execute(f'tmux rename-window -t analysis-{n} done-{n}')

    else:
        assert False, f'Invalid arguments: {sys.argv}'


if __name__ == '__main__':
    main()
