from openoperator.perception.accessibility import (
    AccessibilityElement,
    AccessibilityTree,
)


def test_find_buttons():
    tree = AccessibilityTree()

    tree.add(
        AccessibilityElement(
            name="Save",
            control_type="Button",
            left=0,
            top=0,
            width=100,
            height=40,
            enabled=True,
        )
    )

    tree.add(
        AccessibilityElement(
            name="Username",
            control_type="Edit",
            left=0,
            top=50,
            width=200,
            height=30,
            enabled=True,
        )
    )

    buttons = tree.find_by_control_type("Button")

    assert len(buttons) == 1
    assert buttons[0].name == "Save"


def test_find_missing_control_type():
    tree = AccessibilityTree()

    assert tree.find_by_control_type("Menu") == []