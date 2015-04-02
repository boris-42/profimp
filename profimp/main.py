# Copyright 2015: Boris Pavlovic
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from __future__ import print_function

import sys

from profimp import reports
from profimp import tracer


HELP_MESSAGE = """
    Profimp allows you to trace imports of your code.

    This lib should be used to simplify optimization of imports in your code.
    At least you will find what consumes the most part of time and do the
    right decisions.

    Syntax:
        profimp [import_module_line] [--html]

    Samples:
        profimp "import collections"

        profimp "from somemoudle import something"

        prpfimp --html "import multiprocessing"

"""


def print_help():
    print(HELP_MESSAGE)


def trace_module(import_line):
    root_pt = tracer.init_stack()
    with tracer.patch_import():
        with root_pt:
            exec(import_line)
    return root_pt


def main():
    if len(sys.argv) == 1:
        print_help()
    elif len(sys.argv) == 2:
        report = reports.to_json(trace_module(sys.argv[1]))
        sys.stdout.write(report)
    elif len(sys.argv) == 3:
        if "--html" in sys.argv[1:]:
            arg_pos = 1 if sys.argv[1] != "--html" else 2
            report = reports.to_html(trace_module(sys.argv[arg_pos]))
            sys.stdout.write(report)
        else:
            print_help()
            raise SystemExit("Wrong input arguments: %s" % sys.argv)
    else:
        print_help()
        raise SystemExit("Wrong input arguments: %s" % sys.argv)


if __name__ == "__main__":
    main()
