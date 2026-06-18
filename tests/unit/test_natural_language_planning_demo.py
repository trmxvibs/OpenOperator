from openoperator.agent.intelligent_planner import (
    IntelligentTaskPlanner,
)


def test_demo_prompt_generates_plan():

    planner = IntelligentTaskPlanner()

    plan = planner.create_plan(
        "open notepad and type hello"
    )

    assert plan.is_executable is True

    assert len(plan.steps) == 2


def test_demo_prompt_with_click():

    planner = IntelligentTaskPlanner()

    plan = planner.create_plan(
        "open chrome and click search"
    )

    assert plan.is_executable is True

    assert len(plan.steps) == 2