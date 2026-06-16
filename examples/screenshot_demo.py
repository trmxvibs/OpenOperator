from openoperator.perception.screenshot import ScreenshotEngine


def main() -> None:
    engine = ScreenshotEngine()

    image = engine.capture_screen()

    print(
        f"Captured image bytes: {len(image)}"
    )


if __name__ == "__main__":
    main()