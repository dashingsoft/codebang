from unittest import TestCase

import cga
import parser


class TestParser(TestCase):

    md = [
            {'h2': '##'},
            {'text_line': 'this is h2'},
            {'code_start': '```c'},
            {'text_line': 'int main() {'},
            {'text_line': '    return 0'},
            {'text_line': '}'},
            {'code_end': '```'}
        ]

    def test_hunt(self):
        prey = parser.hunt(self.md)
        block = parser.CodeBlock(parser.CODE_TYPE.C)
        block.append('int main() {')
        block.append('    return 0')
        block.append('}')
        expect = [block]
        for f, s in zip(expect, prey):
            self.assertEqual(f, s)

    def test_insert(self):

        token_list = cga.make_token_list(self.md)
        tokens = [
            {'h2': 'error info'},
            {'code_start': '```'},
            {'text_line': 'this is error info'},
            {'code_end': '```'}
        ]

        expected_token_list = cga.make_token_list(self.md)
        nodelist = cga.make_token_list(tokens)
        footer = expected_token_list[3].next
        expected_token_list[3].next = nodelist[0]
        nodelist[-1].next = footer

        self.assertNotEqual(expected_token_list[0], token_list[0])

        parser.insert(token_list[3], tokens)

        self.assertEqual(expected_token_list[0], token_list[0])
        self.assertEqual(expected_token_list, token_list)


class TestCodeBlock(TestCase):

    def test_code(self):
        codeblock = parser.CodeBlock(parser.CODE_TYPE.C)
        codeblock.append('line1')
        codeblock.append('line2')
        self.assertEqual('line1\nline2\n', codeblock.code)


class TestInfoBlock(TestCase):

    def test_tokens(self):
        infoblock = parser.InfoBlock()
        infoblock.append('line1')
        infoblock.append('line2')
        tokens = [
            {'h2': '##'},
            {'text_line': 'error info'},
            {'code_start': '```'},
            {'text_line': 'line1'},
            {'text_line': 'line2'},
            {'code_end': '```'}
        ]

        self.assertListEqual(tokens, infoblock.tokens)
