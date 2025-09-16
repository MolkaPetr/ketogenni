import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import io

import pytest

from calculator import Calculator, main


@pytest.fixture
def calculator() -> Calculator:
    return Calculator()


def test_basic_arithmetic(calculator: Calculator) -> None:
    assert calculator.evaluate("2 + 3 * 4") == 14


def test_parentheses_and_power(calculator: Calculator) -> None:
    assert calculator.evaluate("(2 + 3) ** 2") == 25


def test_unary_operations(calculator: Calculator) -> None:
    assert calculator.evaluate("-5 + +2") == -3


def test_division_by_zero(calculator: Calculator) -> None:
    with pytest.raises(ZeroDivisionError):
        calculator.evaluate("10 / 0")


def test_abs_function(calculator: Calculator) -> None:
    assert calculator.evaluate("abs(-7)") == 7


def test_round_function(calculator: Calculator) -> None:
    assert calculator.evaluate("round(10 / 3, 2)") == round(10 / 3, 2)


def test_invalid_function(calculator: Calculator) -> None:
    with pytest.raises(ValueError):
        calculator.evaluate("pow(2, 3)")


def test_invalid_expression(calculator: Calculator) -> None:
    with pytest.raises(ValueError):
        calculator.evaluate("")


def test_cli_evaluates_expression(capsys) -> None:
    main(["2 + 2"])
    captured = capsys.readouterr()
    assert captured.out.strip() == "4"


def test_cli_reads_from_stdin(monkeypatch, capsys) -> None:
    class FakeInput(io.StringIO):
        def isatty(self) -> bool:  # pragma: no cover - simple helper
            return False

    fake_stdin = FakeInput("3 * 3")
    monkeypatch.setattr("sys.stdin", fake_stdin)

    main([])

    captured = capsys.readouterr()
    assert captured.out.strip() == "9"


def test_cli_interactive_mode(monkeypatch, capsys) -> None:
    responses = iter(["2 + 3", "quit"])

    def fake_input(prompt: str = "") -> str:
        print(prompt, end="")
        return next(responses)

    monkeypatch.setattr("builtins.input", fake_input)

    main(["--interactive"])

    captured = capsys.readouterr()

    assert "Interaktivní režim" in captured.out
    assert "5" in captured.out.split()
