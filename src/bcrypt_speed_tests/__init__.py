"""bcrypt cost-factor benchmark.

Tests multiple cost factors and reports average hash time.
Run this on the *same hardware* your app will run on.
"""

# ruff: noqa: T201
import statistics
import time

import bcrypt

PASSWORD = b"correct horse battery staple"
ITERATIONS = 3  # hashes per cost factor
COSTS = range(10, 15)  # adjust as needed


def benchmark_cost(cost: int, iterations: int) -> float:
    """Return the average time in seconds for a bcrypt cost factor.

    Args:
        cost: Bcrypt cost factor to benchmark.
        iterations: Number of hashes to run for the cost factor.

    Returns:
        The average time in seconds.

    """
    times = []
    for _ in range(iterations):
        start = time.perf_counter()
        bcrypt.hashpw(PASSWORD, bcrypt.gensalt(rounds=cost))
        end = time.perf_counter()
        times.append(end - start)
    return statistics.mean(times)


def main() -> None:
    """Run the benchmark for configured cost factors and print a table."""
    print(f"Iterations per cost: {ITERATIONS}\n")
    print(f"{'Cost':>4} | {'Avg time (ms)':>12}")
    print("-" * 22)

    for cost in COSTS:
        avg = benchmark_cost(cost, ITERATIONS)
        print(f"{cost:>4} | {avg * 1000:>12.1f}")


if __name__ == "__main__":
    main()
