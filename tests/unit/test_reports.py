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

import os
import json

import mock

from profimp import reports
from tests.unit import test


class ReportsTestCase(test.TestCase):

    @mock.patch("profimp.reports._normalize")
    def test_to_json(self, mock_normalize):

        results = mock.MagicMock()
        results.to_dict.return_value = {"a": 1, "b": 20}
        mock_normalize.return_value = {"c": 10}

        self.assertEqual(json.dumps(mock_normalize.return_value, indent=2),
                         reports.to_json(results))
        mock_normalize.assert_called_once_with(results.to_dict.return_value)

    @mock.patch("profimp.reports.to_json")
    @mock.patch("profimp.reports.open", create=True)
    def test_html(self, mock_open, mock_to_json):
        mock_open.side_effect = [
            mock.mock_open(read_data="1_{{DATA}}_2").return_value
        ]

        mock_to_json.return_value = "ABC"

        template_path = os.path.join(
            os.path.dirname(reports.__file__), "templates", "report.tpl")

        results = mock.MagicMock()
        self.assertEqual("1_ABC_2", reports.to_html(results))
        mock_to_json.assert_called_once_with(results)
        mock_open.assert_called_once_with(template_path)

    def test_normalize(self):
        results = {
            "started_at": 1,
            "finished_at": 10,
            "children": [
                {
                    "started_at": 2,
                    "finished_at": 3,
                    "children": [
                        {
                            "started_at": 2.5,
                            "finished_at": 2.6,
                            "children": []
                        }
                    ]
                },
                {
                    "started_at": 3,
                    "finished_at": 4,
                    "children": []
                },
            ]
        }

        expected_normalized_results = {
            "started_at": 0.0,
            "finished_at": 9000.0,
            "children": [
                {
                    "started_at": 1000.0,
                    "finished_at": 2000.0,
                    "children": [
                        {
                            "started_at": 1500.0,
                            "finished_at": 1600.0,
                            "children": []
                        }
                    ]
                },
                {
                    "started_at": 2000.0,
                    "finished_at": 3000.0,
                    "children": []
                },
            ]
        }

        self.assertEqual(expected_normalized_results,
                         reports._normalize(results))
