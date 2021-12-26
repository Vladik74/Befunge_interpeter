import math
import pathlib
import random
import unittest
from interpreter import Interpreter


class ExampleTests(unittest.TestCase):
    def setUp(self):
        self.interpreter = Interpreter()

    def tearDown(self):
        files = [pathlib.Path('test_program.txt'), pathlib.Path('output.txt'),
                 pathlib.Path('input.txt')]
        for f in files:
            try:
                f.unlink()
            except FileNotFoundError:
                pass

    def test_printing_hello_word(self):
        with open('test_program.txt', 'w') as f:
            f.write('25*"!dlroW ,olleH" >:#,_@')
        self.interpreter.load_file('test_program.txt')
        with self.assertRaises(SystemExit):
            self.interpreter.run()
        with open('output.txt', 'r') as h:
            line = h.readline()
            self.assertEqual(line.rstrip('\n'), 'Hello, World!')

    def test_fourth_factorial(self):
        with open('test_program.txt', 'w') as f:
            f.write('44* >:1-:v    v ,*25 .:* ,,,,"! = ".:_ @ '
                    '\n    ^    _ $1 > \:                   ^ ')
        self.interpreter.load_file('test_program.txt')
        with self.assertRaises(SystemExit):
            self.interpreter.run()
        with open('output.txt', 'r') as h:
            lines = h.readlines()
            self.assertEqual(lines[3].rstrip('\n '), '4 ! = 24')

    def test_fibonacci_numbers(self):
        with open('test_program.txt', 'w') as f:
            f.write('031p132p 94+ > 31g 32g :. + 32g v'
                    '\n             | :-1,,", "p23 p13 <'
                    '\n             > "."::,,,@')
        self.interpreter.load_file('test_program.txt')
        with self.assertRaises(SystemExit):
            self.interpreter.run()
        with open('output.txt', 'r') as h:
            lines = h.readlines()
            self.assertEqual(*lines, '1 , 1 , 2 , 3 , 5 , 8 , 13 , 21 , 34 , '
                                     '55 , 89 , 144 , 233 , ...')

    def test_random_factorial(self):
        rnd = random.randint(2, 10)
        with open('test_program.txt', 'w') as f:
            f.write('vv    <>v *<\n&>:1-:|$>\:|\n>^    >^@.$<')
        with open('input.txt', 'w') as g:
            g.write(str(rnd))
        self.interpreter.load_file('test_program.txt', 'input.txt')
        with self.assertRaises(SystemExit):
            self.interpreter.run()
        with open('output.txt', 'r') as h:
            line = h.readline()
            self.assertEqual(line.rstrip(' '), str(math.factorial(rnd)))

    def test_gcd(self):
        rnd1 = random.randint(2, 200)
        rnd2 = random.randint(2, 200)
        with open('test_program.txt', 'w') as f:
            f.write(f'#v&<     @.$< \n:<\g05%p05:_^#')
        with open('input.txt', 'w') as g:
            g.write(f'{rnd1} {rnd2}')
        self.interpreter.load_file('test_program.txt', 'input.txt')
        with self.assertRaises(SystemExit):
            self.interpreter.run()
        with open('output.txt', 'r') as h:
            line = h.readline()
            self.assertEqual(line.rstrip(' '), str(math.gcd(rnd1, rnd2)))


if __name__ == '__main__':
    unittest.main()
