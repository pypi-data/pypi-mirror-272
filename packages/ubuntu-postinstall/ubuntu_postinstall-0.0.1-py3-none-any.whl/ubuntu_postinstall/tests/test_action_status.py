import unittest
from ubuntu_postinstall.models.action import Action
from ubuntu_postinstall.models.command_function import CommandFunction

class TestAction(unittest.TestCase):
    def test_action(self):
        action = Action('Test action', [
            CommandFunction(lambda: True)
        ])
        self.assertEqual(action.message, 'Test action')
        self.assertEqual(len(action.commands), 1)
        self.assertEqual(action.commands[0].execute(), True)
