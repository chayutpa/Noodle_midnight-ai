from milkyway_ai import mean


def main() -> None:
    """Calculate and print the average of a fixed list of numbers."""
    values: list[int] = [1, 2, 3, 4, 5]
    print(f"Average value: {mean(values)}")


if __name__ == "__main__":
    main()
