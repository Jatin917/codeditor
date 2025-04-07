import random
from rules import Rules
from utils import draw_cards

class Player:
    def __init__(self, player_id):
        self.player_id = player_id
        self.hand = []

    def is_valid_move(self, card, top_card):
        return Rules.is_valid_move(card, top_card)

    def play(self, hand, top_card):
        for card in hand:
            if self.is_valid_move(card, top_card):
                return card
        return None  # No valid move

    def choose_card(self, hand, top_card):
        valid_cards = [card for card in hand if Rules.is_valid_move(card, top_card)]
        if valid_cards:
            return random.choice(valid_cards)
        return None

    def find_playable_card(self, top_card):
        """Find the first playable card in hand using Rules."""
        for card in self.hand:
            if Rules.is_valid_move(card, top_card):
                return card
        return None

    def make_move(self, top_card, game):
        """Player keeps drawing until it finds a valid move, then plays it."""
        card_to_play = self.find_playable_card(top_card)

        # Draw until a valid card is found
        while card_to_play is None:
            print(f"[PLAYER {self.player_id}] No valid card. Drawing...")
            card = self.deck.draw_card()
            print(f"[PLAYER {self.player_id}] Drew card: {card}")
            self.hand.append(card)
            card_to_play = self.find_playable_card(top_card)

        print(f"[PLAYER {self.player_id}] Playing card: {card_to_play}")
        self.play_card(card_to_play, top_card, game)
        game.played_cards.append(card_to_play)
        Rules.apply_card_effect(card_to_play, game)

        if not game.check_winner():
            game.next_turn()

    def choose_color(self):
        colors = ['R', 'G', 'B', 'Y']
        chosen_color = random.choice(colors)
        print(f"[PLAYER {self.current_player}] Choose color: {chosen_color}")
        return chosen_color

    def play_card(self, card, top_card, game):
        """Play the card (assume it's already been checked as valid)."""
        if card in self.hand:
            self.hand.remove(card)

    def __str__(self):
        return f"[PLAYER] {self.player_id}: {self.hand}"
