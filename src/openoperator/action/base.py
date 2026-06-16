from abc import ABC
from abc import abstractmethod


class ActionController(ABC):

    @abstractmethod
    def move_mouse(self, x: int, y: int) -> bool:
        pass

    @abstractmethod
    def click(self, button: str = "left") -> bool:
        pass

    @abstractmethod
    def type_text(self, text: str) -> bool:
        pass
        
