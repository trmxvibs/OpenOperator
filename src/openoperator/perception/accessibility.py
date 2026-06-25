"""
Accessibility models for OpenOperator.

Provides platform-independent accessibility element
representations that can later be populated by:

- Windows UI Automation
- macOS Accessibility API
- Linux AT-SPI
"""

from dataclasses import dataclass, field


@dataclass
class AccessibilityElement:
    """
    Represents a single UI element exposed through
    an operating system accessibility API.
    """

    name: str
    control_type: str

    left: int
    top: int
    width: int
    height: int

    enabled: bool = True
    interactable: bool = True

    @property
    def center_x(self) -> int:
        return self.left + self.width // 2

    @property
    def center_y(self) -> int:
        return self.top + self.height // 2

    @property
    def right(self) -> int:
        return self.left + self.width

    @property
    def bottom(self) -> int:
        return self.top + self.height

    @property
    def bounds(self) -> tuple[int, int, int, int]:
        return (
            self.left,
            self.top,
            self.right,
            self.bottom,
        )


@dataclass
class AccessibilityTree:
    """
    Container holding all accessibility elements
    detected on the current screen.
    """

    elements: list[AccessibilityElement] = field(default_factory=list)

    def add(self, element: AccessibilityElement) -> None:
        self.elements.append(element)

    def find_by_name(self, name: str):
        """
        Returns the first element whose name matches.
        """
        search = name.lower()

        for element in self.elements:
            if element.name.lower() == search:
                return element

        return None

    def find_by_control_type(self, control_type: str):
        """
        Returns every element having the requested control type.
        """
        search = control_type.lower()

        return [
            element
            for element in self.elements
            if element.control_type.lower() == search
        ]