from openoperator.perception.ui_automation import UIAutomationProvider
from openoperator.perception.accessibility import AccessibilityTree


class DummyProvider(UIAutomationProvider):
    def get_accessibility_tree(self) -> AccessibilityTree:
        return AccessibilityTree()


def test_provider_returns_accessibility_tree():
    provider = DummyProvider()

    tree = provider.get_accessibility_tree()

    assert isinstance(tree, AccessibilityTree)


def test_empty_tree_by_default():
    provider = DummyProvider()

    tree = provider.get_accessibility_tree()

    assert len(tree.elements) == 0


def test_provider_method_exists():
    provider = DummyProvider()

    assert hasattr(provider, "get_accessibility_tree")