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
