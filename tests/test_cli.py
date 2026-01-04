"""CLI integration tests for bcrypt-speed-tests."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from typer.testing import CliRunner

from bcrypt_speed_tests.main import app

if TYPE_CHECKING:
    from pytest_mock import MockerFixture


@pytest.fixture
def runner() -> CliRunner:
    """Provide a Typer CLI runner for tests."""
    return CliRunner()


def test_cli_defaults_use_configured_costs(
    runner: CliRunner, mocker: MockerFixture
) -> None:
    """Render the default table using the configured costs."""
    mocker.patch("bcrypt_speed_tests.main.COSTS", [4, 5])
    mocker.patch(
        "bcrypt_speed_tests.main.benchmark_cost",
        side_effect=lambda cost, _iterations: 0.01 * cost,
    )

    result = runner.invoke(app, [])

    assert result.exit_code == 0
    assert "Iterations per cost: 3" in result.output
    assert "   4 |" in result.output
    assert "   5 |" in result.output


def test_cli_custom_options_override_defaults(
    runner: CliRunner, mocker: MockerFixture
) -> None:
    """Use CLI options to override costs and iterations."""
    calls: list[tuple[int, int]] = []

    def fake_benchmark(cost: int, iterations: int) -> float:
        calls.append((cost, iterations))
        return 0.001

    mocker.patch(
        "bcrypt_speed_tests.main.benchmark_cost", side_effect=fake_benchmark
    )

    result = runner.invoke(
        app,
        ["--iterations", "2", "--cost", "10", "--cost", "12"],
    )

    assert result.exit_code == 0
    assert calls == [(10, 2), (12, 2)]
    assert "Iterations per cost: 2" in result.output


def test_cli_rejects_invalid_cost(runner: CliRunner) -> None:
    """Reject invalid cost values outside the allowed range."""
    result = runner.invoke(app, ["--cost", "3"])

    assert result.exit_code != 0
    assert "Usage:" in result.output


def test_cli_rejects_invalid_iterations(runner: CliRunner) -> None:
    """Reject iterations below the minimum bound."""
    result = runner.invoke(app, ["--iterations", "0"])

    assert result.exit_code != 0
    assert "Usage:" in result.output
