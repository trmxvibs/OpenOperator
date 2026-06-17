from openoperator.agent.task_planner import TaskPlanner


def test_type_action_parses_trailing_text() -> None:
    plan = TaskPlanner().create_plan("type hello world")

    assert len(plan.actions) == 1
    assert plan.actions[0].action == "type"
    assert plan.actions[0].text == "hello world"


def test_type_action_does_not_use_placeholder_when_empty() -> None:
    plan = TaskPlanner().create_plan("type")

    assert len(plan.actions) == 1
    assert plan.actions[0].action == "type"
    assert plan.actions[0].text == ""
