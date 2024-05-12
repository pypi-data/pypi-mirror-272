from models.command_line import CommandLine
import unittest


class TestCommandLine(unittest.TestCase):
    def test_init(self):
        command = CommandLine('echo "Hello, World!"')
        self.assertEqual(command.command, 'echo "Hello, World!"')

    def test_execute(self):
        command = CommandLine('echo "Hello, World!"')
        self.assertTrue(command.execute())

    def test_execute_failure(self):
        command = CommandLine('i_am_not_a_real_command')
        self.assertFalse(command.execute())
