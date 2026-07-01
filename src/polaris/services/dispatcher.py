from abc import ABC, abstractmethod
from polaris.models.event import Event


class BaseDispatcher(ABC):
    @abstractmethod
    async def send(self, event: Event):
        pass

class ConsoleDispatcher(BaseDispatcher):
    async def send(self, event: Event):
        print(f"[DISPATCH] {event.level} | {event.title} | {event.message}")