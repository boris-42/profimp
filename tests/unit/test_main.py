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

from profimp import main
from tests.unit import test


class MainTestCase(test.TestCase):

    @mock.patch("profimp.main.print", create=True)
    def test_print_help(self, mock_print):
        main.print_help()
        mock_print.assert_called_once_with(main.HELP_MESSAGE)

    def test_trace_module(self):
        root_pt = main.trace_module("import re")

        self.assertEqual(1, len(root_pt.children))
        self.assertEqual("import re", root_pt.children[0].import_line)

    @mock.patch("profimp.main.print_help")
    @mock.patch("profimp.main.sys")
    def test_main_too_few_args(self, mock_sys, mock_print_help):
        mock_sys.argv = ["profimp"]
        main.main()
        mock_print_help.assert_called_once_with()

    @mock.patch("profimp.main.reports")
    @mock.patch("profimp.main.trace_module")
    @mock.patch("profimp.main.sys")
    def test_main(self, mock_sys, mock_trace_module, mock_reports):
        mock_sys.argv = ["profimp", "import re"]

        mock_trace_module.return_value
        main.main()

        mock_trace_module.assert_called_once_with("import re")
        mock_reports.to_json.assert_called_once_with(
            mock_trace_module.return_value)

    @mock.patch("profimp.main.print_help")
    @mock.patch("profimp.main.sys")
    def test_main_with_too_many_args(self, mock_sys, mock_print_help):
        mock_sys.argv = ["profimp", "module_one", "something else", "and"]
        self.assertRaises(SystemExit, main.main)
        mock_print_help.assert_called_once_with()

    @mock.patch("profimp.main.print_help")
    @mock.patch("profimp.main.sys")
    def test_main_html_wrong_key(self, mock_sys, mock_print_help):
        mock_sys.argv = ["profimp", "module_one", "not a --html"]
        self.assertRaises(SystemExit, main.main)
        mock_print_help.assert_called_once_with()

    @mock.patch("profimp.main.reports")
    @mock.patch("profimp.main.trace_module")
    @mock.patch("profimp.main.sys")
    def test_main_html(self, mock_sys, mock_trace_module, mock_reports):
        mock_sys.argv = ["profimp", "import re", "--html"]

        mock_trace_module.return_value
        main.main()

        mock_trace_module.assert_called_once_with("import re")
        mock_reports.to_html.assert_called_once_with(
            mock_trace_module.return_value)
