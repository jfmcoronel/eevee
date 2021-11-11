import sys

# Usage:
# python3 olivine_slave_analysis.py <n> <covtargetpath> <optsetflags> <timeout> <coveragesrcpath>

# let chakraCoreMetricsFetchInfo =
#     { PathToFuzzTarget = "/home/jfmcoronel/ch"
#       PathToCovTarget = "/home/jfmcoronel/ch-cov-src/out/Debug/ch"
#       TimeoutSeconds = 10
#       OptSetFlags = "-bgjit- -dump:backend"
#       CoverageSrcPath = "/home/jfmcoronel/ch-cov-src/out/Debug/"
#       JitCompilerCode = "ch" }


# let v8MetricsFetchInfo =
#     { PathToFuzzTarget = "/home/jfmcoronel/d8"
#       PathToCovTarget = "/home/jfmcoronel/die/engines/v8/v8/out/Debug/d8"
#       TimeoutSeconds = 10
#       OptSetFlags = "--trace-turbo-reduction"
#       CoverageSrcPath = "/home/jfmcoronel/die/engines/v8/v8/out/Debug/"
#       JitCompilerCode = "v8" }

#             [ $"{timedCmdBlock} > >(tee ~/die/output-0/time_metrics.txt) 2>&1"

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
