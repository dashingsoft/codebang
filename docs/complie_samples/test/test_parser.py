from unittest import TestCase

import ca
import cga
import parser
from discern import lex
from util import write2file
import logging


class TestParser(TestCase):

    md = [
            {'h2': '##'},
            {'text_line': 'this is h2'},
            {'code_start': '```c'},
            {'text_line': 'int main() {'},
            {'text_line': '    return 0'},
            {'text_line': '}'},
            {'code_end': '```'},
            {'text_line': 'just a comment'}
        ]

    @classmethod
    def setUpClass(cls) -> None:
        logging.basicConfig(level=logging.INFO)

    def test_hunt(self):
        node_list = cga.make_token_list(self.md)
        prey = parser.hunt(node_list)
        block = parser.CodeBlock(parser.CODE_TYPE.C)
        block.append(cga.TokenNode({'code_start': '```c'}))
        block.append(cga.TokenNode({'text_line': 'int main() {'}))
        block.append(cga.TokenNode({'text_line': '    return 0'}))
        block.append(cga.TokenNode({'text_line': '}'}))
        block.append(cga.TokenNode({'code_end': '```'}))
        expect = [block]
        for f, s in zip(expect, prey):
            self.assertEqual(f, s)

    def test_insert_tokens(self):

        token_list = cga.make_token_list(self.md)
        expected_tokens = [
            {'h2': '##'},
            {'text_line': 'this is h2'},
            {'code_start': '```c'},
            {'text_line': 'int main() {'},
            {'h2': 'error info'},
            {'code_start': '```'},
            {'text_line': 'this is error info'},
            {'code_end': '```'},
            {'text_line': '    return 0'},
            {'text_line': '}'},
            {'code_end': '```'},
            {'text_line': 'just a comment'},
        ]
        expected_token_list = cga.make_token_list(expected_tokens)

        self.assertNotEqual(expected_token_list[0], token_list[0])

        tokens_for_inserting = [
            {'h2': 'error info'},
            {'code_start': '```'},
            {'text_line': 'this is error info'},
            {'code_end': '```'},
        ]
        parser.insert_tokens(token_list[3], tokens_for_inserting)

        self.assertEqual(expected_token_list[0], token_list[0])
        node = token_list[3]
        for _ in tokens_for_inserting:
            self.assertIsNotNone(node.next)
            node = node.next
        self.assertIsNone(token_list[-1].next)

    def test_insert(self):
        expected_md = [
            {'h2': '##'},
            {'text_line': 'this is h2'},
            {'code_start': '```c'},
            {'text_line': 'int main() {'},
            {'text_line': '    return 0'},
            {'text_line': '}'},
            {'code_end': '```'},
            {'text_line': ''},
            {'h2': '##'},
            {'text_line': 'error info'},
            {'code_start': '```'},
            {'text_line': 'this is error info'},
            {'code_end': '```'},
            {'text_line': ''},
            {'text_line': 'just a comment'},
        ]
        token_list = cga.make_token_list(self.md)
        expected_token_list = cga.make_token_list(expected_md)

        # self.assertNotEqual(expected_token_list[0], token_list[0])

        info_block = ca.build_block('this is error info')
        parser.insert(token_list[6], info_block)

        self.assertEqual(expected_token_list[6], token_list[6])
        self.assertEqual(expected_token_list[0], token_list[0])


class TestCodeBlock(TestCase):
    md = '''# h1 text
## h2 text

```c
int main() {
    printf(a);
    return 0;
}
```

## h2 text2

```c
int main() {
    printf("hello world");
}
```
'''

    def test_code(self):
        md = [
            '```c',
            'int main() {',
            '    printf("hello!");',
            'return 0;',
            '}',
            '```'
        ]
        path = write2file('\n'.join(md) + '\n')
        tokens = lex(path)
        node_list = cga.make_token_list(tokens)

        code_block = parser.CodeBlock(parser.CODE_TYPE.C)

        for i in node_list:
            code_block.append(i)

        self.assertEqual('int main() {\n    printf("hello!");\nreturn 0;\n}\n', code_block.code)

    def test_head_and_end(self):
        path = write2file(self.md)
        tokens = lex(path)
        node_list = cga.make_token_list(tokens)
        code_block = parser.CodeBlock(parser.CODE_TYPE.C)
        for i in node_list:
            code_block.append(i)
        self.assertEqual(node_list[0], code_block.head)
        self.assertEqual(node_list[-1], code_block.end)


class TestInfoBlock(TestCase):

    def test_tokens_and_str(self):
        info_block = parser.InfoBlock()
        info_block.append(cga.TokenNode({'text_line': 'line1'}))
        info_block.append(cga.TokenNode({'text_line': 'line2'}))
        tokens = [
            {'text_line': ''},
            {'h2': '##'},
            {'text_line': 'error info'},
            {'code_start': '```'},
            {'text_line': 'line1'},
            {'text_line': 'line2'},
            {'code_end': '```'},
            {'text_line': ''},
        ]

        self.assertEqual(str(tokens), str(info_block))
        self.assertListEqual(tokens, info_block.tokens)
