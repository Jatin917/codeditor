# participants code

from utils import is_next_uno, is_any_uno, draw_cards
from deck import Deck

class Player:
    def __init__(self, player_id, deck):
        """Initialize a player with an ID and a starting hand."""
        self.player_id = player_id
        self.hand = [deck.draw_card() for _ in range(7)]
    
    def get_card_count(self):
        """return the no of card player has"""
        return len(self.hand)

    def draw_card(self, deck, num_cards=1):
        """Draw a specified number of cards."""
        draw_cards(deck, self.hand, num_cards)

    def play_card(self, card, top_card, game_state):
        """Attempt to play a card. If invalid, force player to draw a card."""
        if card in self.hand and game_state.rules.is_valid_move(card, top_card):
            print("aya", card, top_card, game_state)
            self.hand.remove(card)
            game_state.played_cards.append(card)
            game_state.rules.apply_card_effect(card, game_state)

            # Check if THIS player has UNO
            if self.has_uno():
                print(f"⚠ Player {self.player_id} has UNO! ⚠")

            return True
        else:
            print(f"Invalid move! Player {self.player_id} must draw a card.")
            self.draw_card(game_state.deck)  # Force drawing a card
            return False

    def has_uno(self):
        """Check if the player has exactly one card left."""
        return len(self.hand) == 1

    def __str__(self):
        """Return a string representation of the player's hand."""
        return f"Player {self.player_id}: {self.hand}"

# Example Usage
if __name__ == "__main__":
    deck = Deck()
    player = Player(0, deck)
    print(player)
    player.draw_card(deck, 1)
    print(player)
