"""CLI integration tests for bcrypt-speed-tests."""

from __future__ import annotations

import importlib

import pytest
from typer.testing import CliRunner

main_module = importlib.import_module("bcrypt_speed_tests.main")


@pytest.fixture
def runner() -> CliRunner:
    """Provide a Typer CLI runner for tests."""
    return CliRunner()


def test_cli_defaults_use_configured_costs(
    runner: CliRunner,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Render the default table using the configured costs."""
    monkeypatch.setattr(main_module, "COSTS", [4, 5])
    monkeypatch.setattr(
        main_module,
        "benchmark_cost",
        lambda cost, _iterations: 0.01 * cost,
    )

    result = runner.invoke(main_module.app, [])

    assert result.exit_code == 0
    assert "Iterations per cost: 3" in result.output
    assert "   4 |" in result.output
    assert "   5 |" in result.output


def test_cli_custom_options_override_defaults(
    runner: CliRunner,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Use CLI options to override costs and iterations."""
    calls: list[tuple[int, int]] = []

    def fake_benchmark(cost: int, iterations: int) -> float:
        calls.append((cost, iterations))
        return 0.001

    monkeypatch.setattr(main_module, "benchmark_cost", fake_benchmark)

    result = runner.invoke(
        main_module.app,
        ["--iterations", "2", "--cost", "10", "--cost", "12"],
    )

    assert result.exit_code == 0
    assert calls == [(10, 2), (12, 2)]
    assert "Iterations per cost: 2" in result.output


def test_cli_rejects_invalid_cost(runner: CliRunner) -> None:
    """Reject invalid cost values outside the allowed range."""
    result = runner.invoke(main_module.app, ["--cost", "3"])

    assert result.exit_code != 0
    assert "Usage:" in result.output


def test_cli_rejects_invalid_iterations(runner: CliRunner) -> None:
    """Reject iterations below the minimum bound."""
    result = runner.invoke(main_module.app, ["--iterations", "0"])

    assert result.exit_code != 0
    assert "Usage:" in result.output


def test_cli_callback_skips_on_subcommand(runner: CliRunner) -> None:
    """Skip the benchmark output when a subcommand is invoked."""

    @main_module.app.command("noop")
    def noop() -> None:
        pass

    result = runner.invoke(main_module.app, ["noop"])

    assert result.exit_code == 0
    assert "Iterations per cost" not in result.output


def test_main_calls_app(monkeypatch: pytest.MonkeyPatch) -> None:
    """Delegate to the Typer app from the entrypoint."""
    called = {"count": 0}

    def fake_app() -> None:
        called["count"] += 1

    monkeypatch.setattr(main_module, "app", fake_app)

    main_module.main()

    assert called["count"] == 1
