from openoperator.agent.intent_parser import VisionIntentParser
from openoperator.agent.vision_models import VisionActionType


def test_open_and_type_sequence():
    parser = VisionIntentParser()

    plan = parser.parse(
        "Open Notepad and type hello"
    )

    assert plan.is_executable is True
    assert len(plan.steps) == 2

    assert plan.steps[0].action_type == VisionActionType.FOCUS_WINDOW
    assert plan.steps[0].target_element == "Notepad"

    assert plan.steps[1].action_type == VisionActionType.TYPE_TEXT
    assert plan.steps[1].input_data == "hello"


def test_click_and_type_sequence():
    parser = VisionIntentParser()

    plan = parser.parse(
        "click file and type hello"
    )

    assert plan.is_executable is True
    assert len(plan.steps) == 2

    assert plan.steps[0].action_type == VisionActionType.CLICK_TEXT
    assert plan.steps[0].target_element == "file"

    assert plan.steps[1].action_type == VisionActionType.TYPE_TEXT
    assert plan.steps[1].input_data == "hello"


def test_then_connector():
    parser = VisionIntentParser()

    plan = parser.parse(
        "open notepad then type test"
    )

    assert len(plan.steps) == 2

    assert plan.steps[0].target_element == "notepad"
    assert plan.steps[1].input_data == "test"


def test_next_connector():
    parser = VisionIntentParser()

    plan = parser.parse(
        "open chrome next click search"
    )

    assert len(plan.steps) == 2

    assert plan.steps[0].target_element == "chrome"
    assert plan.steps[1].target_element == "search"


def test_verify_step():
    parser = VisionIntentParser()

    plan = parser.parse(
        "verify success"
    )

    assert len(plan.steps) == 1

    assert (
        plan.steps[0].action_type
        == VisionActionType.VERIFY_STATE
    )

    assert plan.steps[0].input_data == "success"


def test_no_valid_actions():
    parser = VisionIntentParser()

    plan = parser.parse(
        "this sentence contains nothing useful"
    )

    assert plan.is_executable is False
    assert len(plan.steps) == 0
    assert len(plan.missing_context) > 0


def test_click_on_keyword_cleanup():
    parser = VisionIntentParser()

    plan = parser.parse(
        "click on File"
    )

    assert len(plan.steps) == 1

    assert (
        plan.steps[0].target_element
        == "File"
    )