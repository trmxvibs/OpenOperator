from openoperator.agent.intelligent_planner import (
    IntelligentTaskPlanner,
)
from openoperator.agent.vision_models import (
    VisionActionType,
)


def test_open_and_type_plan():

    planner = IntelligentTaskPlanner()

    plan = planner.create_plan(
        "open notepad and type hello"
    )

    assert plan.is_executable is True

    assert len(plan.steps) == 2

    assert (
        plan.steps[0].action_type
        == VisionActionType.FOCUS_WINDOW
    )

    assert (
        plan.steps[1].action_type
        == VisionActionType.TYPE_TEXT
    )


def test_click_and_verify_plan():

    planner = IntelligentTaskPlanner()

    plan = planner.create_plan(
        "click file and verify saved"
    )

    assert len(plan.steps) == 2

    assert (
        plan.steps[0].action_type
        == VisionActionType.CLICK_TEXT
    )

    assert (
        plan.steps[1].action_type
        == VisionActionType.VERIFY_STATE
    )


def test_invalid_prompt():

    planner = IntelligentTaskPlanner()

    plan = planner.create_plan(
        "weather is nice today"
    )

    assert plan.is_executable is False

    assert len(plan.steps) == 0


def test_type_without_focus_fails_compiler():

    planner = IntelligentTaskPlanner()

    plan = planner.create_plan(
        "type hello"
    )

    assert plan.is_executable is False