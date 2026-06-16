from abc import ABC
from abc import abstractmethod

from openoperator.core.models import ActionIntent


class AgentBrain(ABC):

    @abstractmethod
    def decide_next_action(
        self,
        goal: str,
        screen_context: str,
    ) -> ActionIntent:
        pass
