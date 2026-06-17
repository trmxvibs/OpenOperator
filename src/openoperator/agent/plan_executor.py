import logging
from typing import Optional

from openoperator.action.keyboard import KeyboardActionController
from openoperator.action.mouse import MouseActionController
from openoperator.agent.task_planner import TaskPlan

logger = logging.getLogger(__name__)


class PlanExecutor:

    def __init__(
        self,
        mouse_controller: Optional[MouseActionController] = None,
        keyboard_controller: Optional[KeyboardActionController] = None,
    ) -> None:
        self.mouse = mouse_controller or MouseActionController()
        self.keyboard = keyboard_controller or KeyboardActionController()

    def execute(self, plan: TaskPlan) -> None:
        logger.info(f"Starting execution of TaskPlan for goal: '{plan.goal}'")

        for index, action_item in enumerate(plan.actions, start=1):
            action_type = action_item.action.lower()

            try:
                if action_type == "move":
                    x = action_item.x if action_item.x is not None else 0
                    y = action_item.y if action_item.y is not None else 0
                    self.mouse.move_mouse(x, y)

                elif action_type == "click":
                    self.mouse.click("left")

                elif action_type == "type":
                    text_to_type = action_item.text or ""
                    if text_to_type:
                        self.keyboard.type_text(text_to_type)

                else:
                    logger.warning(f"Unsupported action: {action_type}")

            except Exception as e:
                logger.error(
                    f"Failed to execute step {index}: {e}",
                    exc_info=True,
                )

        logger.info("TaskPlan execution completed.")