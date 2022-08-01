#!/usr/bin/env python3
"""
Blackjack game with simple rules (version 1.1, used sleeping time).

Classic casino rules (except splitting of players' pocket cards).
Implements S17 rule - dealer must draw on 16 or less, and stand on 17 or more.
The program creates and uses only one card desk per game.
"""
import random
import time

# Define winning constants
WIN_SCORE = 21
STAND_ON_SOFT = 17


def main():
    """Run main program."""
    # Show running titles
    print('Welcome to BLACKJACK game!')
    print('--------------------------')

    time.sleep(1)
    print('Do you want to read rules of the game? (YES=1, NO=0)')
    answer = get_user_choice()

    if answer == 1:
        show_rules()

    print()
    print('---------------------------')
    print('Player_1, ready to start...')

    for second in range(5, 0, -1):
        print(f'\t...{second}...')
        time.sleep(1)

    print()

    # Create hands for player and dealer
    player_hand = []
    dealer_hand = []

    # Create totals for player and dealer
    player_total = 0
    dealer_total = 0

    # Create flags if anybody exceeds 21
    player_exceed = False
    dealer_exceed = False

    # Create a new card deck
    card_deck = create_cards()

    # Deal first two cards and show hands
    # Deal cards:
    for card_number in range(1, 3):
        # for player
        print(f'Pocket card #{card_number} to you, Player_1.')
        new_card = deal_card(card_deck)
        player_hand.append(new_card)
        time.sleep(1)

        # for dealer
        print(f'Pocket card #{card_number} to dealer.')
        new_card = deal_card(card_deck)
        dealer_hand.append(new_card)
        time.sleep(1)

    # Show player's hands (first two cards)
    print()
    print('Your hand:')
    time.sleep(1)
    show_hand(player_hand)
    player_total = count_hand(player_hand)
    print()

    # Check if player has BLACKJACK
    player_blackjack = check_blackjack(player_hand)

    if player_blackjack:
        print('You get BLACKJACK!')
        print()

    print('Dealer\'s hand:')
    show_half_hand(dealer_hand)

    # Check if dealer has BLACKJACK:
    dealer_blackjack = check_blackjack(dealer_hand)

    if dealer_blackjack:
        print()
        print('Dealer gets BLACKJACK!')
        time.sleep(1)
        print()
        print('Dealer\'s hand:')
        show_hand(dealer_hand)

    # If BLACKJACK, the game finishes
    if player_blackjack and dealer_blackjack:
        print()
        time.sleep(1)
        print('PUSH! Game ties (both BLACKJACKS).')
    elif player_blackjack:
        print()
        time.sleep(1)
        print('You have BLACKJACK and win. Congratulations, Player_1!')
    elif dealer_blackjack:
        print()
        time.sleep(1)
        print('Sorry, dealer has BLACKJACK, you lose the game.')

    # Continue the game
    else:
        # Player hits or stands
        while player_total < WIN_SCORE:
            print()
            time.sleep(1)
            print(f'Player_1, your total: {player_total}')
            time.sleep(1)
            show_one_card(dealer_hand)
            time.sleep(1)
            print('You have to decide:')
            print('take another card (HIT=1) or pass (STAND=0).')
            time.sleep(2)
            hit = check_choice()

            if hit == 1:
                another_card = deal_card(card_deck)
                player_hand.append(another_card)
                print()
                time.sleep(1)
                print('Additional card  to you, Player_1.')
                print('Your hand:')
                show_hand(player_hand)
                player_total = count_hand(player_hand)
                print(f'Your total: {player_total}')

                # Check if player exeeds 21
                if player_total > WIN_SCORE:
                    player_exceed = True
                    print('Oh... BUST!')
            else:
                break

        # Open dealer's pocket hand
        print()
        time.sleep(1)
        print('Opening dealer\'s hand.')
        time.sleep(1)
        show_hand(dealer_hand)
        dealer_total = count_hand(dealer_hand)
        print(f'Dealer\'s total: {dealer_total}')

        # Dealer hits or stands
        if not player_exceed:
            while dealer_total < STAND_ON_SOFT:
                print()
                time.sleep(1)
                print('Additional card to dealer.')
                another_card = deal_card(card_deck)
                dealer_hand.append(another_card)
                print('Dealer\'s hand:')
                show_hand(dealer_hand)
                dealer_total = count_hand(dealer_hand)
                print(f'Dealer\'s total: {dealer_total}')

                # Check if dealer exeeds 21
                if dealer_total > WIN_SCORE:
                    dealer_exceed = True
                    print('Oh... BUST!')

        # Show totals and who wins the game
        print()
        time.sleep(2)
        print('********')
        print('Finally:')
        time.sleep(1)
        print(f'- Player_1, your total: {player_total}')
        print(f'- Dealer\'s total: {dealer_total}')
        time.sleep(2)
        # Print who wins or the game ties
        if player_total == dealer_total and player_total <= WIN_SCORE:
            print()
            time.sleep(1)
            print('PUSH! Game ties (equal totals).')
        elif player_exceed and dealer_exceed:
            print()
            time.sleep(1)
            print('BUST! Game ties (both exceed 21).')
        elif not player_exceed and dealer_exceed:
            print()
            time.sleep(1)
            print('Dealer exceeds 21 and you win.')
            print('Congratulations, Player_1!')
        elif player_exceed and not dealer_exceed:
            print()
            print('Sorry, dealer wins,')
            print('you exceed 21 and lose the game.')
        elif player_total > dealer_total:
            print()
            time.sleep(1)
            print('You win by higher total.')
            print('Congratulations, Player_1!')
        elif dealer_total > player_total:
            print()
            time.sleep(1)
            print('Sorry, dealer wins by higher total,')
            print('you lose the game.')

    # Show finishing titles
    print()
    time.sleep(2)
    print('---------------------------------------------')
    print('The game is over. Thanks for playing my game!')
    time.sleep(1)
    print('(c) Nobus, 2022')


