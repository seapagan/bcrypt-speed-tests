"""Unit tests for benchmark helpers."""

import pytest

from bcrypt_speed_tests import benchmark


def test_benchmark_cost_returns_average(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Return the average time and execute the expected iterations."""
    calls = {"count": 0}
    iterations = 3

    def fake_hashpw(_: bytes, __: bytes) -> bytes:
        calls["count"] += 1
        return b"hash"

    monkeypatch.setattr(
        "bcrypt_speed_tests.benchmark.bcrypt.gensalt", lambda **_: b"salt"
    )
    monkeypatch.setattr(
        "bcrypt_speed_tests.benchmark.bcrypt.hashpw", fake_hashpw
    )

    timings = iter([0.0, 0.5, 0.5, 1.0, 1.0, 2.0])
    monkeypatch.setattr(
        "bcrypt_speed_tests.benchmark.time.perf_counter", lambda: next(timings)
    )

    result = benchmark.benchmark_cost(10, iterations)

    assert calls["count"] == iterations
    assert result == pytest.approx(2.0 / 3.0)
