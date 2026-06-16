from openoperator.perception.screenshot import ScreenshotEngine


def test_capture_screen():
    engine = ScreenshotEngine()

    image = engine.capture()

    assert image is not None
    assert len(image) > 0
