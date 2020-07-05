# Define the classes we use
from pathlib import Path
from poker import Hand, Deck


def determine_winner(hands):
    winner = None
    if not all(hand == hands[0] for hand in hands):
        winner_index = hands.index(max(hands))
    print('Winner: Hand {}'.format(winner_index + 1))

# Parses a line of ten cards separated by spaces into the hands for two players


def parse_player_hands_from_line(line):
    cards = line.split(' ')
    # For every chunk of 5 cards (a player's hand)
    chunk_size = 5
    player_hands = []
    player_number = 1
    for i in range(0, len(cards), chunk_size):
        player_hand = Hand(cards[i:i+chunk_size])
        print("Player {} Hand: {}".format(
            player_number, str(player_hand)))
        player_hands.append(player_hand)
        player_number += 1

    # Determine the winner
    determine_winner(player_hands)


deck = Deck()


def determine_winner_for_hands_from_deck():
    deck.shuffle()
    player_hands = deck.deal_hands(2)

    print(str(player_hands[0]))
    print(str(player_hands[1]))

    # Determine the winner
    determine_winner(player_hands)


def determine_winner_for_hands_from_file():
    # Relative paths are always resolved from the current working directory
    # Therefore we need to resolve the text file's path using this file's path
    # file_path = './p054_poker_groups.txt'
    # file_path = './p054_poker_suits.txt'
    file_path = './p054_poker_tiebreakers.txt'
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


# determine_winner_for_hands_from_file()
determine_winner_for_hands_from_deck()
determine_winner_for_hands_from_deck()
determine_winner_for_hands_from_deck()
determine_winner_for_hands_from_deck()
determine_winner_for_hands_from_deck()
