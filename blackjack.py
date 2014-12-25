from enum import Enum
from random import shuffle

class Suit(Enum):
    """This represents the suit of a card.
    """
    clubs = "Clubs"
    diamonds = "Diamonds"
    hearts = "Hearts"
    spades = "Spades"

class Rank(Enum):
    """This represents the rank of a card.
    """
    ace = "Ace"
    two = "2"
    three = "3"
    four = "4"
    five = "5"
    six = "6"
    seven = "7"
    eight = "8"
    nine = "9"
    ten = "10"
    jack = "Jack"
    queen = "Queen"
    king = "King"

class Card(object):
    """Represents a playing card, where each card has a suit and rank.

    Attributes:
        rank: Rank of the card.
        suit: Suit of the card.
    """
    
    def __init__(self, rank, suit):
        """Initializes the card.
        """
        self.rank = rank
        self.suit = suit

    def __str__(self):
        """Returns a string of the card.
        """
        return str(self.rank.value + " of " + self.suit.value)

    def is_ace(self):
        """Returns true if the card is an ace.
        """
        return self.rank == Rank.ace

    def is_face(self):
        """Returns true if the card is a face card (king, queen, or jack).
        """
        return self.rank == Rank.jack or self.rank == Rank.queen or \
            self.rank == Rank.king

class Deck(object):
    """Represents a standard deck of playing cards.

    Attributes:
        cards: The cards of the deck.
    """
    
    def __init__(self):
        """Initializes the deck.
        """
        self.cards = [Card(rank, suit) for rank in Rank for suit in Suit]

    def get_cards(self):
        """Returns the cards in the deck.
        """
        return self.cards

class Shoe(object):
    """Represents a Shoe, which holds multiple decks.

    Attributes:
        cards: The cards of the shoe.
        garbage_pile: The cards that were used in previous rounds.
        card_counter: The number of cards dealt.
        total_cards: The number of cards in a full shoe
    """
    
    def __init__(self, number_of_decks = 1):
        """Initializes the shoe.

        Args:
            number_of_decks: The number of decks in the shoe.
        
        """
        self.card_counter = 0
        self.garbage_pile = []
        self.cards = []
        self.total_cards = 0
        if number_of_decks < 1:
            number_of_decks = 1
        for num in range(number_of_decks):
            deck = Deck()
            self.cards += deck.get_cards()
        shuffle(self.cards)
        self.total_cards = len(self.cards)

    def deal_card(self):
        """Deals a card from the shoe.

        Returns:
            A card in the shoe that is being dealt or None if there are
            no cards left in the shoe.
        """
        if not self.cards:
            return None            
        self.card_counter += 1
        return self.cards.pop()

    def get_cards_to_garbage_pile(self, discarded_cards=[]):
        """Takes the dealt cards and puts them in the garbage pile.
        """
        self.garbage_pile += discarded_cards

    def shuffle_required(self):
        """Whether a shuffle is needed, where half the shoe has been dealt.

        Returns:
            A boolean on whether or not the shoe needs to be shuffled.
        """
        return self.total_cards / 2 < self.card_counter

    def shuffle_cards(self):
        """Takes all the cards and shuffles them.
        """
        self.cards += self.garbage_pile
        self.garbage_pile = []
        shuffle(self.cards)
        self.card_counter = 0

class Hand(object):
    """Represents a Hand.

    Attributes:
        hand_cards: Cards in the hand.
        hand_value: Value of the hand.
        number_of_aces: Number of aces in the hand.
    """
    
    def __init__(self):
        """Initializes the hand.
        """
        self.hand_cards = []
        self.hand_value = 0
        self.number_of_aces = 0

    def __str__(self):
        """Returns a string of the hand.
        """
        return "\n".join(str(card) for card in self.hand_cards)

    def add_card(self, card):
        """Add a card to the hand and update its value.

        Args:
            card: The card added to the hand.
        """
        self.hand_cards.append(card)
        self.update_hand_value(card)

    def reset_hand(self):
        """Return cards and reset the hand to empty
        """
        temp = self.hand_cards
        self.hand_cards = []
        self.hand_value = 0
        self.number_of_aces = 0
        return temp

    def update_hand_value(self, card):
        """Update the hand based on the new card.

        Updates the hand to the best hand value. If adding the new card causes
        the value to be over 21 then change the value of an ace from 11 to 1.

        Args:
            card: The card added to the hand.
        """
        if card.is_ace():
            self.number_of_aces += 1
            self.hand_value += 11
        elif card.is_face():
            self.hand_value += 10
        else:
           self.hand_value += int(card.rank.value)
        if self.hand_value > 21 and self.number_of_aces > 0:
            self.hand_value -= 10
            self.number_of_aces -= 1

