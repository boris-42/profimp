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

import contextlib
import time

from six.moves import builtins


class TracePoint(object):

    def __init__(self, import_line, level=0):
        self.started_at = 0
        self.finished_at = 0
        self.import_line = import_line
        self.level = level
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


@contextlib.contextmanager
def patch_import():
    old_import = builtins.__import__
    builtins.__import__ = _traceit(builtins.__import__)
    yield
    builtins.__import__ = old_import


def _traceit(f):
    def w(*args, **kwargs):
        import_line = ""

        if len(args) > 3 and args[3]:
            import_line = "from %s import %s" % (args[0], ", ".join(args[3]))
        else:
            import_line = "import %s" % args[0]

        with TracePoint(import_line) as trace_pt:
            TRACE_STACK[-1].add_child(trace_pt)
            TRACE_STACK.append(trace_pt)
            try:
                return f(*args, **kwargs)
            finally:
                TRACE_STACK.pop()
    return w
