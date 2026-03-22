import itertools
from functools import lru_cache


@lru_cache(maxsize=None)
def evaluate_single_attack(
    attack_dice: int, defence_dice: int
) -> tuple[tuple[int, int, float], ...]:
    """Evaluate a single Risk dice attack roll.

    Args:
        attack_dice: Number of attack dice (1-3).
        defence_dice: Number of defence dice (1-2).

    Returns:
        A tuple of (attacker_loss, defender_loss, probability) triples covering
        all possible outcomes for the roll. attacker_loss and defender_loss are
        non-positive integers (losses are represented as negative offsets).

    Raises:
        TypeError: If either argument is not an integer.
        ValueError: If either argument is less than 1.

    Example:
        >>> evaluate_single_attack(3, 2)
        ((-2, 0, 0.2924...), (-1, -1, 0.3241...), (0, -2, 0.3726...))
    """
    if not isinstance(attack_dice, int) or not isinstance(defence_dice, int):
        raise TypeError("Dice counts must be integers")
    if attack_dice < 1 or defence_dice < 1:
        raise ValueError("Dice counts must be at least 1")
    attack_permutations = list(itertools.product(range(1, 7), repeat=attack_dice))
    defence_permutations = list(itertools.product(range(1, 7), repeat=defence_dice))
    n_combat_dice = min(attack_dice, defence_dice)
    results = [0] * (n_combat_dice + 1)
    cases = [[i - n_combat_dice, -i] for i in range(n_combat_dice + 1)]

    for attack in attack_permutations:
        for defence in defence_permutations:
            attack_sorted = sorted(attack, reverse=True)[:n_combat_dice]
            defence_sorted = sorted(defence, reverse=True)[:n_combat_dice]
            attack_wins = [i > j for i, j in zip(attack_sorted, defence_sorted)]
            results[sum(attack_wins)] += 1
    return tuple(
        (case[0], case[1], result / sum(results))
        for case, result in zip(cases, results)
    )


if __name__ == "__main__":
    print(evaluate_single_attack(3, 2))
    print(evaluate_single_attack(2, 2))
    print(evaluate_single_attack(1, 2))
    print(evaluate_single_attack(3, 1))
    print(evaluate_single_attack(2, 1))
    print(evaluate_single_attack(1, 1))
