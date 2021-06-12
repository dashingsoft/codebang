from unittest import TestCase

import cga
import discern as ds
from util import write2file


class Test(TestCase):
    def test_ll_title_normal(self):
        buffer = cga.Buffer('## this is h2\n')
        act = ds.ll_title(buffer)
        self.assertEqual(4, len(act))
        expect = {
            'matched': True,
            'token': 'h2',
            'sign': '##',
            'remain': 'this is h2\n'
        }
        self.assertDictEqual(expect, act)

    def test_ll_title_exception(self):
        buffer = cga.Buffer(' ## this is h2\n')
        act = ds.ll_title(buffer)
        expect = {
            'matched': False,
            'remain': ' ## this is h2\n'
        }
        self.assertEqual(2, len(act))
        self.assertDictEqual(expect, act)

    def test_ll_text_line(self):
        buffer = cga.Buffer('## this is h2\n')
        act = ds.ll_text_line(buffer)
        expect = {
            'matched': True,
            'token': 'text_line',
            'sign': '## this is h2',
            'remain': ''
        }
        self.assertDictEqual(expect, act)

    def test_lexer(self):
        buffer = cga.Buffer('# this is h1\n')
        act = ds.lexer(buffer)
        expect = [{'h1': '#'}, {'text_line': 'this is h1'}]
        self.assertListEqual(expect, act)

    def test_lex_with_headline(self):
        md = '# this is h1\n'
        file_path = write2file(md)
        act = ds.lex(file_path)
        expect = [{'h1': '#'}, {'text_line': 'this is h1'}]
        self.assertListEqual(expect, act)

    def test_lex_with_text(self):
        md = '## this is h2\n  hello world!\nhappy tdd\n'
        file_path = write2file(md)
        act = ds.lex(file_path)
        expect = [
            {'h2': '##'},
            {'text_line': 'this is h2'},
            {'text_line': '  hello world!'},
            {'text_line': 'happy tdd'}
        ]
        self.assertListEqual(expect, act)

    def test_lex_with_code_block(self):
        md = '## this is h2\n```c\nint main() {\n    return 0;\n}\n```\n'
        file_path = write2file(md)
        act = ds.lex(file_path)
        expect = [
            {'h2': '##'},
            {'text_line': 'this is h2'},
            {'code_start': '```c'},
            {'text_line': 'int main() {'},
            {'text_line': '    return 0;'},
            {'text_line': '}'},
            {'code_end': '```'}
        ]
        self.assertListEqual(expect, act)
