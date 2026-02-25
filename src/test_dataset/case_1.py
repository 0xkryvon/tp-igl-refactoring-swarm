from typing import List


def process_data(items: List[int]) -> List[int]:
    """Processes a list of numbers, doubling positive ones."""
    return [item * 2 for item in items if item > 0]


class DataProcessor:
    """Processes a list of numerical data."""
    def __init__(self, data: List[int]):
        """Initializes the DataProcessor with a list of integers."""
        self.data = data

    def filter_positive(self) -> List[int]:
        """Filters out and returns only positive numbers from the data."""
        return [x for x in self.data if x > 0]

    def get_sum(self) -> int:
        """Calculates the sum of all numbers in the data."""
        return sum(self.data)


def main():
    """Main function to demonstrate data processing."""
    numbers = [1, 2, 3, 4, 5]
    result = process_data(numbers)
    print(result)

    processor = DataProcessor([10, -5, 20, -3, 15])
    filtered = processor.filter_positive()
    print(filtered)


if __name__ == "__main__":
    main()