import os
from ubuntu_postinstall.models.command import Command


class CommandLine(Command):
    def __init__(self, command: str):
        self.command = command

    def execute(self) -> bool:
        exitcode = os.system(self.command)

        if exitcode == 0:
            return True

        return False
