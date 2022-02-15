# risk-attack-prob
Calculation of attack probabilities for the game 'Risk'.

The modules here calculate probabilities by considering a directed acyclic graph representing all possible dice roll permutations and individual attack outcomes.

As such, the probabilities calculated using these modules are exact (subject to the limitations of floating point arithmetic).

`single_attack.py` provides a function which evaluates the possible outcomes (and associated probabilities) for a single Risk combat.

`multiple_attack.py` provides functions which evaluate a Risk battle to its completion (win/loss for the attacker).

The table below provides attacker win probabilities for battles involving up to 10 troops on either side, calculated using these modules. 

| Attackers/Defenders | 1      | 2      | 3      | 4      | 5      | 6      | 7      | 8      | 9      | 10      |
| ------------------- | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------- |
| 1                   | 41.67% | 75.42% | 91.64% | 97.15% | 99.03% | 99.67% | 99.89% | 99.96% | 99.99% | 100.00% |
| 2                   | 10.61% | 36.27% | 65.60% | 78.55% | 88.98% | 93.40% | 96.66% | 98.03% | 99.01% | 99.42%  |
| 3                   | 2.70%  | 20.61% | 47.03% | 64.16% | 76.94% | 85.69% | 90.99% | 94.68% | 96.70% | 98.11%  |
| 4                   | 0.69%  | 9.13%  | 31.50% | 47.65% | 63.83% | 74.49% | 83.37% | 88.78% | 92.98% | 95.39%  |
| 5                   | 0.18%  | 4.91%  | 20.59% | 35.86% | 50.62% | 63.77% | 73.64% | 81.84% | 87.29% | 91.63%  |
| 6                   | 0.04%  | 2.14%  | 13.37% | 25.25% | 39.68% | 52.07% | 64.01% | 72.96% | 80.76% | 86.11%  |
| 7                   | 0.01%  | 1.13%  | 8.37%  | 18.15% | 29.74% | 42.33% | 53.55% | 64.29% | 72.61% | 79.98%  |
| 8                   | 0.00%  | 0.49%  | 5.35%  | 12.34% | 22.40% | 32.95% | 44.56% | 54.74% | 64.64% | 72.40%  |
| 8                   | 0.00%  | 0.26%  | 3.28%  | 8.62%  | 16.16% | 25.78% | 35.69% | 46.40% | 55.81% | 65.01%  |
| 10                  | 0.00%  | 0.11%  | 2.08%  | 5.72%  | 11.83% | 19.34% | 28.68% | 37.99% | 47.99% | 56.76%  |