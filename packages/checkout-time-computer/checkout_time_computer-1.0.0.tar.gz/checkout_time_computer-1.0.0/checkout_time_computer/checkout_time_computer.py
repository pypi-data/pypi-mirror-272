import heapq
from typing import List


class CheckoutTimeComputer:
    """Class to compute the total time required for all customers to check out."""

    def __init__(self, customers: List[int], n: int):
        """
        Initialize the CheckoutTimeComputer.

        Args:
            customers (List[int]): List of positive integers representing the customers' checkout times.
            n (int): Number of checkout counters.
        """
        if not isinstance(customers, list) or not all(isinstance(customer, int) and customer > 0 for customer in customers):
            raise ValueError("Customers must be a list of positive integers.")

        if not isinstance(n, int) or n <= 0:
            raise ValueError("Number of checkout counters must be a positive integer.")

        self.customers = customers
        self.n = n

    def compute_checkout_time(self) -> int:
        """
        Compute the total time required for all customers to check out.

        Returns:
            int: The total time required.
        """
        if self.n == 1:
            return sum(self.customers)

        checkout_counters = [0] * self.n

        for customer_time in self.customers:
            next_counter_time = heapq.heappop(checkout_counters)
            next_counter_time += customer_time
            heapq.heappush(checkout_counters, next_counter_time)

        return max(checkout_counters) if checkout_counters else 0