class Player(object):
    """Represents a player (user or dealer).

    Attributes:
        hand: Hand played.
    """
    
    def __init__(self):
        """Initializes the player and their hand.
        """
        self.hand = Hand()

    def add_card(self, card):
        """Adds a card to the player's hand.
        """
        self.hand.add_card(card)

    def can_hit(self):
        """Returns true if the hand can take another card.
        """
        return self.hand.hand_value < 21

    def is_bust(self):
        """Returns true if the hand is a bust.
        """
        return self.hand.hand_value > 21

    def print_hand_and_value(self):
        """Print the cards of the hand and its value.
        """
        print(self.hand)
        print("The hand value is", self.hand.hand_value)

class User(Player):
    """Represents a user player.

        Attributes:
        chips: Chips the user has.
    """
    
    def __init__(self,chips=100):
        """Initializes the player.
        """
        Player.__init__(self)
        self.chips = chips

    def has_chips(self):
        """Returns true if the player has chips.
        """
        return self.chips > 0

    def add_chips(self, chips):
        """Adds chips to the user.
        """
        self.chips += chips

    def remove_chips(self, chips):
        """Take away chips from the user.
        """
        self.chips -= chips
    
class Dealer(Player):
    """Represents a dealer player.
    """
    
    def __init__(self):
        """Initializes the player.
        """
        Player.__init__(self)
        
    def advised_to_hit(self):
        """Returns true if the hand is less than 17.
        """
        return self.hand.hand_value < 17

    def print_initial_dealer_hand(self):
        """Print the initial cards of the dealer's hand.

        When printing the initial dealer hand, the first card is shown and
        the second card is hidden.
        """
        print(self.hand.hand_cards[0])
        print("Hidden Card")

class GameError(Exception):
    """Error occurred in the game"""
    def __init__(self, value):
        self.value = value

class PlayerOption(Enum):
    """This represents the options that a player can select during a round
    of blackjack.
    """
    stand = 0
    hit = 1

