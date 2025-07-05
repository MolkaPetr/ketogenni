#!/usr/bin/env python3
"""Utility to compute macronutrient ratios.

This script can either compute the ratio of fats, carbohydrates and proteins
from given gram amounts or determine the required grams of each macronutrient
for a target total weight given the desired ratio.

Usage examples:
    python macro_ratio_calculator.py ratio --fats 80 --carbs 10 --proteins 30
    python macro_ratio_calculator.py grams --weight 120 --fats 0.7 --carbs 0.05 --proteins 0.25

"""

import argparse
from typing import Tuple


def compute_ratio(fats: float, carbs: float, proteins: float) -> Tuple[float, float, float]:
    """Return the ratio of each macronutrient given the grams of each."""
    total = fats + carbs + proteins
    if total == 0:
        raise ValueError("Total weight of macros must be greater than zero")
    return fats / total, carbs / total, proteins / total


def compute_grams(weight: float, fats_ratio: float, carbs_ratio: float, proteins_ratio: float) -> Tuple[float, float, float]:
    """Compute grams of each macro given the target total weight and ratios."""
    total_ratio = fats_ratio + carbs_ratio + proteins_ratio
    if total_ratio == 0:
        raise ValueError("Sum of ratios must be greater than zero")
    factor = weight / total_ratio
    return fats_ratio * factor, carbs_ratio * factor, proteins_ratio * factor


def main() -> None:
    parser = argparse.ArgumentParser(description="Calculate macronutrient ratios or grams")
    subparsers = parser.add_subparsers(dest="command", required=True)

    ratio_parser = subparsers.add_parser("ratio", help="Compute ratio from grams")
    ratio_parser.add_argument("--fats", type=float, required=True, help="Grams of fat")
    ratio_parser.add_argument("--carbs", type=float, required=True, help="Grams of carbohydrates")
    ratio_parser.add_argument("--proteins", type=float, required=True, help="Grams of protein")

    grams_parser = subparsers.add_parser("grams", help="Compute grams from ratio and total weight")
    grams_parser.add_argument("--weight", type=float, required=True, help="Target total weight (grams)")
    grams_parser.add_argument("--fats", type=float, required=True, help="Fats ratio (e.g. 0.7 for 70%)")
    grams_parser.add_argument("--carbs", type=float, required=True, help="Carbs ratio")
    grams_parser.add_argument("--proteins", type=float, required=True, help="Proteins ratio")

    args = parser.parse_args()

    if args.command == "ratio":
        ratio = compute_ratio(args.fats, args.carbs, args.proteins)
        print(f"Ratio F:C:P = {ratio[0]:.2f}:{ratio[1]:.2f}:{ratio[2]:.2f}")
    else:
        grams = compute_grams(args.weight, args.fats, args.carbs, args.proteins)
        print(f"Grams F:C:P = {grams[0]:.1f}g:{grams[1]:.1f}g:{grams[2]:.1f}g")


if __name__ == "__main__":
    main()

