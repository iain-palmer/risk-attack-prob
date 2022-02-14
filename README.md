# risk-attack-prob
Calculation of attack probabilities for the game 'Risk'.

The modules here calculate probabilities by considering the tree of all possible dice roll permutations and individual attack outcomes.

As such, the probabilities calculated using these modules are exact (subject to the limitations of floating point arithmetic).

`single_attack.py` provides a function which evaluates the possible outcomes (and associated probabilities) for a single Risk combat.

`multiple_attack.py` provides functions which evaluate a Risk battle to its completion (win/loss for the attacker).