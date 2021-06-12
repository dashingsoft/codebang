from unittest import TestCase
import cga
import util


class BufferTest(TestCase):

    def test_next(self):
        _input = '# test\n'
        buffer = cga.Buffer(_input)
        for i in _input:
            self.assertEqual(i, buffer.next())

    def test_current(self):
        _input = '# test\n'
        buffer = cga.Buffer(_input)
        for _ in _input:
            expect = buffer.next()
            self.assertEqual(expect, buffer.current())
            expect = 'ff'
            self.assertNotEqual(expect, buffer.current())

    def test_seek(self):
        _input = '012345\n'
        buffer = cga.Buffer(_input)
        for i in range(3):
            buffer.next()
        self.assertEqual('2', buffer.seek(0))
        self.assertEqual('0', buffer.seek(-2))
        self.assertEqual('\n', buffer.seek(4))
        self.assertEqual('4', buffer.seek(2))
        self.assertEqual(buffer.current(), buffer.seek(0))
        self.assertEqual(buffer.seek(1), buffer.next())
        self.assertEqual(buffer.next(), buffer.seek(0))

    def test_seeks(self):
        _input = '012345\n'
        buffer = cga.Buffer(_input)
        for i in range(3):
            buffer.next()

        self.assertEqual('01', buffer.seeks(-2))
        self.assertEqual('2', buffer.seeks(0))
        self.assertEqual('34', buffer.seeks(2))
        self.assertEqual('345\n', buffer.seeks(4))


class StaGraphTest(TestCase):

    def test_evolve(self):
        stat = cga.StaGraph()
        self.assertTrue(stat.evolve(cga.LexSta.PROCESSING))
        self.assertTrue(stat.evolve(cga.LexSta.END))
        self.assertTrue(stat.evolve(cga.LexSta.START))
        self.assertTrue(stat.evolve(cga.LexSta.PROCESSING))
        self.assertTrue(stat.evolve(cga.LexSta.END))

        self.assertFalse(stat.evolve(cga.LexSta.PROCESSING))

        self.assertTrue(stat.evolve(cga.LexSta.START))
        self.assertFalse(stat.evolve(cga.LexSta.END))

        self.assertTrue(stat.evolve(cga.LexSta.PROCESSING))
        self.assertFalse(stat.evolve(cga.LexSta.PROCESSING))


class TokenNodeTest(TestCase):

    def test_next(self):
        headnode = cga.TokenNode({'h1': 'the h1 title'})
        nextnode = cga.TokenNode({'text_line': 'here is text'})
        headnode.next = nextnode

        self.assertIs(headnode.next, nextnode)

    def test_get(self):
        node = cga.TokenNode({'h1': 'the h1 title'})
        self.assertEqual('the h1 title', node.get('h1'))

    def test_key(self):
        node = cga.TokenNode({'h1': 'the h1 title'})
        self.assertEqual('h1', node.key)

    def test_val(self):
        node = cga.TokenNode({'h1': 'the h1 title'})
        self.assertEqual('the h1 title', node.val)


class TestMakeTokenList(TestCase):

    def test_make_token_list(self):
        tokens = [
            {'h2': '##'},
            {'text_line': 'this is h2'},
            {'code_start': '```c'},
            {'text_line': 'int main() {'},
            {'text_line': '    return 0;'},
            {'text_line': '}'},
            {'code_end': '```'}
        ]

        expected = [cga.TokenNode(i) for i in tokens]

        for i in range(len(expected) - 1):
            expected[i].next = expected[i + 1]

        nodelist = cga.make_token_list(tokens)

        self.assertListEqual(expected, nodelist)


# class TestMain(TestCase):
#     def test_main(self):
#         md = '''# h1 text
#         ## h2 text
#
#         ```c
#         int main() {
#             printf(a);
#             return 0;
#         }
#         ```
#
#         ## h2 text2
#
#         ```c
#         int main() {
#             printf("hello world");
#         }
#         ```
#         '''
#
#         expected = '''# h1 text
#         ## h2 text
#
#         ```c
#         int main() {
#             printf(a);
#             return 0;
#         }
#         ```
#
#         ## errorinfo
#         ```
#         t1.c: In function ‘main’:
#         t1.c:2:5: warning: implicit declaration of function ‘printf’ [-Wimplicit-function-declaration]
#             2 |     printf(a);
#               |     ^~~~~~
#         t1.c:2:5: warning: incompatible implicit declaration of built-in function ‘printf’
#         t1.c:1:1: note: include ‘<stdio.h>’ or provide a declaration of ‘printf’
#           +++ |+#include <stdio.h>
#             1 | int main() {
#         t1.c:2:12: error: ‘a’ undeclared (first use in this function)
#             2 |     printf(a);
#               |            ^
#         t1.c:2:12: note: each undeclared identifier is reported only once for each function it appears in
#         ```
#
#         ## h2 text2
#
#         ```c
#         int main() {
#             printf("hello world");
#         }
#         ```
#         ## errorinfo
#         ```
#         t2.c: In function ‘main’:
#         t2.c:2:5: warning: implicit declaration of function ‘printf’ [-Wimplicit-function-declaration]
#             2 |     printf("hello world");
#               |     ^~~~~~
#         t2.c:2:5: warning: incompatible implicit declaration of built-in function ‘printf’
#         t2.c:1:1: note: include ‘<stdio.h>’ or provide a declaration of ‘printf’
#           +++ |+#include <stdio.h>
#             1 | int main() {
#         ```
#         '''
#
#         file_path = util.write2file(md)
#
#         cmd = f'python3 ../cga.py {file_path}'
#         util.execute_cmd(cmd)
#         with open(file_path, mode='r', encoding='utf-8') as f:
#             res = f.read()
#             f.close()
#         self.assertEqual(expected, res)
