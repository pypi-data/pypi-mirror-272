# Copyright (c) 2024, Zhendong Peng (pzd17@tsinghua.org.cn)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from pyopenhc import opencc_clib


class OpenHC(opencc_clib._OpenCC):
    def __init__(self, config="t2s"):
        if not config.endswith(".json"):
            config += ".json"
        if not os.path.isfile(config):
            config = os.path.join(os.path.dirname(__file__), "data", config)
        super(OpenHC, self).__init__(config)
        self.config = config

    def convert(self, text):
        text = text.encode("utf-8")
        return super(OpenHC, self).convert(text, len(text))
