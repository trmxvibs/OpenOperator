from openoperator.agent.task_planner import TaskPlanner


def main() -> None:
    planner = TaskPlanner()

    plan = planner.create_plan(
        "type hello world"
    )

    print(plan.model_dump_json(indent=4))


if __name__ == "__main__":
    main()