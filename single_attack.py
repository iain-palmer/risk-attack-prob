import itertools
from functools import lru_cache


@lru_cache(maxsize=None)
def evaluate_single_attack(
    attack_dice: int, defence_dice: int
) -> tuple[tuple[int, int, float], ...]:
    """Evaluate a single Risk dice attack roll."""
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
            defence_sorted = sorted(defence)[:n_combat_dice]
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
