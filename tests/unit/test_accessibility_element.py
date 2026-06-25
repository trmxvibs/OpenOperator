from openoperator.perception.accessibility import AccessibilityElement


def test_accessibility_element_creation():
    element = AccessibilityElement(
        name="Save",
        control_type="Button",
        left=100,
        top=200,
        width=50,
        height=20,
        enabled=True,
    )

    assert element.name == "Save"
    assert element.control_type == "Button"
    assert element.left == 100
    assert element.top == 200
    assert element.width == 50
    assert element.height == 20
    assert element.enabled is True


def test_accessibility_element_center():
    element = AccessibilityElement(
        name="Save",
        control_type="Button",
        left=100,
        top=200,
        width=50,
        height=20,
        enabled=True,
    )

    assert element.center_x == 125
    assert element.center_y == 210