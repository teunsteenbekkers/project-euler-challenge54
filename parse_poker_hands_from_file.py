# Define the classes we use
from enum import Enum
from pathlib import Path


class Suit(Enum):
    HEARTS = 'H'
    DIAMONDS = 'D'
    CLUBS = 'C'
    SPADES = 'S'


class Card:
    def __init__(self, card_id):
        self.id = card_id
        suit_id = card_id[len(card_id)-1]
        value_id = card_id[0:len(card_id)-1]
        self.suit = Suit(suit_id)
        self.value = self.value_id_to_int(value_id)

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
        suit_name = Card.get_suit_name(card.suit)
        return '{} of {}'.format(value_name, suit_name)

    @staticmethod
    def get_value_name(value):
        switcher = {
            11: 'Jack',
            12: 'Queen',
            13: 'King',
            14: 'Ace'
        }

        return switcher.get(value, str(value))

    @staticmethod
    def get_suit_name(suit):
        return str(suit.name.capitalize())


class Hand:
    def __init__(self, card_ids):
        self.cards = []
        for card_id in card_ids:
            card = Card(card_id)
            self.cards.append(card)
        self.index = len(self.cards)

        # Sort the cards by value
        self.cards.sort(key=lambda card: card.value, reverse=True)

        # Print the cards' names
        print(list(map(lambda card: Card.get_card_name(card), self.cards)))

        self.has_pair_of_any_kind()

    def has_pair_of_any_kind(self):
        from itertools import groupby

        # User itertools to group the cards by their value (2 to Ace)
        card_values = map(lambda card: card.value, self.cards)
        cards_grouped_by_value = groupby(
            iterable=card_values, key=lambda value: value)

        # Define the function used to map the cards grouped by value to tuples of the format (card_value, number_of_cards_in_group)
        def map_function(data):
            card_value, group_of_cards = data
            number_of_cards_in_group = len(list(group_of_cards))
            # print("Number of cards with value of {}: {}".format(
            #     card_value, number_of_cards_in_group))
            return (card_value, number_of_cards_in_group)

        # Map the grouped cards to tuples
        number_of_cards_per_unique_value = list(map(
            map_function, cards_grouped_by_value))

        # Remove the tuples for card groups with only 1 card
        card_groups = list(filter(
            lambda group_of_cards: group_of_cards[1] > 1, number_of_cards_per_unique_value))

        # Sort card groups by size (we want the biggest group first for a Full House)
        card_groups.sort(key=lambda card_group: card_group[1], reverse=True)

        # Determine the number of unique values in this hand
        # 0 means no card values appear more than once (no Pairs, Three of a Kind or Four of a Kind)
        number_of_card_groups = len(card_groups)
        if number_of_card_groups < 1:
            return False
        else:
            # Since we sorted the card groups by the number of cards they contain, the first card group is the biggest
            biggest_group = card_groups[0]
            biggest_group_count = biggest_group[1]

            # Determine what kind of hand (group wise) we're dealing with
            # Possibilities: One Pair, Two Pairs, Three of a Kind, Full House, Four of a Kind or none of those

            # 1 means one card value appears more than once: One Pair, Three of a Kind or Four of a Kind
            if number_of_card_groups == 1:
                # Determine which kind of card group this hand has
                if biggest_group_count == 2:
                    print('One pair: {}'.format(
                        Card.get_value_name(biggest_group[0])))
                elif biggest_group_count == 3:
                    print('Three of a kind: {}'.format(
                        Card.get_value_name(biggest_group[0])))
                elif biggest_group_count == 4:
                    print('Four of a kind: {}'.format(
                        Card.get_value_name(biggest_group[0])))
            # 2 means two card values appear more than once: Two Pairs or a Full House
            else:
                # Determine which kind of card groups this hand has
                if biggest_group_count == 2:
                    print('Two pairs: {} and {}'.format(
                        Card.get_value_name(card_groups[0][0]), Card.get_value_name(card_groups[1][0])))
                elif biggest_group_count == 3:
                    print('Full House: {} (biggest group) and {} (smallest group)'.format(
                        Card.get_value_name(card_groups[0][0]), Card.get_value_name(card_groups[1][0])))


# Parses a line of ten cards separated by spaces into the hands for two players
def parse_player_hands_from_line(line):
    cards = line.split(' ')
    player_one_cards = cards[0:5]
    player_two_cards = cards[5:10]
    print("\nPlayer 1 Hand:")
    player_one_hand = Hand(player_one_cards)
    print("\nPlayer 2 Hand:")
    player_two_hand = Hand(player_two_cards)


# Relative paths are always resolved from the current working directory
# Therefore we need to resolve the text file's path using this file's path
file_path = './p054_poker_custom.txt'
# file_path = './p054_poker.txt'
base_path = Path(__file__).parent
file_path = (base_path / file_path).resolve()

# Read the text file containing the poker hands for two players
with open(file_path, 'r') as file:
    # Get the contents of the file as text
    file_contents = file.read()

    # Every line contains ten cards (five for player one and five for player two)
    # We split the string into lines
    poker_hand_lines = file_contents.splitlines()

    # Parse both players' hands from each line
    for line in poker_hand_lines:
        parse_player_hands_from_line(line)
