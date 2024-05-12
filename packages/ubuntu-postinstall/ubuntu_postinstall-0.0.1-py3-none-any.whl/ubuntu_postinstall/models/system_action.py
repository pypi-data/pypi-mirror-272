from ubuntu_postinstall.models.action import Action
from ubuntu_postinstall.models.command_line import CommandLine


class SystemAction(Action):
    def __init__(self, message: str, commands: list[CommandLine]):
        for command in commands:
            if not isinstance(command, CommandLine):
                raise TypeError("SystemAction can only contain CommandLine objects")

        super().__init__(message, commands)
