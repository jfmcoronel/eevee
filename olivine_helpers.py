import os
import time
from typing import Dict, NamedTuple

TIMEOUT = 10
REDIS_PORT = 6379
OLIVINE_HOME = os.path.expanduser('~')
OLIVINE_BASEPATH = os.path.expanduser('~/die/')
OLIVINE_SLAVE_OUTPUT_DIR_PREFIX = 'output-'
OLIVINE_SUMMARY_BASEPATH = f'{OLIVINE_BASEPATH}/{OLIVINE_SLAVE_OUTPUT_DIR_PREFIX}summary/'

# Python 3.6 has no dataclasses
class PathInfo(NamedTuple):
    fuzz_target_path: str
    cov_target_path: str
    optset_flags: str
    cov_source_code_path: str


v8_path_info = PathInfo(
    fuzz_target_path=f'{OLIVINE_HOME}/v8-afl-dir/v8/out/Debug/d8',
    cov_target_path=f'{OLIVINE_HOME}/die/engines/v8/v8/out/Debug/d8',
    optset_flags='--trace-turbo-reduction',
    cov_source_code_path=f'{OLIVINE_HOME}/die/engines/v8/v8/out/Debug/',
)

ch_path_info = PathInfo(
    fuzz_target_path=f'{OLIVINE_HOME}/ch',
    cov_target_path=f'{OLIVINE_HOME}/ch-cov-src/out/Debug/ch',
    optset_flags='-bgjit- -dump:backend',
    cov_source_code_path=f'{OLIVINE_HOME}/ch-cov-src/out/Debug/',
)

jsc_path_info = PathInfo(
    fuzz_target_path=f'{OLIVINE_HOME}/jsc',
    cov_target_path=f'{OLIVINE_HOME}/jsc-cov',
    optset_flags='--useConcurrentJIT=false --verboseCompilation=true',
    cov_source_code_path=f'{OLIVINE_HOME}/webkit/WebKitBuild/Debug/',
)

# Python 3.6 typing woes
path_info_mapping: Dict[str, PathInfo] = {
    'v8': v8_path_info,
    'ch': ch_path_info,
    'jsc': jsc_path_info,
}


def get_fuzz_target_path(jit_compiler_code: str):
    return path_info_mapping[jit_compiler_code].fuzz_target_path


def get_fuzz_target_flags(jit_compiler_code: str):
    return path_info_mapping[jit_compiler_code].optset_flags


def get_fuzz_target_string_with_flags(jit_compiler_code: str):
    fuzz_target_path = get_fuzz_target_path(jit_compiler_code)
    fuzz_target_flags = get_fuzz_target_flags(jit_compiler_code)
    libs = get_lib_string(jit_compiler_code)

    return f'{fuzz_target_path} {fuzz_target_flags} {libs}'


def get_lib_string(jit_compiler_code: str):
    die_corpus_path = f'{OLIVINE_BASEPATH}/DIE-corpus/'

    if jit_compiler_code == 'ch':
        return f'-lib={die_corpus_path}/lib.js -lib={die_corpus_path}/jsc.js -lib={die_corpus_path}/v8.js -lib={die_corpus_path}/ffx.js -lib={die_corpus_path}/chakra.js'

    return f'{die_corpus_path}/lib.js {die_corpus_path}/jsc.js {die_corpus_path}/v8.js {die_corpus_path}/ffx.js {die_corpus_path}/chakra.js'


def cmd_with_time_logging(cmd: str, log_path: str, should_log_all_output: bool, must_have_double_braces: bool, show_errors_on_screen: bool = True):
    log_all_output = '>&2' if should_log_all_output else ''
    suppressor = '' if show_errors_on_screen else '>/dev/null'

    braced_cmd = f'{{{{ time {{{{ {cmd} ; }}}} ; }}}}' if must_have_double_braces \
                 else f'{{ time {{ {cmd} ; }} ; }}'

    ret = f'''bash -c "{braced_cmd} 2> >(tee {log_path} {suppressor}) {log_all_output}"'''

    print('@@@ Generated:', ret)

    return ret


def wait_until_tmux_windows_closed(window_name: str, interval: int = 60):
    while True:
        output = os.popen('tmux lsw').read()
        print(output)

        if window_name not in output:
            break

        time.sleep(interval)


def get_path_info(jit_compiler_code: str) -> PathInfo:
    return path_info_mapping[jit_compiler_code]


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
