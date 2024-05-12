from models.command import Command


class CommandFunction(Command):
    def __init__(self, function: callable, *args):
        self.function = function
        self.args = args

    def execute(self) -> bool:
        return self.function(*self.args)
