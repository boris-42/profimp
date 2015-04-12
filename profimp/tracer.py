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

import sys
import time

if sys.version_info[0] == 3:
    import builtins
else:
    import __builtin__ as builtins


class TracePoint(object):

    def __init__(self, import_line, level=0, module=None, filepath=None):
        self.started_at = 0
        self.finished_at = 0
        self.import_line = import_line
        self.level = level
        self.module = module
        self.filepath = filepath
        self.children = []

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, etype, value, traceback):
        self.stop()

    def to_dict(self):

        result = {
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "duration": (self.finished_at - self.started_at) * 1000,
            "import_line": self.import_line,
            "level": self.level,
            "module": self.module,
            "filepath": self.filepath,
            "children": []
        }

        for child in self.children:
            result["children"].append(child.to_dict())

        return result

    def start(self):
        self.started_at = time.time()

    def stop(self):
        self.finished_at = time.time()

    def add_child(self, child):
        self.children.append(child)
        child.level = self.level + 1


TRACE_STACK = []


def init_stack():
    global TRACE_STACK
    TRACE_STACK = [TracePoint("root", 0)]
    return TRACE_STACK[0]


class patch_import(object):

    def __enter__(self):
        self.old_import = builtins.__import__
        builtins.__import__ = _traceit(builtins.__import__)

    def __exit__(self, exc_type, exc_value, exc_traceback):
        builtins.__import__ = self.old_import


def _traceit(f):
    def w(*args, **kwargs):
        import_line = ""

        module = "N/A"
        filepath = "N/A"
        if len(args) > 1 and hasattr(args[1], "get"):
            module = args[1].get("__name__")
            filepath = args[1].get("__file__")
        if len(args) > 3 and args[3]:
            import_line = "from %s import %s" % (args[0], ", ".join(args[3]))
        else:
            import_line = "import %s" % args[0]

        with TracePoint(import_line, module=module,
                        filepath=filepath) as trace_pt:
            TRACE_STACK[-1].add_child(trace_pt)
            TRACE_STACK.append(trace_pt)
            try:
                return f(*args, **kwargs)
            finally:
                TRACE_STACK.pop()
    return w
