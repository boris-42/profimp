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


def _normalize(results, started_at=None):
    started_at = started_at or results["started_at"]

    results["started_at"] = (results["started_at"] - started_at) * 1000.0
    results["finished_at"] = (results["finished_at"] - started_at) * 1000.0

    for child in results["children"]:
        _normalize(child, started_at=started_at)

    return results


def to_json(results):
    return json.dumps(_normalize(results.to_dict()), indent=2)


def to_html(results):
    template_path = os.path.join(
        os.path.dirname(__file__), "templates", "report.tpl")

    with open(template_path) as html_template:
        report = html_template.read()
        return report.replace("{{DATA}}", to_json(results))
