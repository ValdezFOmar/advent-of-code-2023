from __future__ import annotations

import functools
from collections import Counter
from dataclasses import dataclass
from enum import IntEnum, auto
from typing import Iterable

from aoc.tools import YieldStr, run_challenge

camel_cards_symbols = ("2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A")
camel_cards: dict[str, int] = {symbol: value for value, symbol in enumerate(camel_cards_symbols)}


# Order matters
class HandType(IntEnum):
    HIGH_CARD = auto()
    ONE_PAIR = auto()
    TWO_PAIR = auto()
    THREE_OF_A_KIND = auto()
    FULL_HOUSE = auto()
    FOUR_OF_A_KIND = auto()
    FIVE_OF_A_KIND = auto()

    @classmethod
    def which_type(cls, cards: str) -> HandType:
        unique_cards = set(cards)
        num_unique_cards = len(unique_cards)

        if num_unique_cards == 1:
            return cls.FIVE_OF_A_KIND
        if num_unique_cards == 2:
            counts = {cards.count(card) for card in unique_cards}
            if 4 in counts:
                return cls.FOUR_OF_A_KIND
            return cls.FULL_HOUSE
        if num_unique_cards == 3:
            counts = {cards.count(card) for card in unique_cards}
            if 3 in counts:
                return cls.THREE_OF_A_KIND
            return cls.TWO_PAIR
        if num_unique_cards == 4:
            return cls.ONE_PAIR
        return cls.HIGH_CARD


@dataclass(frozen=True)
class Hand:
    cards: str
    bid: int
    j_as_wildcard: bool

    @functools.cached_property
    def hand_type(self) -> HandType:
        no_wildcard_hand_type = HandType.which_type(self.cards)
        is_highest_type = no_wildcard_hand_type == HandType.FIVE_OF_A_KIND
        cards_counter = Counter(self.cards)

        if not self.j_as_wildcard or is_highest_type or not cards_counter["J"]:
            return no_wildcard_hand_type

        del cards_counter["J"]
        most_common_card = cards_counter.most_common(1)[0][0]
        cards_with_wildcard = self.cards.replace("J", most_common_card)
        return HandType.which_type(cards_with_wildcard)

    # Implementing __lt__() allows the use of the builtin `sorted()` iterator
    def __lt__(self, __other):
        if not isinstance(__other, type(self)):
            return NotImplemented
        if self.hand_type != __other.hand_type:
            return self.hand_type < __other.hand_type
        for self_card, other_card in zip(self.cards, __other.cards):
            if camel_cards[self_card] == camel_cards[other_card]:
                continue
            return camel_cards[self_card] < camel_cards[other_card]
        return False  # hands are the same


def parse_input(input: YieldStr, j_as_wildcard: bool = False) -> list[Hand]:
    hands: list[Hand] = []
    for line in input:
        cards, bid = line.split()
        hands.append(Hand(cards, int(bid), j_as_wildcard))
    return hands


def total_winnings(hands: Iterable[Hand]):
    return sum(rank * hand.bid for rank, hand in enumerate(sorted(hands), 1))


def solution_part_1(input: YieldStr) -> int:
    hands = parse_input(input)
    output = total_winnings(hands)
    return output


def solution_part_2(input: YieldStr) -> int:
    camel_cards["J"] = -1  # Make J the weakest card
    hands = parse_input(input, j_as_wildcard=True)
    output = total_winnings(hands)
    return output


if __name__ == "__main__":
    run_challenge(solution_part_2, relative_to=__file__, debug=True)
