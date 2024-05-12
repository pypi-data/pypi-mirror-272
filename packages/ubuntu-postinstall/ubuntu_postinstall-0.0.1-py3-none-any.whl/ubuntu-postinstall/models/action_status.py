from enum import Enum


class ActionStatus(Enum):
    PENDING = 0
    IN_PROGRESS = 1
    SUCCESS = 2
    FAILED = 3
