import logging
import time

from openoperator.agent.plan_executor import PlanExecutor
from openoperator.agent.task_planner import TaskPlanner


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    planner = TaskPlanner()
    executor = PlanExecutor()

    goal = "type hello from openoperator"

    plan = planner.create_plan(goal)

    print("\nGENERATED PLAN\n")
    print(plan.model_dump_json(indent=4))

    print("\nExecuting in 5 seconds...")
    time.sleep(5)

    executor.execute(plan)

    print("Done")


if __name__ == "__main__":
    main()
    
    