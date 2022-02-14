from functools import lru_cache

from single_attack import evaluate_single_attack


@lru_cache
def evaluate_multiple_attack(attack_troops: int, defence_troops: int) -> dict:
    """Evaluate a Risk battle to it's conclusion."""
    result = {}
    single_roll = evaluate_single_attack(min(attack_troops, 3), min(defence_troops, 2))
    for attackers_lost, defenders_lost, roll_prob in single_roll:
        attack_troops_final = attack_troops + attackers_lost
        defence_troops_final = defence_troops + defenders_lost
        if attack_troops_final == 0 or defence_troops_final == 0:
            result[(attack_troops_final, defence_troops_final)] = roll_prob
        else:
            for final_state, branch_prob in evaluate_multiple_attack(
                attack_troops_final, defence_troops_final
            ).items():
                if final_state not in result:
                    result[final_state] = 0
                result[final_state] += branch_prob * roll_prob
    return result


def evaluate_attacker_winning(attack_troops: int, defence_troops: int) -> float:
    """Evaluate the probability of an attacker winning a Risk battle."""
    result = evaluate_multiple_attack(attack_troops, defence_troops)
    attack_win_prob = 0
    for i, j in result.items():
        if i[1] == 0:
            attack_win_prob += j
    return attack_win_prob


if __name__ == "__main__":
    probs = [
        [evaluate_attacker_winning(i, j) for i in range(1, 11)] for j in range(1, 11)
    ]
    probs_formatted = [[f"{val*100:5.2f}%" for val in row] for row in probs]
    print("Attacker win probability:")
    print("                                              Attack troops")
    print("".join(x for x in [f"{i:8.0f}  " for i in range(1, 11)]))
    for row in probs_formatted:
        print(row)
