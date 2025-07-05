# Macronutrient Ratio Calculator

This repository contains a small script to help compute ratios of fats,
carbohydrates and proteins. The script can either determine the ratio from
provided gram values or calculate the required grams of each macronutrient for a
specific total weight based on a desired ratio.

## Usage

Install Python 3 and run the script in one of the two modes:

### Calculate ratio from gram amounts
```
python macro_ratio_calculator.py ratio --fats 80 --carbs 10 --proteins 30
```
This prints the fraction of each macronutrient.

### Calculate grams from a target ratio
```
python macro_ratio_calculator.py grams --weight 120 --fats 0.7 --carbs 0.05 --proteins 0.25
```
This calculates how many grams of fats, carbohydrates and proteins are needed so
that their ratio matches the specified values and the total weight equals the
given weight.
