# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
from glob import glob
import logging
import os
import sys

import yaml


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stderr)
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)


def yaml_to_all_tests(glob_paths: list, out_file: str):
    logger.debug(f"Received paths: {glob_paths}")
    yamls = []
    for path in glob_paths:
        yamls.extend(glob(pathname=path, recursive=True))
    # yamls = glob(pathname=glob_path, recursive=True)
    logger.debug(f"Found {len(yamls)} YAML files")
    class_count = 0
    method_count = 0
    with open(out_file, "w") as fp:
        for yaml_file in yamls:
            with open(yaml_file, "r") as yamp_fp:
                tests = yaml.safe_load(yamp_fp)
                for clazz, methods in tests.items():
                    class_count += 1
                    for method in methods:
                        method_count += 1
                        fp.write(f"{clazz}#{method}\n")

    logger.debug(f"Wrote {method_count} test methods from {class_count} classes to {out_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert the test catalog to a single text file")

    parser.add_argument("--path",
                        required=False,
                        action='append',
                        default=None,
                        help="Path to module YAML files. Glob patterns are supported.")
    parser.add_argument("--output-file",
                        required=False,
                        default="combined-test-catalog.txt",
                        help="Output file location")

    if not os.getenv("GITHUB_WORKSPACE"):
        print("This script is intended to by run by GitHub Actions.")
        exit(1)

    args = parser.parse_args()
    if args.path is None:
        args.path = ["test-catalog/**/*.yaml"]
    glob_paths = args.paths if args.paths else ["test-catalog/**/*.yaml"]
    logger.debug(f"Passed paths: {args.path}")
    yaml_to_all_tests(args.path, args.output_file)
