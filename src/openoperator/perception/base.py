from abc import ABC
from abc import abstractmethod


class PerceptionEngine(ABC):

    @abstractmethod
    def capture_screen(self) -> bytes:
        pass
