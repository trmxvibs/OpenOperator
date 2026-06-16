from openoperator.agent.base import AgentBrain
from openoperator.core.models import ActionIntent


class DummyAgent(AgentBrain):

    def decide_next_action(
        self,
        goal: str,
        screen_context: str,
    ) -> ActionIntent:

        return ActionIntent(
            action_type="done"
        )
