from dataclasses import dataclass
import sys


# Usage:
# python3 olivine_slave_analysis.py <n> <jit_compiler_code>

TIMEOUT = 10


@dataclass(frozen=True, slots=True)
class MetricsInfo:
    cov_target_path: str
    opt_set_flags: str
    cov_source_code_path: str


v8_metrics_info = MetricsInfo(
    cov_target_path='/home/jfmcoronel/die/engines/v8/v8/out/Debug/d8',
    opt_set_flags='--trace-turbo-reduction',
    cov_source_code_path='/home/jfmcoronel/die/engines/v8/v8/out/Debug/',
)

ch_metrics_info = MetricsInfo(
    cov_target_path='/home/jfmcoronel/ch-cov-src/out/Debug/ch',
    opt_set_flags='-bgjit- -dump:backend',
    cov_source_code_path='/home/jfmcoronel/ch-cov-src/out/Debug/',
)

metrics_info_mapping: dict[str, MetricsInfo] = {
    'v8': v8_metrics_info,
    'ch': ch_metrics_info,
}


def get_metrics_info(jit_compiler_code: str) -> MetricsInfo:
    return metrics_info_mapping[jit_compiler_code]


# # Optset commands
#     [ "rm -rf ~/die/output-0/@optset"
#       "mkdir ~/die/output-0/@optset"
#       "cd ~/die/output-0/@optset"
#       "~/optset_runner.sh" ]

#     let optSetDumpBashFilename =
#         "/home/jfmcoronel/die/output-0/@optset/\`basename -s .js \$p\`.txt"

#     let optSetDumpCmd =
#         $">{optSetDumpBashFilename} 2>&1; echo \$? >> {optSetDumpBashFilename}"

#     let actualCmd =
#         $"timeout {timeoutSeconds} {pathToFuzzTarget} {optSetFlags} \$p {optSetDumpCmd}"

#     $"""cat << EOF > ~/optset_runner.sh
# #!/bin/bash
# for p in ~/die/output-0/all_inputs/*.js; do
#     echo "{actualCmd}" ;
#     {actualCmd} ;
# done
# EOF
# chmod +x ~/optset_runner.sh"""

def analyze():
    pass


def main():
    n, jit_compiler_code = sys.argv
    n = int(n)

    metrics_info = get_metrics_info(jit_compiler_code)


if __name__ == '__main__':
    main()


# # Coverage commands
#     [ "rm -rf ~/die/output-0/@coverage"
#       "mkdir ~/die/output-0/@coverage"
#       "cd ~/die/output-0/@coverage"
#       "~/cov_runner.sh"
#       $"cd {coverageBasePath}"
#       $"/usr/bin/lcov --capture --no-checksum --directory {coverageBasePath} --output-file ~/die/output-0/@coverage/.lcovinfo --gcov-tool ~/gcov_for_clang.sh"
#       "genhtml ~/die/output-0/@coverage/.lcovinfo --output-directory ~/die/output-0/@coverage/ --ignore-errors=source" ]

#     $"""cat << EOF > ~/cov_runner.sh
# #!/bin/bash
# for p in ~/die/output-0/all_inputs/*.js; do
#     echo {pathToCovTarget} \$p;
#     timeout {timeoutSeconds} {pathToCovTarget} \$p;
# done
# EOF
# chmod +x ~/cov_runner.sh"""
