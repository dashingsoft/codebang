from unittest import TestCase
import parser
import ca
from cga import TokenNode


class CATest(TestCase):

    def test_gcc(self):
        block = parser.CodeBlock(parser.CODE_TYPE.C)
        block.append(TokenNode({'text_line': 'int main() {'}))
        block.append(TokenNode({'text_line': '    return 0'}))
        block.append(TokenNode({'text_line': '}'}))
        error_info = ca.gcc(block.code)
        self.assertIsNotNone(error_info)

    def test_build_block(self):

        error_info = 'line1\nline2\n\n'
        info_block = parser.InfoBlock()
        for line in error_info.split('\n'):
            info_block.append(TokenNode({'text_line': line}))

        self.assertEqual(info_block, ca.build_block(error_info))
