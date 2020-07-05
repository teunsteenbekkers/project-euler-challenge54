from enum import Enum
from functools import total_ordering
from itertools import islice
import random


class Suit(Enum):
    HEARTS = 'H'
    DIAMONDS = 'D'
    CLUBS = 'C'
    SPADES = 'S'

    def __str__(self):
        # pylint: disable=no-member
        return self.name.title()

    def get_unicode_character(self):
        character = ''
        if(self.value == 'S'):
            character = '\u2660'
            character = '♠️'
        elif(self.value == 'C'):
            character = '\u2663'
            character = '♣️'
        elif(self.value == 'H'):
            character = '\u2665'
            character = '♥️'
        elif(self.value == 'D'):
            character = '\u2666'
            character = '♦️'

        return character


@total_ordering
class Ranking(Enum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIRS = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9
    ROYAL_FLUSH = 10

    def __str__(self):
        # pylint: disable=no-member
        return self.name.title().replace('_', ' ')

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        return self.value < other.value


class Deck():
    def __init__(self):
        self.cards = []
        self.index = 0
        # Add the 2 to Ace for every suit
        for suit in Suit.__members__.items():
            for i in range(2, 15):
                new_card = Card.from_suit_and_value(suit, i)
                self.cards.append(new_card)

        # Shuffle the deck
        self.shuffle()

        print(str(self))

    def __str__(self):
        return ' '.join(list(map(lambda card: str(card), self.cards)))

    def __iter__(self):
        return iter(self.cards)

    def __next__(self):
        index = self.index
        self.index += 1
        return index

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_hands(self, number_of_hands):
        iterable = iter(self)
        dealt_hands = []
        for i in range(0, number_of_hands):
            # Deal a hand of five
            cards_for_hand = list(islice(iterable, 5))
            card_ids_for_hand = list(map(lambda card: card.id, cards_for_hand))
            hand = Hand(card_ids_for_hand)
            dealt_hands.append(hand)
        return dealt_hands


class Card:
    def __init__(self, card_id):
        self.id = card_id
        suit_id = card_id[len(card_id)-1]
        value_id = card_id[0:len(card_id)-1]
        self.suit = Suit(suit_id)
        self.value = self.value_id_to_int(value_id)

    @classmethod
    def from_suit_and_value(cls, suit, value):
        switcher = {
            10: 'T',
            11: 'J',
            12: 'Q',
            13: 'K',
            14: 'A'
        }
        value_string = str(switcher.get(value, value))
        card_id = '{}{}'.format(value_string, suit[1].value)
        return Card(card_id)

    def __str__(self):
        # return Card.get_card_name(self)
        return "{}{}".format(self.id[0], self.suit.get_unicode_character())

    def value_id_to_int(self, value_id):
        switcher = {
            'T': 10,
            'J': 11,
            'Q': 12,
            'K': 13,
            'A': 14
        }

        # Values from ten to ace are indicated with a letter so we need to turn them into ints
        return int(switcher.get(value_id, value_id))

    @staticmethod
    def get_card_name(card):
        value_name = Card.get_value_name(card.value)
        suit_name = str(card.suit)
        return '{} of {}'.format(value_name, suit_name)

    @staticmethod
    def get_value_name(value):
        switcher = {
            10: '10',
            11: 'Jack',
            12: 'Queen',
            13: 'King',
            14: 'Ace'
        }
        return switcher.get(value, str(value))


@total_ordering
class Hand:
    def __init__(self, card_ids):
        self.cards = []
        for card_id in card_ids:
            card = Card(card_id)
            self.cards.append(card)
        self.index = len(self.cards)
        self.ranking = Ranking.HIGH_CARD

        # Sort the cards by value
        self.cards.sort(key=lambda card: card.value, reverse=True)

        self.ranking = Hand.get_ranking(self)

    def __str__(self):
        cards_string = " ".join(
            list(map(lambda card: "\t{}".format(str(card)), self.cards)))
        return '{}\t({})'.format(cards_string, str(self.ranking))

    def __eq__(self, other):
        return self.ranking == other.ranking and self.get_card_values() == other.get_card_values()

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        if other.ranking != self.ranking:
            return self.ranking < other.ranking
        else:
            # If the hands have the same ranking it means the number of card groups (and their number of cards) are the same
            self_card_groups = self.get_card_value_groups(True)
            if(len(self_card_groups) == 5):
                # No groups, so check the cards for both hands at every index for equality
                for i in range(0, 5):
                    self_value = self.cards[i].value
                    other_value = other.cards[i].value
                    if(self_value != other_value):
                        print('Tiebreaker card: {} vs {}'.format(
                            self_value, other_value))
                        return self_value < other_value
                return False
            else:
                other_card_groups = other.get_card_value_groups(True)

                # If there are groups, find the tiebreaker (if any)
                for i in range(0, len(self_card_groups)):
                    self_group_value = self_card_groups[i][0]
                    other_group_value = other_card_groups[i][0]
                    if(self_group_value != other_group_value):
                        print('Tiebreaker group: {} vs {}'.format(
                            self_group_value, other_group_value))
                        return self_group_value < other_group_value
                return False

    @ staticmethod
    def get_ranking(hand):
        ranking = Ranking.HIGH_CARD

        # If a player has a flush there is no pair in their hand because every card value appears in a deck ONE time for every suit (4)
        is_flush = hand.get_is_flush()

        # If a player has a straight there is no pair in their hand because every card value in a straight is different
        is_straight = hand.get_is_straight()

        if(is_flush == True or is_straight == True):
            if(is_flush == True and is_straight == True):
                if(hand.get_highest_card_value() == 14):
                    ranking = Ranking.ROYAL_FLUSH
                else:
                    ranking = Ranking.STRAIGHT_FLUSH
            else:
                if(is_flush == True):
                    ranking = Ranking.FLUSH

                if(is_straight == True):
                    ranking = Ranking.STRAIGHT
        # We decide the ranking on card groups if the hand is not a flush or a straight
        else:
            card_groups = hand.get_card_value_groups()

            # Determine the number of unique values in this hand
            # 0 means no card values appear more than once (no Pairs, Three of a Kind or Four of a Kind)
            number_of_card_groups = len(card_groups)
            if number_of_card_groups < 1:
                return ranking
            else:
                # Since we sorted the card groups by the number of cards they contain, the first card group is the biggest
                biggest_group = card_groups[0]
                biggest_group_count = len(biggest_group[1])

                # Determine what kind of card group(s) we're dealing with
                # Possibilities: One Pair, Two Pairs, Three of a Kind, Full House, Four of a Kind or none of those

                # 1 means one card value appears more than once: One Pair, Three of a Kind or Four of a Kind
                if number_of_card_groups == 1:
                    # Determine which kind of card group this hand has
                    if biggest_group_count == 2:
                        ranking = Ranking.ONE_PAIR
                    elif biggest_group_count == 3:
                        ranking = Ranking.THREE_OF_A_KIND
                    else:
                        ranking = Ranking.FOUR_OF_A_KIND
                # 2 means two card values appear more than once: Two Pairs or a Full House
                else:
                    # Determine which kind of card groups this hand has
                    if biggest_group_count == 2:
                        ranking = Ranking.TWO_PAIRS
                    elif biggest_group_count == 3:
                        ranking = Ranking.FULL_HOUSE
        return ranking

    def get_set_of_unique_suits(self):
        return set(map(lambda card: card.suit, self.cards))

    def get_is_flush(self):
        return len(self.get_set_of_unique_suits()) == 1

    def get_is_straight(self):
        if len(self.get_card_value_groups()) > 0:
            return False

        return True if self.get_highest_card_value() == self.get_lowest_card_value() + 4 else False

    def get_card_values(self):
        return list(map(lambda card: card.value, self.cards))

    def get_highest_card_value(self):
        return self.get_card_values()[0]

    def get_lowest_card_value(self):
        return self.get_card_values()[-1]

    def get_card_value_groups(self, include_groups_with_one_card=False):
        from itertools import groupby

        # User itertools to group the cards by their value (2 to 14)
        cards_grouped_by_value = []
        for card_value, group in groupby(
                iterable=self.cards, key=lambda card: card.value):
            # Convert the group to a list (because it's an iterator, after this the group will be empty!)
            group_list = list(group)

            # We're only interested in the card values that occur more than once in this hand
            if include_groups_with_one_card or len(group_list) > 1:
                # We want to know how many times a card value occurs, so I generate a tuple containing just that info ;)
                card_group_tuple = (card_value, group_list)
                cards_grouped_by_value.append(card_group_tuple)

        # Sort card groups by size (we want the biggest group first for a Full House)
        cards_grouped_by_value.sort(
            key=lambda card_group: len(card_group[1]), reverse=True)

        return cards_grouped_by_value
