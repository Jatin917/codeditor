from player import Player
from utils import draw_cards
from deck import Deck
from rules import Rules


from rules import Rules
import random

class Bot:
    def __init__(self, player_id):
        self.id = player_id
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
        """Bot keeps drawing until it finds a valid move, then plays it."""
        card_to_play = self.find_playable_card(top_card)

        # Draw until a valid card is found
        while card_to_play is None:
            print(f"[BOT {self.player_id}] No valid card. Drawing...")
            card = self.deck.draw_card()  # ✅ Use self.deck
            print(f"[BOT {self.player_id}] Drew card: {card}")
            self.hand.append(card)
            card_to_play = self.find_playable_card(top_card)

        print(f"[BOT {self.player_id}] Playing card: {card_to_play}")
        # Play the valid card
        self.play_card(card_to_play, top_card, game)
        print("yha tak game chala")
        game.played_cards.append(card_to_play)
        Rules.apply_card_effect(card_to_play, game)

        if not game.check_winner():
            game.next_turn()


    def choose_color(self):
        colors = ['R', 'G', 'B', 'Y']
        chosen_color = random.choice(colors)
        print(f"[PLAYER {self.current_player}] Choose color: {chosen_color}")
        return chosen_color

    def __str__(self):
        return f"[BOT] Player {self.player_id}: {self.hand}"


# Example usage
if __name__ == "__main__":
    from game_engine import Game  # Now using the updated game file

    deck = Deck()
    game = Game(num_players=1)  # 1 human + 1 bot, assuming bot is player 1

    # Replace one of the default players with our Bot
    bot = Bot(1, deck)
    game.players[1] = bot  # ✅ Store the whole Bot object, not just its hand

    print(bot)
    top_card = game.played_cards[-1]
    print(f"Top card: {top_card}")
    bot.make_move(top_card, game)
    print(bot)
