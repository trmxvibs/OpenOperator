from openoperator.agent.plan_compiler import VisionPlanCompiler
from openoperator.agent.vision_models import (
    VisionActionType,
    VisionStep,
    VisionTaskPlan,
)


def test_valid_focus_click_type_verify_plan():

    plan = VisionTaskPlan(
        original_prompt="test",
        is_executable=True,
        missing_context=[],
        steps=[
            VisionStep(
                step_id=1,
                action_type=VisionActionType.FOCUS_WINDOW,
                target_element="Notepad",
                confidence=1.0,
            ),
            VisionStep(
                step_id=2,
                action_type=VisionActionType.CLICK_TEXT,
                target_element="File",
                confidence=1.0,
            ),
            VisionStep(
                step_id=3,
                action_type=VisionActionType.TYPE_TEXT,
                input_data="Hello",
                confidence=1.0,
            ),
            VisionStep(
                step_id=4,
                action_type=VisionActionType.VERIFY_STATE,
                input_data="Hello",
                confidence=1.0,
            ),
        ],
    )

    compiler = VisionPlanCompiler()

    result = compiler.compile(plan)

    assert result.is_executable is True


def test_type_without_focus_or_click_fails():

    plan = VisionTaskPlan(
        original_prompt="type hello",
        is_executable=True,
        missing_context=[],
        steps=[
            VisionStep(
                step_id=1,
                action_type=VisionActionType.TYPE_TEXT,
                input_data="hello",
                confidence=1.0,
            )
        ],
    )

    compiler = VisionPlanCompiler()

    result = compiler.compile(plan)

    assert result.is_executable is False


def test_empty_plan_fails():

    plan = VisionTaskPlan(
        original_prompt="nothing",
        is_executable=True,
        missing_context=[],
        steps=[],
    )

    compiler = VisionPlanCompiler()

    result = compiler.compile(plan)

    assert result.is_executable is False


def test_click_without_target_fails():

    plan = VisionTaskPlan(
        original_prompt="click",
        is_executable=True,
        missing_context=[],
        steps=[
            VisionStep(
                step_id=1,
                action_type=VisionActionType.CLICK_TEXT,
                target_element=None,
                confidence=1.0,
            )
        ],
    )

    compiler = VisionPlanCompiler()

    result = compiler.compile(plan)

    assert result.is_executable is False


def test_verify_without_input_fails():

    plan = VisionTaskPlan(
        original_prompt="verify",
        is_executable=True,
        missing_context=[],
        steps=[
            VisionStep(
                step_id=1,
                action_type=VisionActionType.VERIFY_STATE,
                input_data=None,
                confidence=1.0,
            )
        ],
    )

    compiler = VisionPlanCompiler()

    result = compiler.compile(plan)

    assert result.is_executable is False