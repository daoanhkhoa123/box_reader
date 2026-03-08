import logging
from src.domain.box_callback import BoxCallbackEnum, BoxCallback
logger = logging.getLogger(__name__)

class BoxCallBackService(BoxCallback):
    def __init__(self) -> None:
        super().__init__()
        self.logger = logger.getChild(self.__class__.__name__)
        self.logger.debug("Box Call Back Service initialized")

    def call(self, callback_enum: BoxCallbackEnum):
        self.logger.debug("Callback recieved %s", callback_enum)
        if callback_enum == BoxCallbackEnum.NONE:
            return
    
        if callback_enum == BoxCallbackEnum.ACCEPT:
            ...

        if callback_enum == BoxCallbackEnum.REJECT:
            ...