class Game(object):
    """The blackjack game.

    Attributes:
        dealer: Dealer of the game.
        user: User of the game.
        shoe: Shoe of the game.
    """
    
    def __init__(self):
        """Initializes the game.

        Initialize the dealer, user, and shoe.
        """
        self.dealer = Dealer()
        self.user = User()
        self.shoe = Shoe()

    def play(self):
        """Checks if the user wants to and can play a round of blackjack.

        Allows the user to play a round of blackjack if they agree. They
        need to have enough chips. If needed then the cards will be shuffled.
        """
        response = True
        while response:
            if not self.user.has_chips():
                break
            response = self.yes_or_no("You have " + str(self.user.chips) +
                                 " chips. Would you like to play a round? ")
            if response:
                if self.shoe.shuffle_required():
                    self.shoe.shuffle_cards()
                self.play_round()

    def play_round(self):
        """Play a round of blackjack between the user and dealer.

        First get the number of chips the user would like to bet. Deal the
        cards. Ask the user for their move. If the player does not bust then
        the dealer will hit or stand. Finally, determine the winner.
        """
        bet = self.number_of_chips_to_bet()
        self.user.remove_chips(bet)
        self.initial_deal()
        self.print_initial_table()
        self.user_move()
        if not self.user.is_bust():
            self.dealer_move()
        self.results(bet)
        self.return_cards()
        
    def number_of_chips_to_bet(self):
        """Gets input for number of chips to bet.

        The number of chips that can be bet will be between 1 and the user's
        number of chips. If the user inputs an invalid bet then the user is
        informed that it is an invalid bet and will be asked for a valid bet.

        Returns:
            Returns the number of chips to bet.

        Raises:
            GameError: An error occurred determining the chips.
        """
        min_bet = 1
        max_bet = self.user.chips
        prompt = "Please place a bet between " + str(min_bet) + " and " + \
                 str(max_bet) + " chips. "
        if min_bet > max_bet:
            raise GameError("Min/Max bet error")
        try:
            while True:
                number = input(prompt).strip()
                if number.isdigit() and min_bet <= int(number) <= max_bet:
                    return int(number)
                print("Invalid input for bet.")
        except EOFError:
            raise GameError("EOFError")

    def initial_deal(self):
        """Initial deal for the round where each player gets two cards.
        """
        self.dealer.add_card(self.shoe.deal_card())
        self.user.add_card(self.shoe.deal_card())
        self.dealer.add_card(self.shoe.deal_card())
        self.user.add_card(self.shoe.deal_card())

    def print_initial_table(self):
        """Print the initial cards on the table.
        """
        print("Dealer hand:")
        self.dealer.print_initial_dealer_hand()
        print("User hand:")
        self.user.print_hand_and_value()

    def user_move(self):
        """User decides their move.

        While the user can hit their hand then ask them if they want to hit
        or stand. A hit adds a card to their hand. A stand means that the user
        is done with the move.
        """
        while self.user.can_hit():
            move = self.user_response("Would you like to hit or stand? ")
            if move == PlayerOption.hit:
                card = self.shoe.deal_card()
                print("Card is", card)
                self.user.add_card(card)
                print("Hand value is", self.user.hand.hand_value)
            elif move == PlayerOption.stand:
                break
        
    def user_response(self, prompt):
        """User responses with their move.

        The user will respond with their move. If the user inputs an invalid
        move then the user is informed that it is an invalid response and will
        be asked for a valid response.

        Args:
            prompt: The question asked to the user.
            
        Raises:
            GameError: An error occurred determining the response.
        """
        try:
            while True:
                answer = input(prompt).strip().lower()
                if answer in ("h", "hit"):
                    return PlayerOption.hit
                if answer in ("s", "stand"):
                    return PlayerOption.stand
                print("Invalid input.")
        except EOFError:
            raise GameError("EOFError")

    def dealer_move(self):
        """Dealer decides their move.

        A dealer will continue adding a card to their hand while the value of
        the hand is less than 17.
        """
        while self.dealer.advised_to_hit():
            self.dealer.add_card(self.shoe.deal_card())

    def results(self, bet):
        """The results of the round.

        At the end of the round, the dealer hand and user hand are shown. The
        winner is determined. If the dealer wins then the user gets no chips.
        If the user wins then the user gets double their bet chips. If the
        game is a tie then the user gets the bet chips back.

        Args:
            bet: A number representing the user's bet
        """
        print("Dealer hand:")
        self.dealer.print_hand_and_value()
        print("User hand:")
        self.user.print_hand_and_value()
        if self.user.is_bust():
            self.results_dealer_win(bet)
        elif self.dealer.is_bust():
            self.results_user_win(bet)
        elif self.dealer.hand.hand_value > self.user.hand.hand_value:
            self.results_dealer_win(bet)
        elif self.user.hand.hand_value > self.dealer.hand.hand_value:
            self.results_user_win(bet)
        else:
            self.results_tie(bet)

    def results_dealer_win(self, bet):
        """The results of a dealer win.

        Args:
            bet: A number representing the user's bet
        """
        print("Dealer wins.")

    def results_user_win(self, bet):
        """The results of a user win.

        Args:
            bet: A number representing the user's bet
        """
        print("User wins.")
        self.user.add_chips(bet*2)

    def results_tie(self, bet):
        """The results of a tie.

        Args:
            bet: A number representing the user's bet
        """
        print("Tie game.")
        self.user.add_chips(bet)

    def return_cards(self):
        """The cards are sent to the garbage pile of the shoe.
        """
        self.shoe.get_cards_to_garbage_pile(self.user.hand.reset_hand())
        self.shoe.get_cards_to_garbage_pile(self.dealer.hand.reset_hand())
        

    def end_game(self):
        """Thanks the user for playing the game.

        Thanks the user for playing blackjack and prints their number of
        chips remaining.
        """
        print("You have", self.user.chips, "chips.")
        print("Thank you for playing!")

    def yes_or_no(self, prompt, complaint = "Please respond yes or no."):
        """Gets input for a yes or no question.

        Args:
            prompt: The question asked to the user.
            complaint: The complaint print to the user if the user response is
                unacceptable.

        Returns:
            Returns true if the answer was yes (or some variation), otherwise
            it returns false if the answer was no (or some variation).
        
        Raises:
            GameError: An error occurred determining yes or no.
        """
        try:
            while True:
                answer = input(prompt).strip().lower()
                if answer in ("y", "ya", "yes", "yup"):
                    return True
                if answer in ("n", "no", "nope"):
                    return False
                print(complaint)
        except EOFError:
            raise GameError("EOFError")

def main():
    """The main method used to play the game.
    """
    game = Game()
    try:
        game.play()
    except GameError:
        print("Game ending error occcurred.")
    game.end_game()

if __name__ == '__main__':
    main()
