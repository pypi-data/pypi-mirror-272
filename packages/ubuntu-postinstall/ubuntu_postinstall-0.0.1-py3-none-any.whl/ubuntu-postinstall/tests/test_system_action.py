import unittest
from models.command_function import CommandFunction
from models.system_action import SystemAction


class TestSystemAction(unittest.TestCase):
    def test_init(self):
        command = SystemAction('Test Action', [])
        self.assertEqual(command.commands, [])
        self.assertEqual(command.message, 'Test Action')

    def test_init_failure(self):
        with self.assertRaises(TypeError):
            SystemAction('Test Action', [False])

    def test_init_failure2(self):
        with self.assertRaises(TypeError):
            SystemAction('Test Action', [CommandFunction(lambda: print("Hello, World!"))])
