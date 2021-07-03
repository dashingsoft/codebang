from unittest import TestCase

import cga
import gener
import util


class TestGener(TestCase):
    md = [
        {'h2': '##'},
        {'text_line': 'this is h2'},
        {'code_start': '```c'},
        {'text_line': 'int main() {'},
        {'text_line': '    return 0'},
        {'text_line': '}'},
        {'code_end': '```'}
    ]

    def test_write_to_md_without_inserted(self):
        node_list = cga.make_token_list(self.md)
        target = util.write2file('')
        gener.write_to_md(node_list, target)
        with open(target, mode='r', encoding='utf-8') as f:
            res = f.read()
            f.close()
        expected = [
            '## this is h2',
            '```c',
            'int main() {',
            '    return 0',
            '}',
            '```'
        ]
        self.assertEqual('\n'.join(expected) + '\n', res)
