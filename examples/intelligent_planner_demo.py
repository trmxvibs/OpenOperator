import json

from openoperator.agent.intelligent_planner import (
    IntelligentTaskPlanner,
)


def main():

    planner = IntelligentTaskPlanner()

    prompt = (
        "open notepad and click file "
        "and type hello world "
        "and verify hello world"
    )

    plan = planner.create_plan(prompt)

    print()

    print("PROMPT:")
    print(prompt)

    print()

    print("PLAN:")

    print(
        json.dumps(
            plan.model_dump(),
            indent=4,
        )
    )

    print()


if __name__ == "__main__":
    main()