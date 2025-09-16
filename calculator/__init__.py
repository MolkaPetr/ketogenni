"""Simple expression-based calculator.

This module defines a :class:`Calculator` capable of evaluating arithmetic
expressions composed of numbers, the operators ``+``, ``-``, ``*``, ``/``,
``//``, ``%``, and ``**``, as well as parentheses and selected built-in
functions. A small command-line interface is provided for convenience.
"""
from __future__ import annotations

import argparse
import ast
import operator
import sys
from typing import Callable, Dict, List, Optional, Union

Number = Union[int, float]


class Calculator:
    """Evaluate arithmetic expressions in a controlled manner.

    The implementation parses expressions using :mod:`ast` and evaluates only
    a curated subset of Python's syntax tree nodes. This keeps evaluation
    deterministic and avoids arbitrary code execution while still supporting a
    handy set of arithmetic features.
    """

    _BINARY_OPERATORS: Dict[type, Callable[[Number, Number], Number]] = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
    }

    _UNARY_OPERATORS: Dict[type, Callable[[Number], Number]] = {
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
    }

    _ALLOWED_FUNCTIONS: Dict[str, Callable[..., Number]] = {
        "abs": abs,
        "round": round,
    }

    def evaluate(self, expression: str) -> Number:
        """Evaluate *expression* and return the resulting number.

        Args:
            expression: The arithmetic expression to evaluate.

        Returns:
            The numeric result of the expression.

        Raises:
            ValueError: If the expression is empty or contains unsupported
                syntax.
            ZeroDivisionError: If a division by zero is attempted.
        """

        cleaned = expression.strip()
        if not cleaned:
            raise ValueError("Expression must not be empty.")

        try:
            parsed = ast.parse(cleaned, mode="eval")
        except SyntaxError as exc:  # pragma: no cover - defensive guard
            raise ValueError("Invalid expression.") from exc

        return self._evaluate_node(parsed.body)

    def _evaluate_node(self, node: ast.AST) -> Number:
        if isinstance(node, ast.BinOp):
            return self._evaluate_binop(node)
        if isinstance(node, ast.UnaryOp):
            return self._evaluate_unaryop(node)
        if isinstance(node, ast.Call):
            return self._evaluate_call(node)
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError(f"Unsupported constant: {node.value!r}")
        if isinstance(node, ast.Num):  # pragma: no cover - Python <3.8
            if isinstance(node.n, (int, float)):
                return node.n
            raise ValueError(f"Unsupported number: {node.n!r}")
        if isinstance(node, ast.Expression):
            return self._evaluate_node(node.body)

        raise ValueError(f"Unsupported expression component: {ast.dump(node)}")

    def _evaluate_binop(self, node: ast.BinOp) -> Number:
        operator_type = type(node.op)
        if operator_type not in self._BINARY_OPERATORS:
            raise ValueError(f"Unsupported operator: {operator_type.__name__}")

        left = self._evaluate_node(node.left)
        right = self._evaluate_node(node.right)

        if operator_type in {ast.Div, ast.FloorDiv, ast.Mod} and right == 0:
            raise ZeroDivisionError("Division by zero is not allowed.")

        operation = self._BINARY_OPERATORS[operator_type]
        return operation(left, right)

    def _evaluate_unaryop(self, node: ast.UnaryOp) -> Number:
        operator_type = type(node.op)
        if operator_type not in self._UNARY_OPERATORS:
            raise ValueError(f"Unsupported unary operator: {operator_type.__name__}")

        operand = self._evaluate_node(node.operand)
        operation = self._UNARY_OPERATORS[operator_type]
        return operation(operand)

    def _evaluate_call(self, node: ast.Call) -> Number:
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only direct function calls are supported.")

        name = node.func.id
        if name not in self._ALLOWED_FUNCTIONS:
            raise ValueError(f"Function '{name}' is not allowed.")

        function = self._ALLOWED_FUNCTIONS[name]
        args = [self._evaluate_node(arg) for arg in node.args]
        kwargs = {kw.arg: self._evaluate_node(kw.value) for kw in node.keywords}

        try:
            return function(*args, **kwargs)
        except TypeError as exc:  # pragma: no cover - delegated error handling
            raise ValueError(str(exc)) from exc


def _emit_result(result: Number, decimals: Optional[int]) -> None:
    if decimals is not None:
        result = round(result, decimals)
    print(result)


def _run_repl(calculator: Calculator, decimals: Optional[int]) -> None:
    print("Interaktivní režim. Ukončete příkazem 'exit'/'quit' nebo Ctrl-D.")
    while True:
        try:
            expression = input(">>> ")
        except EOFError:
            print()
            break

        cleaned = expression.strip()
        if not cleaned:
            continue
        if cleaned.lower() in {"exit", "quit"}:
            break

        try:
            result = calculator.evaluate(cleaned)
        except Exception as exc:  # pragma: no cover - reported to the user
            print(f"Chyba: {exc}")
            continue

        _emit_result(result, decimals)


def main(argv: Optional[List[str]] = None) -> None:
    """Run the calculator's command-line interface."""

    parser = argparse.ArgumentParser(description="Evaluate a mathematical expression.")
    parser.add_argument(
        "expression",
        nargs="?",
        default=None,
        help=(
            "Expression to evaluate. Surround it with quotes to avoid shell interpretation. "
            "Omit it or use --interactive to start the REPL."
        ),
    )
    parser.add_argument(
        "-d",
        "--decimals",
        type=int,
        default=None,
        help="Round the result to the specified number of decimal places.",
    )
    parser.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        help="Start the calculator in interactive mode.",
    )

    args = parser.parse_args(argv)

    calculator = Calculator()

    if args.expression is None:
        if args.interactive:
            _run_repl(calculator, args.decimals)
            return

        if not sys.stdin.isatty():
            streamed = sys.stdin.read().strip()
            if not streamed:
                return
            _emit_result(calculator.evaluate(streamed), args.decimals)
            return

        _run_repl(calculator, args.decimals)
        return

    if args.interactive:
        try:
            result = calculator.evaluate(args.expression)
        except Exception as exc:  # pragma: no cover - delegated to CLI feedback
            print(f"Chyba: {exc}")
        else:
            _emit_result(result, args.decimals)
        _run_repl(calculator, args.decimals)
        return

    result = calculator.evaluate(args.expression)
    _emit_result(result, args.decimals)


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()


__all__ = ["Calculator", "main"]
