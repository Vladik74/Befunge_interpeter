import unittest
from interpreter import Interpreter
import pathlib


class FileTests(unittest.TestCase):
    def setUp(self):
        self.interpreter = Interpreter()

    def tearDown(self):
        files = [pathlib.Path('program.txt'), pathlib.Path('input.txt'),
                 pathlib.Path('output.txt')]
        for f in files:
            try:
                f.unlink()
            except FileNotFoundError:
                pass

    def join_program_lines(self):
        lines = []
        for e in self.interpreter.program:
            lines.append("".join(e))
        return lines

    def test_correct_reading_program(self):
        with open('program.txt', 'w') as f:
            f.write('v.<\n>:|\n@')
        self.interpreter.load_file('program.txt')
        with open('program.txt', 'r') as f:
            self.assertEqual(f.read(), "\n".join(self.join_program_lines()))

    def test_correct_reading_input_data(self):
        with open('program.txt', 'w') as f:
            f.write('v.<\n>:|\n@')
        with open('input.txt', 'w') as f:
            f.write('7 4 a b')
        self.interpreter.load_file('program.txt', 'input.txt')
        with open('input.txt', 'r') as f:
            self.assertEqual(f.read(),
                             " ".join(list(self.interpreter.input_data.queue)))


if __name__ == '__main__':
    unittest.main()
