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

import mock
from six.moves import builtins

from profimp import tracer
from tests.unit import test


class TracePointTestCase(test.TestCase):

    def test_init(self):
        pt = tracer.TracePoint("some_import_line", level=10)
        self.assertEqual(0, pt.started_at)
        self.assertEqual(0, pt.finished_at)
        self.assertEqual("some_import_line", pt.import_line)
        self.assertEqual(10, pt.level)
        self.assertEqual([], pt.children)

    @mock.patch("time.time", side_effect=[1, 2])
    def test_context(self, mock_time):
        with tracer.TracePoint("some_import_line") as pt:
            self.assertEqual(1, pt.started_at)

        self.assertEqual(2, pt.finished_at)

    @mock.patch("time.time", side_effect=[1, 2, 3, 4])
    def test_to_dict(self, mock_time):
        pt = tracer.TracePoint("import_line", level=2)
        pt_child = tracer.TracePoint("import_child")
        pt.add_child(pt_child)
        pt.start()
        pt_child.start()
        pt_child.stop()
        pt.stop()

        expected_pt_child_dict = {
            "started_at": 2,
            "finished_at": 3,
            "duration": 1000,
            "import_line": "import_child",
            "level": 3,
            "children": []
        }

        exepected_pt_dict = {
            "started_at": 1,
            "finished_at": 4,
            "duration": 3000,
            "import_line": "import_line",
            "level": 2,
            "children": [expected_pt_child_dict]
        }

        self.assertEqual(expected_pt_child_dict, pt_child.to_dict())
        self.assertEqual(exepected_pt_dict, pt.to_dict())

    @mock.patch("time.time", side_effect=[10])
    def test_start(self, mock_time):
        pt = tracer.TracePoint("import_line")
        pt.start()
        self.assertEqual(10, pt.started_at)

    @mock.patch("time.time", side_effect=[10])
    def test_stop(self, mock_time):
        pt = tracer.TracePoint("import_line")
        pt.stop()
        self.assertEqual(10, pt.finished_at)

    def test_add_child(self):
        pt = tracer.TracePoint("import_line")
        pt_child1 = tracer.TracePoint("import_line")
        pt_child11 = tracer.TracePoint("import_line")
        pt_child12 = tracer.TracePoint("import_line")
        pt_child2 = tracer.TracePoint("import_line")

        pt.add_child(pt_child1)
        pt_child1.add_child(pt_child11)
        pt_child1.add_child(pt_child12)
        pt.add_child(pt_child2)

        self.assertEqual([pt_child11, pt_child12], pt_child1.children)
        self.assertEqual([pt_child1, pt_child2], pt.children)

        self.assertEqual(0, pt.level)
        self.assertEqual(1, pt_child1.level)
        self.assertEqual(1, pt_child2.level)
        self.assertEqual(2, pt_child11.level)
        self.assertEqual(2, pt_child12.level)


class TraceModuleTestCase(test.TestCase):

    @mock.patch("profimp.tracer.TracePoint")
    def test_init_stack(self, mock_trace_pt):
        trace_pt = tracer.init_stack()
        mock_trace_pt.assert_called_once_with("root", 0)
        self.assertEqual(mock_trace_pt.return_value, trace_pt)
        self.assertEqual([mock_trace_pt.return_value], tracer.TRACE_STACK)

    @mock.patch("profimp.tracer._traceit")
    def test_patch_import(self, mock_traceit):
        normal_import = builtins.__import__

        with tracer.patch_import():
            self.assertEqual(mock_traceit.return_value, builtins.__import__)
            self.assertNotEqual(normal_import, builtins.__import__)

        self.assertEqual(normal_import, builtins.__import__)

    def test__traceit(self):
        tr_pt = tracer.init_stack()
        with tracer.patch_import():
            exec("import re")

        self.assertEqual(1, len(tr_pt.children))
        self.assertEqual("import re", tr_pt.children[0].import_line)

    def test__traceit_from_import(self):
        tr_pt = tracer.init_stack()
        with tracer.patch_import():
            exec("from os import sys")

        self.assertEqual(1, len(tr_pt.children))
        self.assertEqual("from os import sys", tr_pt.children[0].import_line)
