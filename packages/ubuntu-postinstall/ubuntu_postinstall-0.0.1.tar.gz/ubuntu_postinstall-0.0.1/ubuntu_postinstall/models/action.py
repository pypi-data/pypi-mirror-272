from ubuntu_postinstall.models.action_status import ActionStatus
from ubuntu_postinstall.models.command import Command


class Action:
    def __init__(self, message: str, commands: list[Command]):
        self.message = message
        self.commands = commands
        self.status = ActionStatus.PENDING

    def execute(self):
        self.status = ActionStatus.IN_PROGRESS
        for command in self.commands:
            result = command.execute()
            if not result:
                self.status = ActionStatus.FAILED
                return
        self.status = ActionStatus.SUCCESS