def show_rules():
    """Print some game's rules."""
    print()
    print('You will play against the program (dealer).')
    print('The playing card deck consists of 52 cards:')
    time.sleep(3)
    print('- suits do not matter;')
    time.sleep(3)
    print('- 2, 3, 4, 5, 6, 7, 8, 9, 10 count as their numbers;')
    time.sleep(3)
    print('- J (Jack), Q (Queen), K (King) count as 10;')
    time.sleep(3)
    print('- A (Ace) counts as 11 if total is 21 or less (else counts as 1);')
    time.sleep(3)
    print('- if total of first two cards is 21 (10/J/Q/K + A),')
    print('  that hand wins as "BLACKJACK";')
    time.sleep(5)
    print('- if both hands are "BLACKJACKS", game ties ("PUSH");')
    time.sleep(3)
    print('- if total of player\'s cards is less than 21, he can choose:')
    print('  take another card ("HIT") or pass ("STAND");')
    time.sleep(5)
    print('- if total of dealer\'s cards is less than 17,')
    print('  he takes another card and repeat this step')
    print('  while total is not 17 or higher;')
    time.sleep(8)
    print('- if total of player or dealer exceeds 21 ("BUST"), he loses')
    print('  (when both exceed 21, game ties);')
    time.sleep(5)
    print('- if totals of player and dealer are equal and less 22,')
    print('  game ties ("PUSH");')
    time.sleep(5)
    print('- hand (cards) that is is closer to 21 but less 22, wins.')
    time.sleep(3)


def create_cards():
    """Create new card deck."""
    # Constants for card decks
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    SUITS = ['clubs', 'diamonds', 'hearts', 'spades']
    VALUES = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 1]

    # Create list of cards (rank with value)
    cards = []

    for rank in RANKS:
        for suit in SUITS:
            cards.append(f'{rank} of {suit}')

    # Multiply values for all 52 cards
    values = []

    for value in VALUES:
        for cycle in range(4):
            values.append(value)

    # Create and return card deck - dict of tuples (card, value)
    time.sleep(1)
    return list(zip(cards, values))


def deal_card(card_deck):
    """Deal a card from the playing card deck."""
    time.sleep(1)
    return card_deck.pop(random.randrange(0, len(card_deck)))


def show_card(dealt_card):
    """Show popped card."""
    card, value = dealt_card
    print(f'{card}: {value=}')


def show_hand(hand):
    """Show player's/dealer's hand."""
    time.sleep(1)
    for index, card in enumerate(hand):
        print(f'{index+1}) {card[0]}')
        time.sleep(1)


def show_half_hand(hand):
    """Show dealer's pocket hand with one card face down."""
    time.sleep(1)
    print(f'1) {hand[0][0]}')
    time.sleep(1)
    print('2) Card is face down')
    time.sleep(1)


def show_one_card(hand):
    """Show dealer's pocket card which is face up."""
    time.sleep(1)
    print(f'(Dealer\'s card is {hand[0][0]})')


def count_hand(hand):
    """Count card's values in players/dealer's hand."""
    total = 0
    is_ace = False

    for card in hand:
        if card[1] == 1:
            total += 11
            is_ace = True

            if total > 21:
                total -= 10
                is_ace = False
        else:
            total += card[1]
            if total > 21 and is_ace:
                total -= 10
                is_ace = False

    time.sleep(2)
    return total


def get_user_choice():
    """Input user's choice to hit or stand."""
    # Get and assert user's choice
    try:
        user_choice = int(input('>>> Enter your choice (1 or 0): '))
        assert user_choice in [0, 1]
    # If users's input is not 1 or 0 - return None
    except (AssertionError, ValueError):

        print('You should type 1 or 0 and then ENTER.')
        user_choice = None

    finally:
        return user_choice


def check_choice():
    """Get and check user's choice."""
    checked_choice = get_user_choice()

    # Re-enter user's input while it is not valid
    while checked_choice is None:
        checked_choice = get_user_choice()

    return checked_choice


def check_blackjack(hand):
    """Check if Blackjack."""
    return True if count_hand(hand) == WIN_SCORE else False


def check_s17(hand):
    """Check if S17 (stand-on-soft-17) for dealer."""
    return True if (count_hand(hand) == STAND_ON_SOFT and
                    len(hand) == 2 and
                    (hand[0][1] == 1 or hand[1][1] == 1)) else False


def check_exceeding(hand):
    """Check if anybody exceeds 21."""
    return True if count_hand(hand) > WIN_SCORE else False


if __name__ == '__main__':
    main()
