from QuackQuack import *

from lxml import html
import locale
import unittest
import pickle
import os
import os.path


class TestQuackQuack(unittest.TestCase):

    __TEST_DATA_DIR__ = "../data/"

    @classmethod
    def setUpClass(cls):
        locale.setlocale(locale.LC_ALL, "fr_FR")
        cls.test_pages = {}
        cls.test_menus = {}
        for file in os.listdir(cls.__TEST_DATA_DIR__):
            fp = os.path.join(cls.__TEST_DATA_DIR__, file)
            with open(fp, "rb") as fh:
                if "page" in file:
                    cls.test_pages[file] = pickle.load(fh)
                elif "menu" in file:
                    cls.test_menus[file] = pickle.load(fh)

    def test_2019_03_31(self):
        page = self.test_pages["test_page_2019-03-31.bin"]
        expected_menu = self.test_menus["test_menu_2019-03-31.bin"]
        html_tree = html.fromstring(page.content)
        obtained_menu = get_menu_from_html(html_tree)
        self.assertEqual(obtained_menu, expected_menu)


if __name__ == "__main__":
    unittest.main()
