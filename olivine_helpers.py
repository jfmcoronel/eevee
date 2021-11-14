import os
import time
from typing import Dict, NamedTuple

TIMEOUT = 10
REDIS_PORT = 6379


# Python 3.6 has no dataclasses
class MetricsInfo(NamedTuple):
    fuzz_target_path: str
    cov_target_path: str
    optset_flags: str
    cov_source_code_path: str


v8_metrics_info = MetricsInfo(
    fuzz_target_path='/home/jfmcoronel/v8-afl-dir/v8/out/Debug/d8',
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


def get_fuzz_target_path(jit_compiler_code: str):
    return metrics_info_mapping[jit_compiler_code].fuzz_target_path


def wait_until_tmux_windows_closed(window_name: str, interval: int = 60):
    while True:
        output = os.popen('tmux lsw').read()
        print(output)

        if window_name not in output:
            break

        time.sleep(interval)


def get_metrics_info(jit_compiler_code: str) -> MetricsInfo:
    return metrics_info_mapping[jit_compiler_code]


def execute(cmd: str):
    print(cmd)
    os.system(cmd)


def wait_until_tmux_session_closed(session_name: str, interval: int = 60):
    while True:
        output = os.popen('tmux ls').read()
        print(output)

        if session_name not in output:
            break

        time.sleep(interval)
