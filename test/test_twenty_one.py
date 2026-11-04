import pytest

from card_game.card.game.TwentyOne.TwentyOne import score_hand


# test cases as fixture I assume
def test_standard_hand(hand: list[str]) -> None:
    ...