import pytest

from card_game.card.game.TwentyOne.TwentyOne import score_hand
from card_game.card.entity.Card import ace, get_face_card_score


@pytest.fixture(
    params=[
        ["S7", "H8"],  # standard hand
        ["SA", "HK"],  # blackjack (21)
        ["SA", "H5"],  # ace counts as 11
        ["SA", "HK", "DQ"],  # ace adjusted to 1
        ["SA", "HK", "DQ", "C2"],  # bust even after ace adjustment
        ["SA", "HA", "D9"],  # multiple aces
        ["S7", "H7", "D7"],  # exactly 21
    ]
)
def hand(request):
    return request.param


def test_standard_hand(hand: list[str]) -> None:
    if any(card[1] == ace for card in hand):
        pytest.skip("no ace")

    score = score_hand(hand)
    _score = sum(get_face_card_score(card) for card in hand)
    assert score == _score


def test_ace_as_high_value(hand: list[str]) -> None:
    if all(card[1] != ace for card in hand):
        pytest.skip("ace required")

    _score = sum(get_face_card_score(card) for card in hand)
    if _score <= 21:
        assert score_hand(hand) == _score


def test_ace_adjusted_to_low_value(hand: list[str]) -> None:
    if all(card[1] != ace for card in hand):
        pytest.skip("ace required")

    _score = sum(get_face_card_score(card) for card in hand)
    if _score > 21:
        correct_score = sum(1 if card[1] == ace else get_face_card_score(card) for card in hand)
        assert score_hand(hand) == correct_score


def test_bust_hand(hand: list[str]) -> None:
    _score = sum(get_face_card_score(card) for card in hand)
    if _score > 21:
        _score = sum(1 if card[1] == ace else get_face_card_score(card) for card in hand)

    if _score > 21:
        assert score_hand(hand) == 0


@pytest.mark.parametrize(
    ("hand", "expected_score"),
    [
        # Empty hand
        ([], 0),
        # Natural 21 (Ace + 10-value card)
        (["SA", "SK"], 21),
        # Hand exceeding 21 even after reducing Ace to 1
        (["SA", "SK", "HQ", "D2"], 0),
        # Multiple Aces in hand
        (["SA", "HA", "D9"], 21),
        # Exact 21 with multiple low cards
        (["S7", "H7", "D7"], 21),
    ],
)
def test_score_hand_combinations(
    hand: list[str],
    expected_score: int,
) -> None:
    assert score_hand(hand) == expected_score
