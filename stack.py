class Stack:
    def __init__(self):
        self.stack = []

    def __iter__(self):
        return self.stack

    def pop(self):
        if self.stack:
            return self.stack.pop()
        return 0

    def append(self, n):
        self.stack.append(n)