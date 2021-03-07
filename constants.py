from enum import Enum
HOST_ADDR = '203.253.23.46'
LOCALHOST = 'localhost'


class Session(Enum):
    SESSION_START = 1
    SESSION_PAUSE = 2
    SESSION_END = 3


class Level(Enum):
    """Difficulty Level"""
    LOW = 1
    LOW_MEDIUM = 2
    MEDIUM = 3
    MEDIUM_HIGH = 4
    HIGH = 5


class Conditions(Enum):
    """Offering Conditions"""
    WAITING = 'Waiting'
    STARTED = 'Started'
    PAUSED = 'Paused'
    CANCELED = 'Canceled'
    FINISHED = 'Finished'
