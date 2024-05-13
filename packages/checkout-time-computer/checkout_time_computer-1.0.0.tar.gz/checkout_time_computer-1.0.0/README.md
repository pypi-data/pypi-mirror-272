# checkout-time-computer

checkout-time-computer simulates a grocery store checkout line to determine the total time required for all customers to check out.

## Installation

Package is published on [PyPI](https://pypi.org/project/checkout-time-computer/), you can install it using pip:

```
pip install checkout-time-computer
```

## Usage

```python
from checkout_time_computer import CheckoutTimeComputer

# Example usage
checkout_computer = CheckoutTimeComputer([5, 3, 4], 1)
print(checkout_computer.compute_checkout_time())  # Output: 12

checkout_computer = CheckoutTimeComputer([10, 2, 3, 3], 2)
print(checkout_computer.compute_checkout_time())  # Output: 10

checkout_computer = CheckoutTimeComputer([2, 3, 10], 2)
print(checkout_computer.compute_checkout_time())  # Output: 12
```

## Local development

Project is set up using Poetry, to run it locally follow these steps:

1. Clone this repository to your local machine:

    ```
    git clone https://github.com/augustinasn/checkout-time-computer.git
    ```

2. Navigate to the project directory:

    ```
    cd checkout-time-computer
    ```

3. Install Poetry (if you haven't already):

    ```
    pip install poetry
    ```

4. Use Poetry to install the project's dependencies:

    ```
    poetry install
    ```

5. Activate the Poetry virtual environment:

    ```
    poetry shell
    ```

6. Tests are included in the tests directory. You can run the tests using the following command:
    ```
    python test.py
    ```
## License

This project is licensed under the MIT License - see the [LICENSE](LICENCE) file for details.