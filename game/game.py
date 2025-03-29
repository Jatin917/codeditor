from deck import Deck
from rules import Rules

class Game:
    def __init__(self, num_players=4):
        self.deck = Deck()
        self.players = {i: [] for i in range(num_players)}
        self.played_cards = []
        self.current_player = 0
        self.direction = 1  # 1 for clockwise, -1 for counterclockwise

        # Deal initial cards
        for _ in range(7):
            for p in range(num_players):
                self.players[p].append(self.deck.draw_card())

        # Start with one card
        self.played_cards.append(self.deck.draw_card())

    def next_turn(self):
        """Move to the next player's turn."""
        self.current_player = (self.current_player + self.direction) % len(self.players)

    def skip_turn(self):
        """Skip the next player's turn."""
        self.next_turn()
        self.next_turn()

    def reverse_turn_order(self):
        """Reverse the direction of turns."""
        self.direction *= -1

    def next_player_draw(self, num_cards):
        """Make the next player draw a specific number of cards."""
        next_player = (self.current_player + self.direction) % len(self.players)
        for _ in range(num_cards):
            self.players[next_player].append(self.deck.draw_card())

    def play_turn(self, player_move):
        """Handle a player's move."""
        if Rules.is_valid_move(player_move, self.played_cards[-1]):
            self.played_cards.append(player_move)
            Rules.apply_card_effect(player_move, self)
            self.next_turn()
        else:
            print("Invalid move!")

# Example Usage
if __name__ == "__main__":
    game = Game()
    print("Player Hands:", game.players)
    print("Top Card:", game.played_cards[-1])
