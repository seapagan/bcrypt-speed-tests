"""CLI entrypoint for bcrypt speed tests."""

# ruff: noqa: T201
from .benchmark import COSTS, ITERATIONS, benchmark_cost


def main() -> None:
    """Run the benchmark for configured cost factors and print a table."""
    print(f"Iterations per cost: {ITERATIONS}\n")
    print(f"{'Cost':>4} | {'Avg time (ms)':>12}")
    print("-" * 22)

    for cost in COSTS:
        avg = benchmark_cost(cost, ITERATIONS)
        print(f"{cost:>4} | {avg * 1000:>12.1f}")
