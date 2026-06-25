from openoperator.perception.accessibility import (
    AccessibilityElement,
    AccessibilityTree,
)


def test_empty_tree():
    tree = AccessibilityTree()

    assert len(tree.elements) == 0


def test_add_element():
    tree = AccessibilityTree()

    button = AccessibilityElement(
        name="Save",
        control_type="Button",
        left=10,
        top=20,
        width=100,
        height=30,
    )

    tree.add(button)

    assert len(tree.elements) == 1
    assert tree.elements[0].name == "Save"


def test_find_by_name():
    tree = AccessibilityTree()

    tree.add(
        AccessibilityElement(
            name="Save",
            control_type="Button",
            left=0,
            top=0,
            width=10,
            height=10,
        )
    )

    tree.add(
        AccessibilityElement(
            name="Cancel",
            control_type="Button",
            left=0,
            top=0,
            width=10,
            height=10,
        )
    )

    result = tree.find_by_name("Save")

    assert result is not None
    assert result.name == "Save"


def test_find_missing_name():
    tree = AccessibilityTree()

    result = tree.find_by_name("DoesNotExist")

    assert result is None