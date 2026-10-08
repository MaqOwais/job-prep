"""
🟡 Deck of Cards — generic deck + Blackjack specialization.

Primer: https://github.com/donnemartin/system-design-primer/blob/master/solutions/object_oriented_design/deck_of_cards/deck_of_cards.ipynb

Talking points:
  - Generic Card/Deck/Hand classes reusable across games (Open/Closed principle)
  - BlackjackCard overrides value (face cards = 10, ace = 1 or 11)
  - BlackjackHand computes the best score <= 21 handling multiple aces
"""
from __future__ import annotations

import random
from enum import Enum


class Suit(Enum):
    HEARTS = "♥"
    DIAMONDS = "♦"
    CLUBS = "♣"
    SPADES = "♠"


class Card:
    def __init__(self, rank: int, suit: Suit):  # rank 1 (Ace) .. 13 (King)
        self.rank, self.suit = rank, suit

    @property
    def value(self) -> int:
        return self.rank

    def __repr__(self):
        names = {1: "A", 11: "J", 12: "Q", 13: "K"}
        return f"{names.get(self.rank, self.rank)}{self.suit.value}"


class BlackjackCard(Card):
    @property
    def value(self) -> int:
        return 10 if self.rank >= 10 else self.rank  # ace counted as 1 here

    @property
    def is_ace(self) -> bool:
        return self.rank == 1


class Deck:
    def __init__(self, card_cls=Card, seed: int | None = None):
        self.cards = [card_cls(r, s) for s in Suit for r in range(1, 14)]
        self._rng = random.Random(seed)

    def shuffle(self) -> None:
        self._rng.shuffle(self.cards)

    def deal(self) -> Card:
        if not self.cards:
            raise IndexError("deck is empty")
        return self.cards.pop()

    def __len__(self):
        return len(self.cards)


class Hand:
    def __init__(self):
        self.cards: list[Card] = []

    def add(self, card: Card) -> None:
        self.cards.append(card)

    def score(self) -> int:
        return sum(c.value for c in self.cards)


class BlackjackHand(Hand):
    def score(self) -> int:
        total = sum(c.value for c in self.cards)
        aces = sum(1 for c in self.cards if c.is_ace)
        while aces and total + 10 <= 21:  # upgrade an ace from 1 to 11 if it helps
            total += 10
            aces -= 1
        return total

    def is_bust(self) -> bool:
        return self.score() > 21

    def is_blackjack(self) -> bool:
        return len(self.cards) == 2 and self.score() == 21


if __name__ == "__main__":
    d = Deck(BlackjackCard, seed=1)
    assert len(d) == 52
    d.shuffle()
    h = BlackjackHand()
    h.add(BlackjackCard(1, Suit.SPADES))
    h.add(BlackjackCard(13, Suit.HEARTS))
    assert h.score() == 21 and h.is_blackjack()
    h2 = BlackjackHand()
    for r in (1, 1, 9):
        h2.add(BlackjackCard(r, Suit.CLUBS))
    assert h2.score() == 21  # 11 + 1 + 9
    h2.add(BlackjackCard(5, Suit.CLUBS))
    assert h2.score() == 16  # both aces as 1
    print("✅ Deck of cards tests passed")
