"""
End-to-End Natural Language Planning Demo.

Demonstrates:

Prompt
    ↓
VisionIntentParser
    ↓
VisionPlanCompiler
    ↓
IntelligentTaskPlanner
    ↓
VisionTaskPlan
"""

import json

from openoperator.agent.intelligent_planner import (
    IntelligentTaskPlanner,
)


def print_plan(plan) -> None:

    print()
    print("=" * 60)
    print("EXECUTABLE:", plan.is_executable)
    print("=" * 60)

    for step in plan.steps:

        print(
            f"[{step.step_id}] "
            f"{step.action_type}"
        )

        if step.target_element:
            print(
                f"  target_element = "
                f"{step.target_element}"
            )

        if step.input_data:
            print(
                f"  input_data = "
                f"{step.input_data}"
            )

        print(
            f"  confidence = "
            f"{step.confidence}"
        )

        print()

    if plan.missing_context:

        print("MISSING CONTEXT:")

        for item in plan.missing_context:
            print("-", item)

    print("=" * 60)
    print()


def main() -> None:

    planner = IntelligentTaskPlanner()

    examples = [

        "open notepad and type hello world",

        (
            "switch to chrome "
            "and click search "
            "and type OpenOperator"
        ),

        (
            "open notepad "
            "and click file "
            "and verify file"
        ),
    ]

    for prompt in examples:

        print()
        print("#" * 60)
        print("PROMPT:")
        print(prompt)
        print("#" * 60)

        plan = planner.create_plan(prompt)

        print_plan(plan)

        print("RAW MODEL:")

        print(
            json.dumps(
                plan.model_dump(),
                indent=4,
            )
        )

        print()


if __name__ == "__main__":
    main()