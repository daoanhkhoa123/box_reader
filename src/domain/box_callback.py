from enum import Enum, auto


class CallbackEnum(Enum):
    ACCEPT = auto()
    REJECT = auto()

class ModelCallback:
    def call(self, callback_enum: CallbackEnum):  ...