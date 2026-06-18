from openoperator.agent.task_planner import TaskPlanner


def test_type_action_parses_trailing_text() -> None:
    planner = TaskPlanner()

    plan = planner.create_plan(
        "type hello world"
    )

    assert len(plan.actions) == 1
    assert plan.actions[0].action == "type"
    assert plan.actions[0].text == "hello world"


def test_type_action_does_not_use_placeholder_when_empty() -> None:
    planner = TaskPlanner()

    plan = planner.create_plan(
        "type"
    )

    assert len(plan.actions) == 1
    assert plan.actions[0].action == "type"
    assert plan.actions[0].text == ""


def test_move_action_parses_coordinates() -> None:
    planner = TaskPlanner()

    plan = planner.create_plan(
        "move 500 300"
    )

    assert len(plan.actions) == 1
    assert plan.actions[0].action == "move"
    assert plan.actions[0].x == 500
    assert plan.actions[0].y == 300


def test_move_action_uses_default_coordinates() -> None:
    planner = TaskPlanner()

    plan = planner.create_plan(
        "move"
    )

    assert len(plan.actions) == 1
    assert plan.actions[0].action == "move"
    assert plan.actions[0].x == 500
    assert plan.actions[0].y == 500


def test_click_action_creates_click_step() -> None:
    planner = TaskPlanner()

    plan = planner.create_plan(
        "click"
    )

    assert len(plan.actions) == 1
    assert plan.actions[0].action == "click"


def test_compound_plan_generates_multiple_steps() -> None:
    planner = TaskPlanner()

    plan = planner.create_plan(
        "move 100 200 click type hello"
    )

    assert len(plan.actions) == 3

    assert plan.actions[0].action == "move"
    assert plan.actions[0].x == 100
    assert plan.actions[0].y == 200

    assert plan.actions[1].action == "click"

    assert plan.actions[2].action == "type"
    assert plan.actions[2].text == "hello"


def test_unknown_command_returns_empty_plan() -> None:
    planner = TaskPlanner()

    plan = planner.create_plan(
        "launch chrome browser"
    )

    assert len(plan.actions) == 0