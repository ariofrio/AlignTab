import sublime, sys
from unittest import TestCase

version = sublime.version()

import AlignTab.aligntab as aligntab


class TestAlignTab(TestCase):

    def setUp(self):
        self.view = sublime.active_window().new_file()

    def tearDown(self):
        if self.view:
            self.view.set_scratch(True)
            # don't close the last tab in osx platform
            if len(self.view.window().views()) == 1 and sublime.platform() == "osx": return
            self.view.window().run_command("close_file")

    def setText(self, string):
        self.view.run_command("insert", {"characters": string})

    def getRow(self, row):
        return self.view.substr(self.view.line(self.view.text_point(row-1,0)))

    def test_align_equal(self):
        string = """apple =  1==0
        banana = 100
        car =    2"""
        self.setText(string)
        self.view.run_command("align_tab", {"user_input" :"=/f"})

        first_row = self.getRow(1)
        self.assertEqual(first_row,"apple  = 1==0")

    def test_align_tab(self):
        self.view.settings().set("translate_tabs_to_spaces", False)
        string = """a \t b \t   c
        d \t   e \tf"""
        self.setText(string)
        self.view.run_command("align_tab", {"user_input" :"\t"})

        second_row = self.getRow(2)
        self.assertEqual(second_row,"d \t e \t f")


class TestHelloWorld2(TestCase):

    def test_input_parser(self):
        input = "=/l0r*2f3"
        output = aligntab.input_parser(input)
        self.assertEqual(output, ['=', [['l', 0], ['r', 1], ['r', 1]], 3])
