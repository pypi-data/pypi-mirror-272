# Copyright 2023 OpenC3, Inc.
# All Rights Reserved.
#
# This program is free software; you can modify and/or redistribute it
# under the terms of the GNU Affero General Public License
# as published by the Free Software Foundation; version 3 with
# attribution addendums as found in the LICENSE.txt
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# This file may also be used under the terms of a commercial license
# if purchased from OpenC3, Inc.

import unittest
from unittest.mock import *
from test.test_helper import *
from openc3.accessors.html_accessor import HtmlAccessor
from collections import namedtuple


class TestHtmlAccessor(unittest.TestCase):
    def setUp(self):
        self.data1 = bytearray(
            '<!DOCTYPE html><html lang="en"><head><title>My Title</title><script src="test.js"></script></head><body><noscript>No Script Detected</noscript><img src="test.jpg" alt="An Image"/><p>Paragraph</p><ul><li>1</li><li>3.14</li><li>[1.1,2.2,3.3]</li></ul></body></html>',
            encoding="utf-8",
        )
        self.Html = namedtuple("Html", ("name", "key", "data_type", "array_size"))

    def test_should_handle_various_keys(self):
        item = self.Html("ITEM", "/html/head/script/@src", "STRING", None)
        self.assertEqual(HtmlAccessor.class_read_item(item, self.data1), "test.js")

        item = self.Html("ITEM", "/html/body/noscript/text()", "STRING", None)
        self.assertEqual(
            HtmlAccessor.class_read_item(item, self.data1), "No Script Detected"
        )

        item = self.Html("ITEM", "/html/body/img/@src", "STRING", None)
        self.assertEqual(HtmlAccessor.class_read_item(item, self.data1), "test.jpg")

        item = self.Html("ITEM", "/html/body/ul/li[1]/text()", "UINT", None)
        self.assertEqual(HtmlAccessor.class_read_item(item, self.data1), 1)
        item = self.Html("ITEM", "/html/body/ul/li[1]/text()", "FLOAT", None)
        self.assertEqual(HtmlAccessor.class_read_item(item, self.data1), 1.0)
        item = self.Html("ITEM", "/html/body/ul/li[1]/text()", "STRING", None)
        self.assertEqual(HtmlAccessor.class_read_item(item, self.data1), "1")

        item = self.Html("ITEM", "/html/body/ul/li[2]/text()", "INT", None)
        self.assertEqual(HtmlAccessor.class_read_item(item, self.data1), 3)
        item = self.Html("ITEM", "/html/body/ul/li[2]/text()", "FLOAT", None)
        self.assertEqual(HtmlAccessor.class_read_item(item, self.data1), 3.14)
        item = self.Html("ITEM", "/html/body/ul/li[2]/text()", "STRING", None)
        self.assertEqual(HtmlAccessor.class_read_item(item, self.data1), "3.14")

        item = self.Html("ITEM", "/html/body/ul/li[3]/text()", "INT", 24)
        self.assertEqual(HtmlAccessor.class_read_item(item, self.data1), [1, 2, 3])
        item = self.Html("ITEM", "/html/body/ul/li[3]/text()", "FLOAT", 24)
        self.assertEqual(
            HtmlAccessor.class_read_item(item, self.data1), [1.1, 2.2, 3.3]
        )
        item = self.Html("ITEM", "/html/body/ul/li[3]/text()", "STRING", 24)
        self.assertEqual(
            HtmlAccessor.class_read_item(item, self.data1), ["1.1", "2.2", "3.3"]
        )

    def test_should_read_a_collection_of_items(self):
        item1 = self.Html("ITEM1", "/html/head/script/@src", "STRING", None)
        item2 = self.Html("ITEM2", "/html/body/noscript/text()", "STRING", None)
        item3 = self.Html("ITEM3", "/html/body/img/@src", "STRING", None)
        item4 = self.Html("ITEM4", "/html/body/ul/li[1]/text()", "UINT", None)
        item5 = self.Html("ITEM5", "/html/body/ul/li[2]/text()", "FLOAT", None)
        item6 = self.Html("ITEM6", "/html/body/ul/li[3]/text()", "FLOAT", 24)

        items = [item1, item2, item3, item4, item5, item6]

        results = HtmlAccessor.class_read_items(items, self.data1)
        self.assertEqual(results["ITEM1"], "test.js")
        self.assertEqual(results["ITEM2"], "No Script Detected")
        self.assertEqual(results["ITEM3"], "test.jpg")
        self.assertEqual(results["ITEM4"], 1)
        self.assertEqual(results["ITEM5"], 3.14)
        self.assertEqual(results["ITEM6"], [1.1, 2.2, 3.3])

    def test_should_write_different_types(self):
        item = self.Html("ITEM", "/html/head/script/@src", "STRING", None)
        HtmlAccessor.class_write_item(item, "different.js", self.data1)
        self.assertEqual(HtmlAccessor.class_read_item(item, self.data1), "different.js")

        item = self.Html("ITEM", "/html/body/noscript/text()", "STRING", None)
        HtmlAccessor.class_write_item(item, "Nothing Here", self.data1)
        self.assertEqual(HtmlAccessor.class_read_item(item, self.data1), "Nothing Here")

        item = self.Html("ITEM", "/html/body/img/@src", "STRING", None)
        HtmlAccessor.class_write_item(item, "other.png", self.data1)
        self.assertEqual(HtmlAccessor.class_read_item(item, self.data1), "other.png")

        item = self.Html("ITEM", "/html/body/ul/li[1]/text()", "UINT", None)
        HtmlAccessor.class_write_item(item, 15, self.data1)
        self.assertEqual(HtmlAccessor.class_read_item(item, self.data1), 15)

        item = self.Html("ITEM", "/html/body/ul/li[2]/text()", "FLOAT", None)
        HtmlAccessor.class_write_item(item, 1.234, self.data1)
        self.assertEqual(HtmlAccessor.class_read_item(item, self.data1), 1.234)

        item = self.Html("ITEM", "/html/body/ul/li[3]/text()", "FLOAT", 24)
        HtmlAccessor.class_write_item(item, ["2.2", 3, 4.4], self.data1)
        self.assertEqual(
            HtmlAccessor.class_read_item(item, self.data1), [2.2, 3.0, 4.4]
        )

    def test_should_write_multiple_items(self):
        item1 = self.Html("ITEM1", "/html/head/script/@src", "STRING", None)
        item2 = self.Html("ITEM2", "/html/body/noscript/text()", "STRING", None)
        item3 = self.Html("ITEM3", "/html/body/img/@src", "STRING", None)
        item4 = self.Html("ITEM4", "/html/body/ul/li[1]/text()", "UINT", None)
        item5 = self.Html("ITEM5", "/html/body/ul/li[2]/text()", "FLOAT", None)
        item6 = self.Html("ITEM6", "/html/body/ul/li[3]/text()", "FLOAT", 24)

        items = [item1, item2, item3, item4, item5, item6]
        values = [
            "different.js",
            "Nothing Here",
            "other.png",
            15,
            1.234,
            [2.2, 3.3, 4.4],
        ]
        HtmlAccessor.class_write_items(items, values, self.data1)

        self.assertEqual(
            HtmlAccessor.class_read_item(item1, self.data1), "different.js"
        )
        self.assertEqual(
            HtmlAccessor.class_read_item(item2, self.data1), "Nothing Here"
        )
        self.assertEqual(HtmlAccessor.class_read_item(item3, self.data1), "other.png")
        self.assertEqual(HtmlAccessor.class_read_item(item4, self.data1), 15)
        self.assertEqual(HtmlAccessor.class_read_item(item5, self.data1), 1.234)
        self.assertEqual(
            HtmlAccessor.class_read_item(item6, self.data1), [2.2, 3.3, 4.4]
        )
