import glob
import os
import sys
import time
from typing import Dict, NamedTuple


# Usage:
# python3 olivine_slave_analysis.py optset <n> <jit_compiler_code>
# python3 olivine_slave_analysis.py coverage <n> <jit_compiler_code>

TIMEOUT = 10


# Python 3.6 has no dataclasses
class MetricsInfo(NamedTuple):
    fuzz_target_path: str
    cov_target_path: str
    optset_flags: str
    cov_source_code_path: str


v8_metrics_info = MetricsInfo(
    fuzz_target_path='/home/jfmcoronel/d8',
    cov_target_path='/home/jfmcoronel/die/engines/v8/v8/out/Debug/d8',
    optset_flags='--trace-turbo-reduction',
    cov_source_code_path='/home/jfmcoronel/die/engines/v8/v8/out/Debug/',
)

ch_metrics_info = MetricsInfo(
    fuzz_target_path='/home/jfmcoronel/ch',
    cov_target_path='/home/jfmcoronel/ch-cov-src/out/Debug/ch',
    optset_flags='-bgjit- -dump:backend',
    cov_source_code_path='/home/jfmcoronel/ch-cov-src/out/Debug/',
)

# Python 3.6 typing woes
metrics_info_mapping: Dict[str, MetricsInfo] = {
    'v8': v8_metrics_info,
    'ch': ch_metrics_info,
}


def wait_until_tmux_windows_closed(window_name: str, interval: int = 60):
    while True:
        time.sleep(interval)
        output = os.popen('tmux lsw').read()
        print(output)

        if window_name not in output:
            break


def get_metrics_info(jit_compiler_code: str) -> MetricsInfo:
    return metrics_info_mapping[jit_compiler_code]


def execute(cmd: str):
    print(cmd)
    os.system(cmd)


def generate_optsets(n: str, metrics_info: MetricsInfo):
    output_basepath = f'~/die/output-{n}/@optset'
    fuzz_input_basepath = f'/home/jfmcoronel/die/output-{n}/all_inputs/*.js'

    cmd: list[str] = [
        f'rm -rf {output_basepath}',
        f'mkdir {output_basepath}',
        f'cd {output_basepath}',
    ]
    execute(' ; '.join(cmd))

    for full_js_path in sorted(glob.glob(fuzz_input_basepath)):
        js_name_ext = os.path.basename(full_js_path)
        js_basename = os.path.splitext(js_name_ext)[0]
        optset_output_path = os.path.join(output_basepath, f'{js_basename}.txt')

        dump_suffix = f'>{optset_output_path} 2>&1; echo $? >> {optset_output_path}'
        actual_cmd = f'timeout {TIMEOUT} {metrics_info.fuzz_target_path} {metrics_info.optset_flags} {full_js_path} {dump_suffix}'

        execute(actual_cmd)


def generate_coverage(n: str, metrics_info: MetricsInfo):
    output_basepath = f'~/die/output-{n}/@coverage'
    fuzz_input_basepath = f'/home/jfmcoronel/die/output-{n}/all_inputs/*.js'

    cmd_before: list[str] = [
        f'rm -rf {output_basepath}',
        f'mkdir {output_basepath}',
        f'cd {output_basepath}',
    ]
    execute(' ; '.join(cmd_before))

    for full_js_path in sorted(glob.glob(fuzz_input_basepath)):
        actual_cmd = f'timeout {TIMEOUT} {metrics_info.fuzz_target_path} {full_js_path}'
        execute(actual_cmd)

    lcovinfo_path = os.path.join(output_basepath, '.lcovinfo')

    cmd_after: list[str] = [
        f'cd {metrics_info.cov_source_code_path}',
        f'/usr/bin/lcov --capture --no-checksum --directory {metrics_info.cov_source_code_path} --output-file {lcovinfo_path} --gcov-tool ~/gcov_for_clang.sh',
        f'genhtml {lcovinfo_path} --output-directory {output_basepath} --ignore-errors=source',
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
        if int(n) == 1:
            # Cannot be parallelized yet
            # Must wait for all slaves to finish
            execute(f'tmux rename-window -t done-{n} coverage-{n}')
            wait_until_tmux_windows_closed('optset', 60)

            generate_coverage(n, metrics_info)

        execute(f'tmux rename-window -t coverage-{n} done-{n}')
    else:
        assert False, f'Invalid arguments: {sys.argv}'


if __name__ == '__main__':
    main()
