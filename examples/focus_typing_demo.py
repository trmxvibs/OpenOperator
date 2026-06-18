import logging
import time

from pydantic import BaseModel

from openoperator.agent.plan_executor import PlanExecutor
from openoperator.agent.task_planner import TaskPlanner


class DemoResult(BaseModel):
    goal: str
    success: bool
    actions_executed: int


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    logger = logging.getLogger(__name__)

    planner = TaskPlanner()
    executor = PlanExecutor()

    goal = "move 500 500 click type Hello from OpenOperator"

    logger.info("Generating plan...")
    plan = planner.create_plan(goal)

    logger.info("Waiting 5 seconds...")
    time.sleep(5)

    success = executor.execute(plan)

    result = DemoResult(
        goal=goal,
        success=success,
        actions_executed=len(plan.actions) if success else 0,
    )

    print(result.model_dump_json(indent=4))


if __name__ == "__main__":
    main()