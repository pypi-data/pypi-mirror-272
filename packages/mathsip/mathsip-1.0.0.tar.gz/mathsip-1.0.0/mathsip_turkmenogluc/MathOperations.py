class MathOperations:
    """
    A simple class for basic mathematical operations.
    """

    def __init__(self, a, b):
        """
        Initialize the class with two numbers.
        """
        self.a = a
        self.b = b

    def add(self):
        """
        Adds the two numbers.
        """
        return self.a + self.b

    def subtract(self):
        """
        Subtracts the two numbers.
        """
        return self.a - self.b


# Example usage
if __name__ == "__main__":
    calculator = MathOperations(5, 3)
    sum = calculator.add()
    difference = calculator.subtract()
    print(f"Sum: {sum}, Difference: {difference}")
