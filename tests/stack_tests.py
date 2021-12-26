import unittest
from stack import Stack


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.stack = Stack()

    def test_append(self):
        self.stack.append(3)
        self.stack.append('&')
        self.assertListEqual(self.stack.stack, [3, '&'])

    def test_pop(self):
        self.stack.append(2)
        self.stack.append('\\')
        self.stack.append('$')
        e = self.stack.pop()
        self.assertListEqual(self.stack.stack, [2, '\\'])
        self.assertEqual(e, '$')

    def test_empty_stack(self):
        e = self.stack.pop()
        self.assertListEqual(self.stack.stack, [])
        self.assertEqual(e, 0)

    def test_some_operations(self):
        self.stack.append('#')
        self.stack.append('?')
        self.stack.append('-')
        self.stack.pop()
        self.stack.pop()
        self.stack.append('#')
        self.assertListEqual(self.stack.stack, ['#', '#'])


if __name__ == '__main__':
    unittest.main()
