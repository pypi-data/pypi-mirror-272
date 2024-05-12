import unittest
from ubuntu_postinstall.models.action import Action
from ubuntu_postinstall.models.action_status import ActionStatus
from ubuntu_postinstall.models.command_line import CommandLine


class TestAction(unittest.TestCase):
    def test_init(self):
        action = Action('Hello, World!', [])
        self.assertEqual(action.message, 'Hello, World!')
        self.assertEqual(action.commands, [])
        self.assertEqual(action.status, ActionStatus.PENDING)

    def test_execute(self):
        action = Action('Hello, World!', [CommandLine('echo "Hello, World!"')])
        action.execute()
        self.assertEqual(action.status, ActionStatus.SUCCESS)

    def test_execute_failure(self):
        action = Action('Hello, World!', [CommandLine('i_am_not_a_real_command')])
        action.execute()
        self.assertEqual(action.status, ActionStatus.FAILED)
