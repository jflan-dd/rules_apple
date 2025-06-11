#!/usr/bin/python3
# Copyright 2022 The Bazel Authors. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import json
import subprocess
from typing import List

def _simctl(extra_args: List[str]) -> str:
    return subprocess.check_output(["xcrun", "simctl"] + extra_args).decode()

def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "os_version", help="The iOS version to run the tests on, ex: 12.1"
    )
    return parser


def _main(os_version) -> None:
    runtimes = json.loads(_simctl(["list", "runtimes", "-j"]))["runtimes"]
    runtime_identifier = "com.apple.CoreSimulator.SimRuntime.iOS-{}".format(
        os_version.replace(".", "-")
    )

    runtime=None
    for r in runtimes:
        if r["identifier"] == runtime_identifier:
            runtime = r
            break

    if runtime:
        print(runtime["runtimeRoot"])


if __name__ == "__main__":
    args = _build_parser().parse_args()
    _main(args.os_version)
