from enum import Enum, auto

class BoxCallbackEnum(Enum):
    NONE = auto()
    ACCEPT = auto()
    REJECT = auto()

class BoxCallback:
    def call(self, callback_enum: BoxCallbackEnum):  ...