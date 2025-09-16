# Kalkulačka

Tento repozitář obsahuje jednoduchou kalkulačku v Pythonu. Výrazy jsou
vyhodnocovány bezpečně pomocí modulu `ast` a kromě základních operací je možné
využít i funkce `abs` a `round`.

## Požadavky

* Python 3.11 (nebo novější verze řady 3.x)

## Spuštění z příkazové řádky

```bash
python -m calculator "2 + 3 * 4"
```

Výsledek je vypsán na standardní výstup. Pomocí přepínače `--decimals` lze
nechat výsledek zaokrouhlit na zadaný počet desetinných míst:

```bash
python -m calculator "10 / 3" --decimals 2
```

Bez uvedení výrazu se kalkulačka spustí v interaktivním režimu, ve kterém
zpracovává výrazy po jednotlivých řádcích. Režim je možné vyvolat i explicitně
pomocí přepínače `--interactive`.

```bash
python -m calculator --interactive
```

Výraz je možné předat také přes standardní vstup, například při použití roury:

```bash
echo "(5 + 3) * 2" | python -m calculator
```

## Použití v Pythonu

```python
from calculator import Calculator

calc = Calculator()
print(calc.evaluate("(5 + 3) ** 2"))
```

## Testy

Testy spustíte příkazem:

```bash
pytest
```
