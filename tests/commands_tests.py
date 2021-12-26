import unittest
from interpreter import Interpreter
from exceptions import ReadError


class CommandsTest(unittest.TestCase):
    def setUp(self):
        self.interpreter = Interpreter()

    def move(self):
        self.interpreter.execute_command()
        self.interpreter.move_pointer()

    def test_up_command(self):
        self.interpreter.program = [['^'], [' '], ['@'], [' ']]
        self.move()
        self.move()
        self.assertEqual(self.interpreter.ypos, 2)
        self.assertEqual(self.interpreter.xpos, 0)

    def test_down_command(self):
        self.interpreter.program = [['v'], [' '], [' '], ['@']]
        self.move()
        self.move()
        self.assertEqual(self.interpreter.ypos, 2)
        self.assertEqual(self.interpreter.xpos, 0)

    def test_right_command(self):
        self.interpreter.program = [['>', 'v', ' ', ' '], ['@', '>', ' ', ' ']]
        for _ in range(5):
            self.move()
        self.assertEqual(self.interpreter.ypos, 1)
        self.assertEqual(self.interpreter.xpos, 0)

    def test_left_command(self):
        self.interpreter.program = [['<', '@', ' ']]
        self.move()
        self.move()
        self.assertEqual(self.interpreter.ypos, 0)
        self.assertEqual(self.interpreter.xpos, 1)

    def test_horizontal_if_zero_in_stack(self):
        self.interpreter.stack.append(0)
        self.interpreter.program = [['_', ' ', ' ', '@']]
        for _ in range(3):
            self.move()
        self.assertEqual(self.interpreter.ypos, 0)
        self.assertEqual(self.interpreter.xpos, 3)

    def test_horizontal_if_not_zero_in_stack(self):
        self.interpreter.stack.append(1)
        self.interpreter.program = [['_', ' ', '@', ' ']]
        self.move()
        self.move()
        self.assertEqual(self.interpreter.ypos, 0)
        self.assertEqual(self.interpreter.xpos, 2)

    def test_vertical_if_zero_in_stack(self):
        self.interpreter.stack.append(0)
        self.interpreter.program = [['|'], [' '], ['@']]
        self.move()
        self.move()
        self.assertEqual(self.interpreter.ypos, 2)
        self.assertEqual(self.interpreter.xpos, 0)

    def test_vertical_if_not_zero_in_stack(self):
        self.interpreter.stack.append(1)
        self.interpreter.program = [['|'], ['@'], [' '], [' ']]
        for _ in range(3):
            self.move()
        self.assertEqual(self.interpreter.ypos, 1)
        self.assertEqual(self.interpreter.xpos, 0)

    def test_change_mode(self):
        self.interpreter.change_mode()
        self.assertTrue(self.interpreter.quote_mode)

    def test_copy_stack(self):
        self.interpreter.stack.append(1)
        self.interpreter.copy_stack_top()
        self.assertEqual(self.interpreter.stack.stack, [1, 1])

    def test_swap(self):
        self.interpreter.stack.append(0)
        self.interpreter.stack.append(1)
        self.interpreter.swap()
        self.assertEqual(self.interpreter.stack.stack, [1, 0])

    def test_drop(self):
        self.interpreter.stack.append(0)
        self.interpreter.stack.append(1)
        self.interpreter.drop()
        self.assertEqual(self.interpreter.stack.stack, [0])

    def test_skip_cell(self):
        self.interpreter.program = [['>', ' ', ' ', 'v'], [' ', ' ', ' ', ' '],
                                    ['@', ' ', '#', '<']]
        for _ in range(7):
            self.move()
        self.assertEqual(self.interpreter.ypos, 2)
        self.assertEqual(self.interpreter.xpos, 0)

    def test_put(self):
        self.interpreter.stack.append(97)
        self.interpreter.stack.append(2)
        self.interpreter.stack.append(0)
        self.interpreter.program = [['p', '@', ' ']]
        self.interpreter.put()
        self.assertEqual(self.interpreter.program, [['p', '@', 'a']])

    def test_get(self):
        self.interpreter.stack.append(2)
        self.interpreter.stack.append(0)
        self.interpreter.program = [['g', '@', 'a']]
        self.interpreter.get()
        self.assertEqual(self.interpreter.program, [['g', '@', 'a']])
        self.assertEqual(self.interpreter.stack.stack, [97])

    def test_get_if_cell_not_exists(self):
        self.interpreter.stack.append(3)
        self.interpreter.stack.append(0)
        self.interpreter.program = [['g', '@', 'a']]
        self.interpreter.get()
        self.assertEqual(self.interpreter.program, [['g', '@', 'a']])
        self.assertEqual(self.interpreter.stack.stack, [0])

    def test_add(self):
        self.interpreter.stack.append(1)
        self.interpreter.stack.append(2)
        self.interpreter.add()
        self.assertEqual(self.interpreter.stack.stack, [3])

    def test_sub(self):
        self.interpreter.stack.append(3)
        self.interpreter.stack.append(2)
        self.interpreter.sub()
        self.assertEqual(self.interpreter.stack.stack, [1])

    def test_mul(self):
        self.interpreter.stack.append(4)
        self.interpreter.stack.append(2)
        self.interpreter.mul()
        self.assertEqual(self.interpreter.stack.stack, [8])

    def test_div(self):
        self.interpreter.stack.append(16)
        self.interpreter.stack.append(2)
        self.interpreter.div()
        self.assertEqual(self.interpreter.stack.stack, [8])

    def test_mod(self):
        self.interpreter.stack.append(5)
        self.interpreter.stack.append(2)
        self.interpreter.mod()
        self.assertEqual(self.interpreter.stack.stack, [1])

    def test_invert(self):
        self.interpreter.stack.append(3)
        self.interpreter.invert()
        self.assertEqual(self.interpreter.stack.stack, [0])
        self.interpreter.invert()
        self.assertEqual(self.interpreter.stack.stack, [1])

    def test_greater(self):
        self.interpreter.stack.append(4)
        self.interpreter.stack.append(3)
        self.interpreter.greater()
        self.assertEqual(self.interpreter.stack.stack, [1])
        self.interpreter.stack.append(3)
        self.interpreter.greater()
        self.assertEqual(self.interpreter.stack.stack, [0])

    def test_input_number_if_exits(self):
        self.interpreter.program = [['&', '@']]
        self.interpreter.input_data.put(3)
        self.move()
        self.assertEqual(self.interpreter.stack.stack, [3])

    def test_input_number_if_empty(self):
        with self.assertRaises(ReadError):
            self.interpreter.input_number()

    def test_input_number_if_char(self):
        self.interpreter.input_data.put('a')
        self.interpreter.input_number()
        self.assertRaises(ValueError)

    def test_input_char(self):
        self.interpreter.program = [['~', '@']]
        self.interpreter.input_data.put('a')
        self.move()
        self.assertEqual(self.interpreter.stack.stack, [97])

    def test_input_char_if_empty(self):
        with self.assertRaises(ReadError):
            self.interpreter.input_char()

    def test_print_number(self):
        self.interpreter.program = [['.', '@']]
        self.interpreter.stack.append(5)
        self.move()
        self.assertEqual(self.interpreter.output, ['5 '])

    def test_print_char(self):
        self.interpreter.program = [[',', '@']]
        self.interpreter.stack.append(97)
        self.move()
        self.assertEqual(self.interpreter.output, ['a'])

    def test_unknown_command(self):
        self.interpreter.program = [['(', '@']]
        with self.assertRaises(KeyError):
            self.move()


if __name__ == '__main__':
    unittest.main()
