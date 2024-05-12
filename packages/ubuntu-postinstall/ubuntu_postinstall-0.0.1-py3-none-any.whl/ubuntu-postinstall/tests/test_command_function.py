import unittest
from models.command_function import CommandFunction


def test_function():
    return True


class TestCommandFunction(unittest.TestCase):
    def test_init(self):
        command = CommandFunction(test_function)
        self.assertEqual(command.function, test_function)

    def test_execute(self):
        command = CommandFunction(test_function)
        self.assertTrue(command.execute())
