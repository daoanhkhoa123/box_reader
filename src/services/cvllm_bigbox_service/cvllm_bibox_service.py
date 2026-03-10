from src.infrastructure.event_bus import EventBus

class CVLLMBigBoxEvent: ...

class CVLLMBigBoxSevice:
    def __init__(self, event_bus: EventBus) -> None:
        event_bus.subscribe(CVLLMBigBoxEvent, self.run)

    def run(self, event: CVLLMBigBoxEvent):
        print("reading some box", event)

        