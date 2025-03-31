from deck import Deck
from rules import Rules


class Game:

    def __init__(self, num_players=4):
        self.deck = Deck()
        self.players = {
            i: [self.deck.draw_card() for _ in range(7)]
            for i in range(num_players)
        }
        self.played_cards = [self.deck.draw_card()]
        self.current_player = 0
        self.direction = 1  # 1 for clockwise, -1 for counterclockwise

    def next_turn(self):
        """Move to the next player's turn."""
        self.current_player = (self.current_player + self.direction) % len(
            self.players)

    def skip_turn(self):
        """Skip the next player's turn."""
        self.next_turn()
        self.next_turn()

    def reverse_turn_order(self):
        """Reverse the direction of turns."""
        self.direction *= -1

    def next_player_draw(self, num_cards):
        """Make the next player draw a specific number of cards."""
        next_player = (self.current_player + self.direction) % len(
            self.players)
        for _ in range(num_cards):
            self.players[next_player].append(self.deck.draw_card())

    def check_winner(self):
        """Check if a player has won the game."""
        for player, hand in self.players.items():
            if not hand:
                print(f"Player {player} wins!")
                return True
        return False

    def play_turn(self, player, player_move=None):
        """Handle a player's move."""
        if player != self.current_player:
            print("Not your turn!")
            return

        if player_move and Rules.is_valid_move(player_move,
                                               self.played_cards[-1]):
            self.played_cards.append(player_move)
            self.players[player].remove(player_move)
            Rules.apply_card_effect(player_move, self)
            if not self.check_winner():
                self.next_turn()
        else:
            print("No valid moves, drawing a card...")
            drawn_card = self.deck.draw_card()
            self.players[player].append(drawn_card)
            if Rules.is_valid_move(drawn_card, self.played_cards[-1]):
                print(f"You drew {drawn_card}, and it can be played!")
            self.next_turn()


# Example Usage
if __name__ == "__main__":
    game = Game()
    print("Initial Player Hands:", game.players)
    print("Top Card:", game.played_cards[-1])
