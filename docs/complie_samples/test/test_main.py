from unittest import TestCase

import util
import os


class TestMain(TestCase):
    def test_main_without_args(self):
        cmd = 'python3 ../main.py'.split(' ')
        res = util.execute_in_shell(cmd)
        self.assertTrue('[-h] [-v] [-o OUTPUT] markdown' in res)

    def test_main_with_only_input_file(self):
        cmd = 'python3 ../main.py ./test.md'.split(' ')
        res = util.execute_in_shell(cmd)
        self.assertTrue(os.path.exists('test.cc.md'))

    def test_main_with_output_file(self):
        cmd = 'python3 ../main.py ./test.md -o ./build/test-output.md'.split(' ')
        res = util.execute_in_shell(cmd)
        self.assertTrue(os.path.exists('./build/test-output.md'))
