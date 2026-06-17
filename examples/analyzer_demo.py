from openoperator.perception.screen_analyzer import ScreenAnalyzer


def main() -> None:
    analyzer = ScreenAnalyzer()

    result = analyzer.analyze_screen()

    print("\n===== ANALYSIS =====\n")
    print(f"Words : {result.word_count}")
    print(f"Lines : {result.line_count}")
    print()
    print(result.text[:1000])
    print("\n====================\n")


if __name__ == "__main__":
    main()