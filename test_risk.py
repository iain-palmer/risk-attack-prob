import pytest

from single_attack import evaluate_single_attack
from multiple_attack import evaluate_multiple_attack, evaluate_attacker_winning


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _total_prob(outcomes):
    """Sum probabilities from evaluate_single_attack results."""
    return sum(p for _, _, p in outcomes)


# ---------------------------------------------------------------------------
# single_attack tests
# ---------------------------------------------------------------------------

class TestEvaluateSingleAttack:
    def test_probabilities_sum_to_one(self):
        for a in range(1, 4):
            for d in range(1, 3):
                total = _total_prob(evaluate_single_attack(a, d))
                assert abs(total - 1.0) < 1e-9, f"a={a} d={d}: prob sum={total}"

    def test_known_1v1(self):
        # Attacker wins 15/36, ties go to defender
        outcomes = {(a, d): p for a, d, p in evaluate_single_attack(1, 1)}
        assert abs(outcomes[(-1, 0)] - 21 / 36) < 1e-9   # defender wins
        assert abs(outcomes[(0, -1)] - 15 / 36) < 1e-9   # attacker wins

    def test_known_3v2_win_prob(self):
        # Standard Risk 3v2 probabilities (out of 7776 total permutations)
        outcomes = {(a, d): p for a, d, p in evaluate_single_attack(3, 2)}
        # (-2, 0): defender wins both dice
        assert abs(outcomes[(-2, 0)] - 2275 / 7776) < 1e-9
        # (-1, -1): each loses one
        assert abs(outcomes[(-1, -1)] - 2611 / 7776) < 1e-9
        # (0, -2): attacker wins both dice
        assert abs(outcomes[(0, -2)] - 2890 / 7776) < 1e-9

    def test_outcome_structure(self):
        outcomes = evaluate_single_attack(2, 1)
        for attacker_loss, defender_loss, prob in outcomes:
            assert attacker_loss <= 0
            assert defender_loss <= 0
            assert 0.0 <= prob <= 1.0

    def test_returns_tuple(self):
        result = evaluate_single_attack(1, 1)
        assert isinstance(result, tuple)
        for item in result:
            assert isinstance(item, tuple)
            assert len(item) == 3

    def test_type_error_on_float(self):
        # Use 1.5 — lru_cache treats 1.0 and 1 as the same key (equal hash),
        # so 1.5 is needed to actually trigger validation.
        with pytest.raises(TypeError):
            evaluate_single_attack(1.5, 1)
        with pytest.raises(TypeError):
            evaluate_single_attack(1, 1.5)

    def test_value_error_on_zero(self):
        with pytest.raises(ValueError):
            evaluate_single_attack(0, 1)
        with pytest.raises(ValueError):
            evaluate_single_attack(1, 0)

    def test_value_error_on_negative(self):
        with pytest.raises(ValueError):
            evaluate_single_attack(-1, 1)
        with pytest.raises(ValueError):
            evaluate_single_attack(1, -1)


# ---------------------------------------------------------------------------
# multiple_attack tests
# ---------------------------------------------------------------------------

class TestEvaluateMultipleAttack:
    def test_probabilities_sum_to_one(self):
        for a in range(1, 6):
            for d in range(1, 6):
                total = sum(evaluate_multiple_attack(a, d).values())
                assert abs(total - 1.0) < 1e-9, f"a={a} d={d}: prob sum={total}"

    def test_all_outcomes_are_terminal(self):
        for a in range(1, 5):
            for d in range(1, 5):
                for state in evaluate_multiple_attack(a, d):
                    assert state[0] == 0 or state[1] == 0

    def test_type_error_on_float(self):
        with pytest.raises(TypeError):
            evaluate_multiple_attack(1.5, 1)
        with pytest.raises(TypeError):
            evaluate_multiple_attack(1, 1.5)

    def test_value_error_on_zero(self):
        with pytest.raises(ValueError):
            evaluate_multiple_attack(0, 1)
        with pytest.raises(ValueError):
            evaluate_multiple_attack(1, 0)

    def test_value_error_on_negative(self):
        with pytest.raises(ValueError):
            evaluate_multiple_attack(-1, 1)


# ---------------------------------------------------------------------------
# evaluate_attacker_winning tests
# ---------------------------------------------------------------------------

class TestEvaluateAttackerWinning:
    # Reference values from README table
    README_TABLE = {
        (1, 1): 0.4167, (2, 1): 0.7542, (3, 1): 0.9164,
        (1, 2): 0.1061, (2, 2): 0.3627, (3, 2): 0.6560,
        (3, 3): 0.4703,
        (10, 1): 1.0000, (1, 10): 0.0000,
    }

    @pytest.mark.parametrize("troops,expected", README_TABLE.items())
    def test_known_probabilities(self, troops, expected):
        attack, defence = troops
        result = evaluate_attacker_winning(attack, defence)
        assert abs(result - expected) < 0.001, (
            f"a={attack} d={defence}: expected ~{expected}, got {result:.4f}"
        )

    def test_returns_float(self):
        result = evaluate_attacker_winning(2, 2)
        assert isinstance(result, float)

    def test_probability_in_range(self):
        for a in range(1, 6):
            for d in range(1, 6):
                p = evaluate_attacker_winning(a, d)
                assert 0.0 <= p <= 1.0

    def test_more_attackers_higher_prob(self):
        # Adding attackers should not decrease win probability
        d = 3
        probs = [evaluate_attacker_winning(a, d) for a in range(1, 8)]
        assert probs == sorted(probs)

    def test_type_error_on_float(self):
        with pytest.raises(TypeError):
            evaluate_attacker_winning(1.5, 1)

    def test_value_error_on_zero(self):
        with pytest.raises(ValueError):
            evaluate_attacker_winning(0, 1)
