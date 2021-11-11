import sys

# Usage:
# python3 olivine_batch_runner.py populate <jitpath> <diecorpuspath> <jitcode> <seed>
# python3 olivine_batch_runner.py run <jitpath> <jitcode> <seed>

# python3 olivine_slave_helper.py analyze <covtargetpath> <optsetflags> <timeout> <coveragesrcpath>

# Coverage commands
    [ "rm -rf ~/die/output-0/@coverage"
      "mkdir ~/die/output-0/@coverage"
      "cd ~/die/output-0/@coverage"
      "~/cov_runner.sh"
      $"cd {coverageBasePath}"
      $"/usr/bin/lcov --capture --no-checksum --directory {coverageBasePath} --output-file ~/die/output-0/@coverage/.lcovinfo --gcov-tool ~/gcov_for_clang.sh"
      "genhtml ~/die/output-0/@coverage/.lcovinfo --output-directory ~/die/output-0/@coverage/ --ignore-errors=source" ]


# Optset commands
    [ "rm -rf ~/die/output-0/@optset"
      "mkdir ~/die/output-0/@optset"
      "cd ~/die/output-0/@optset"
      "~/optset_runner.sh" ]
