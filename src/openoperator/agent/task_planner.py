import logging
import re

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class PlannedAction(BaseModel):
    action: str
    x: int | None = None
    y: int | None = None
    text: str | None = None


class TaskPlan(BaseModel):
    goal: str
    actions: list[PlannedAction]


class TaskPlanner:

    def create_plan(self, goal: str) -> TaskPlan:
        logger.debug(f"Creating plan for goal: '{goal}'")

        actions: list[PlannedAction] = []

        pattern = re.compile(
            r"\b(move|click|type)\b(.*?)(?=\b(?:move|click|type)\b|$)",
            re.IGNORECASE,
        )

        matches = pattern.finditer(goal)

        for match in matches:
            action_type = match.group(1).lower()
            remainder = match.group(2).strip()

            if action_type == "move":
                coords = re.findall(r"\d+", remainder)

                if len(coords) >= 2:
                    x = int(coords[0])
                    y = int(coords[1])
                else:
                    x = 500
                    y = 500

                actions.append(
                    PlannedAction(
                        action="move",
                        x=x,
                        y=y,
                    )
                )

            elif action_type == "click":
                actions.append(
                    PlannedAction(
                        action="click"
                    )
                )

            elif action_type == "type":
                actions.append(
                    PlannedAction(
                        action="type",
                        text=remainder.strip(),
                    )
                )

        logger.info(
            f"Successfully generated TaskPlan with {len(actions)} actions."
        )

        return TaskPlan(
            goal=goal,
            actions=actions,
        )