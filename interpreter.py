import random
from enum import Enum
from queue import Queue
from stack import Stack
from exceptions import ReadError


class Direction(Enum):
    RIGHT = 0,
    DOWN = 1,
    LEFT = 2,
    UP = 3


class Interpreter:
    def __init__(self):
        self.program = []
        self.input_data = Queue()
        self.quote_mode = False

        self.xpos = 0
        self.ypos = 0

        self.direction = Direction.RIGHT
        self.stack = Stack()
        self.output = []

        self.commands = {
            '>': (self.change_direction, Direction.RIGHT),
            '<': (self.change_direction, Direction.LEFT),
            '^': (self.change_direction, Direction.UP),
            'v': (self.change_direction, Direction.DOWN),
            ' ': (lambda x: x, 1),
            '"': (self.change_mode,),
            '@': (self.exit,),
            '_': (self.check_horizontal_direction,),
            '|': (self.check_vertical_direction,),
            '?': (self.change_direction, random.choice(list(Direction))),
            ':': (self.copy_stack_top,),
            '\\': (self.swap,),
            '$': (self.drop,),
            '#': (self.skip_cell,),
            'p': (self.put,),
            'g': (self.get,),
            '+': (self.add,),
            '-': (self.sub,),
            '*': (self.mul,),
            '/': (self.div,),
            '%': (self.mod,),
            '!': (self.invert,),
            '`': (self.greater,),
            '&': (self.input_number,),
            '~': (self.input_char,),
            '.': (self.print_number,),
            ',': (self.print_char,)
        }

    def change_direction(self, direction):
        self.direction = direction

    def check_vertical_direction(self):
        if self.stack.pop() == 0:
            self.direction = Direction.DOWN
        else:
            self.direction = Direction.UP

    def check_horizontal_direction(self):
        if self.stack.pop() == 0:
            self.direction = Direction.RIGHT
        else:
            self.direction = Direction.LEFT

    def copy_stack_top(self):
        value = self.stack.pop()
        self.stack.append(value)
        self.stack.append(value)

    def swap(self):
        first = self.stack.pop()
        second = self.stack.pop()
        self.stack.append(first)
        self.stack.append(second)

    def drop(self):
        self.stack.pop()

    def skip_cell(self):
        self.move_pointer()

    def put(self):
        y, x, value = self.stack.pop(), self.stack.pop(), self.stack.pop()
        if 0 <= y < len(self.program) and 0 <= x < len(self.program[y]):
            self.program[y][x] = chr(value)

    def get(self):
        y, x = self.stack.pop(), self.stack.pop()
        if 0 <= y < len(self.program) and 0 <= x < len(self.program[y]):
            self.stack.append(ord(self.program[y][x]))
        else:
            self.stack.append(0)

    def add(self):
        y, x = self.stack.pop(), self.stack.pop()
        self.stack.append(x + y)

    def sub(self):
        y, x = self.stack.pop(), self.stack.pop()
        self.stack.append(x - y)

    def mul(self):
        y, x = self.stack.pop(), self.stack.pop()
        self.stack.append(x * y)

    def div(self):
        y, x = self.stack.pop(), self.stack.pop()
        self.stack.append(x // y)

    def mod(self):
        y, x = self.stack.pop(), self.stack.pop()
        self.stack.append(x % y)

    def invert(self):
        value = self.stack.pop()
        self.stack.append(1 if value == 0 else 0)

    def greater(self):
        first = self.stack.pop()
        second = self.stack.pop()
        self.stack.append(1 if second > first else 0)

    def input_number(self):
        if self.input_data.empty():
            raise ReadError("Входные данные введены не полностью.")
        n = self.input_data.get()
        try:
            self.stack.append(int(n))
        except ValueError:
            print(f'{n} is not int')

    def input_char(self):
        if self.input_data.empty():
            raise ReadError("Входные данные введены не полностью.")
        else:
            self.stack.append(ord(self.input_data.get()))

    def print_number(self):
        self.output.append(str(self.stack.pop()) + " ")

    def print_char(self):
        self.output.append(chr(self.stack.pop()))

    def change_mode(self):
        self.quote_mode = not self.quote_mode

    def exit(self):
        with open('output.txt', 'w') as f:
            f.write("".join(map(str, self.output)))
        exit()

    def load_file(self, program_file, input_file=None):
        try:
            with open(program_file) as f:
                for line in f:
                    self.program.append(list(line.rstrip()))
            if input_file is not None:
                with open(input_file) as f:
                    for s in f.readline().split():
                        self.input_data.put(s)
        except OSError as e:
            raise FileNotFoundError(e.filename)

    def move_pointer(self):
        if self.direction == Direction.RIGHT:
            self.xpos = (self.xpos + 1
                         if self.xpos != len(self.program[self.ypos]) - 1
                         else 0)
        elif self.direction == Direction.LEFT:
            self.xpos = (self.xpos - 1
                         if self.xpos != 0
                         else len(self.program[self.ypos]) - 1)
        elif self.direction == Direction.UP:
            self.ypos = (self.ypos - 1
                         if self.ypos != 0 else len(self.program) - 1)
        else:
            self.ypos = (self.ypos + 1
                         if self.ypos != len(self.program) - 1 else 0)

    def execute_command(self):
        symbol = self.program[self.ypos][self.xpos]
        if symbol.isdigit():
            self.stack.append(int(symbol))
        elif self.quote_mode and symbol != '"':
            self.stack.append(ord(symbol))
        else:
            command = self.commands[symbol]
            if len(command) == 1:
                command[0]()
            else:
                command[0](command[1])

    def run(self):
        while True:
            try:
                self.execute_command()
            except ReadError as e:
                print(e)
                return
            self.move_pointer()
