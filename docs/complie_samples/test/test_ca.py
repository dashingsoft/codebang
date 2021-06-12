from unittest import TestCase
import parser
import ca


class CATest(TestCase):

    def test_gcc(self):
        block = parser.CodeBlock(parser.CODE_TYPE.C)
        block.append('int main() {')
        block.append('    return 0')
        block.append('}')
        error_info = ca.gcc(block.code)
        self.assertIsNotNone(error_info)
