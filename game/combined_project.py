# ===== File: utils.py =====
# helper function

def is_next_uno(players, current_player, direction):
    keys = sorted(players.keys())
    current_index = keys.index(current_player)
    next_index = (current_index + direction) % len(keys)
    next_player = keys[next_index]
    return len(players[next_player]) == 1


def draw_cards(deck, player_hand, num_cards):
    """Draw a specified number of cards and add them to the player's hand."""
    for _ in range(num_cards):
        player_hand.append(deck.draw_card())

def skip_turn(current_player, direction, num_players):
    """Skip the current player's turn."""
    return (current_player + 2 * direction) % num_players

def is_any_uno(players):
    """Check if any player has UNO (only one card left)."""
    return any(len(hand) == 1 for hand in players.values())


# ===== File: deck.py =====
import random

def initialize_deck():
    colors = ['R', 'G', 'B', 'Y']
    numbers = list(range(10))
    actions = ['S', 'R', 'P']

    deck = []
    for color in colors:
        deck.append(f"{color}0")  # One 0 per color
        for num in range(1, 10):
            deck.extend([f"{color}{num}"] * 2)
        for action in actions:
            deck.extend([f"{color}{action}"] * 2)

    wild_cards = ['WC', 'WC', 'WC', 'WC']
    plus_four_cards = ['PC', 'PC', 'PC', 'PC']
    deck.extend(wild_cards)
    deck.extend(plus_four_cards)

    return deck

class Deck:
    def __init__(self):
        self.cards = initialize_deck()
        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop() if self.cards else None

    def reset_deck(self, played_cards):
        """Shuffle played cards back into the deck, keeping the last card in play."""
        last_card = played_cards.pop()
        self.cards = played_cards
        random.shuffle(self.cards)
        self.cards.insert(0, last_card)


# ===== File: rules.py =====
# from game import Game
class Rules:
    VALID_COLORS = {'R', 'G', 'B', 'Y', 'W', 'P'}  # W for Wild # P for Plus4
    ACTION_CARDS = {'S': 'Skip', 'R': 'Reverse', 'P': 'Draw4', 'W': 'Wild'}

    @staticmethod
    def is_valid_move(card, top_card):
        """
        Check if the played card is valid based on UNO rules.
        Card format: [C][N] where C is color (R, G, B, Y) and N is number/action (0-9, S, R, P, W)
        Wild cards: WC/WC/WC/WC (Wild Color), PC/PC/PC/PC (Wild Draw 4), RP/BP/GP/YP (Draw 2)
        """
        if not top_card:
            return True  # First move is always valid
        
        if not card or not top_card:
            return False

        def parse_card(card_str):
            if card_str.startswith("P"):
                # P card (like 'PY' or 'PR')
                value = "P"
                color = card_str[1:] if len(card_str) > 1 else ""
            elif card_str.startswith("W"):
                # Wild card (like 'WR', 'WG')
                value = "W"
                color = card_str[1:] if len(card_str) > 1 else ""
            else:
                # Normal card (like 'R5', 'G2')
                color = card_str[0] if len(card_str) > 1 else ""
                value = card_str[1:] if len(card_str) > 1 else ""
            return color, value


        current_color, current_value = parse_card(card)
        top_color, top_value = parse_card(top_card)

        return (
            current_color == top_color or
            current_value == top_value or
            current_value in {"W", "P"}  # wilds or plus-fours can always be played
        )


    @staticmethod
    def apply_card_effect(card, game_state, agent):
        """
        Apply the effect of action or wild cards to the game state.
        
        Args:
            card (str): The card played (e.g., "RS", "W4", "WR")
            game_state: Game state object with methods: skip_turn(), reverse_turn_order(), 
                       next_player_draw(n), set_next_color(color), challenge_plus_four()
        """
        if not card or not game_state:
            return

        if 'S' in card:  # Skip
            game_state.skip_turn()
        elif 'R' in card:  # Reverse
            game_state.reverse_turn_order()
        elif card.startswith("P") and not card.startswith("W"):  # Wild Draw 4 (PC, PC, PC, PC)
            game_state.next_player_draw(4)
            game_state.skip_turn()
            game_state.prompt_color_choice("P", agent) #Player chooses a color
        elif card.endswith("P"):  # Draw 2 (RP, BP, GP, YP)
            game_state.next_player_draw(2)
            game_state.skip_turn()
        elif card.startswith("W"):  # Wild Color (WC, WC, WC, WC)
            game_state.prompt_color_choice("W", agent) #Player chooses a color


    @staticmethod
    def is_special_card(card):
        """Check if the card is a special action or wild card."""
        if not card:
            return False
        return any(symbol in card for symbol in Rules.ACTION_CARDS.keys())

    @staticmethod
    def get_card_color(card):
        """Get the color of a card (or wild color if specified)."""
        if not card:
            return None
        if card.startswith("W"):
            return "W"  # Wild
        if card.endswith("P"):
            return "2" # Draw 2  
        return card[0] if card[0] in Rules.VALID_COLORS else None

    @staticmethod
    def is_next_uno(game_state, current_player, next_player):
        """
        Check if the next player has only one card left (UNO).
        
        Args:
            game_state: Game state object with player hands
            current_player: Current player's index
            next_player: Next player's index
            
        Returns:
            bool: True if next player has UNO, False otherwise
        """
        return len(game_state.get_player_hand(next_player)) == 1

    @staticmethod
    def is_any_uno(game_state, players):
        """
        Check if any player has only one card left.
        
        Args:
            game_state: Game state object with player hands
            players: List of player indices
            
        Returns:
            bool: True if any player has UNO, False otherwise
        """
        return any(len(game_state.get_player_hand(player)) == 1 for player in players)

    @staticmethod
    def deck_draw(deck, discard_pile, player_hand):
        """
        Draw a card from the deck. If deck is empty, reshuffle discard pile.
        
        Args:
            deck: List of cards in deck
            discard_pile: List of discarded cards
            player_hand: List of cards in player's hand
            
        Returns:
            str: Drawn card, or None if no cards available
        """
        if not deck and discard_pile:
            deck.extend(discard_pile[:-1])  # Keep top card
            import random
            random.shuffle(deck)
            discard_pile = [discard_pile[-1]]  # Reset discard pile to top card

        if deck:
            card = deck.pop()
            player_hand.append(card)
            return card
        return None

    @staticmethod
    def pass_turn(game_state):
        """Skip the current player's turn."""
        game_state.skip_turn()

    @staticmethod
    def check_uno_penalty(game_state, current_player, players):
        """
        Enforce UNO call. If a player has one card and didn't call UNO, penalize them.
        
        Args:
            game_state: Game state object
            current_player: Current player's index
            players: List of all players
        """
        if len(game_state.get_player_hand(current_player)) == 1:
            if not game_state.has_called_uno(current_player):
                game_state.next_player_draw(2)  # Penalty for not calling UNO
                print(f"Player {current_player} forgot to say UNO! Drawing 2 cards as penalty.")

    @staticmethod
    def challenge_plus_four(challenger, challenged, game_state):
        """
        Handle challenge on a +4 card.
        
        Args:
            challenger: Index of challenging player
            challenged: Index of player who played +4
            game_state: Game state object with methods to draw cards
            
        Returns:
            bool: True if challenge was successful, False otherwise
        """
        # Check if challenged player had any playable card of matching color
        last_card = game_state.get_last_played_card()
        if not last_card or not last_card.startswith("P"):
            return False  # No +4 to challenge

        challenged_hand = game_state.get_player_hand(challenged)
        top_card_before = game_state.get_top_card_before_last()
        has_playable = any(Rules.is_valid_move(card, top_card_before) and 
                          Rules.get_card_color(card) == Rules.get_card_color(top_card_before)
                          for card in challenged_hand)

        if has_playable:
            # Challenge successful: challenged player draws 4
            game_state.next_player_draw(4, challenged)
            return True
        else:
            # Challenge failed: challenger draws 6
            game_state.next_player_draw(6, challenger)
            return False

    @staticmethod
    def can_stack(card1, card2):
        """
        Check if two cards can be stacked (e.g., +2 on +2).
        
        Args:
            card1: First card
            card2: Second card
            
        Returns:
            bool: True if stacking is allowed, False otherwise
        """
        return (card1.startswith("P") and card2.startswith("P")) or (card1.endswith("P") and card2.endswith("P") )

    @staticmethod
    def enforce_auto_penalty(card, game_state, player_hand):
        """
        Apply penalty if an invalid move is attempted.
        
        Args:
            card: Card attempted to play
            game_state: Game state object
            player_hand: Current player's hand
        """
        top_card = game_state.get_top_card()
        if not Rules.is_valid_move(card, top_card):
            game_state.next_player_draw(2)  # Penalty for invalid move
            print("Invalid move! Drawing 2 cards as penalty.")

# Example usage and testing
if __name__ == "__main__":
    class MockGameState:
        def __init__(self):
            self.players_hands = {0: ["R5", "GS"], 1: ["B7"], 2: ["Y9"]}
            self.current_top_card = "R2"
            self.last_played = None
            self.turn_order = [0, 1, 2]
            self.current_player = 0
            self.uno_calls = {i: False for i in range(3)}

        def skip_turn(self):
            print("Turn skipped!")

        def reverse_turn_order(self):
            self.turn_order.reverse()
            print("Turn order reversed!")

        def next_player_draw(self, n, player=None):
            if player is None:
                player = (self.current_player + 1) % len(self.turn_order)
            print(f"Player {player} draws {n} cards!")

        def set_next_color(self, color):
            print(f"Next color set to {color}")

        def get_player_hand(self, player):
            return self.players_hands[player]

        def get_top_card(self):
            return self.current_top_card

        def get_last_played_card(self):
            return self.last_played

        def get_top_card_before_last(self):
            return "G6"  # Example

        def has_called_uno(self, player):
            return self.uno_calls[player]

    # game_state = MockGameState()

    # # Test cases
    # print("Testing UNO Check:")
    # assert Rules.is_next_uno(game_state, 0, 1) == True  # Player 1 has UNO
    # assert Rules.is_any_uno(game_state, [0, 1, 2]) == True

    # print("\nTesting Special Cards:")
    # Rules.apply_card_effect("RS", game_state, agent=None)  # Skip
    # Rules.apply_card_effect("RR", game_state, agent=None)  # Reverse
    # Rules.apply_card_effect("WR", game_state, agent=None)  # Wild
    # Rules.apply_card_effect("PR", game_state, agent=None)   # +4
    # Rules.apply_card_effect("RP", game_state, agent=None)  # +2

    # print("\nTesting Deck and Draw:")
    # deck = ["R3", "B4", "Y5"]
    # discard = ["R2"]
    # hand = ["G6"]
    # drawn = Rules.deck_draw(deck, discard, hand)
    # print(f"Drawn card: {drawn}, New hand: {hand}")

    # print("\nTesting UNO Penalty:")
    # Rules.check_uno_penalty(game_state, 1, [0, 1, 2])  # Player 1 should get penalty

    # print("\nTesting +4 Challenge:")
    # result = Rules.challenge_plus_four(1, 0, game_state)
    # print(f"Challenge result: {'Successful' if result else 'Failed'}")

    # print("\nTesting Stacking:")
    # assert Rules.can_stack("RP", "BP") == True  # +2 can stack on +2
    # assert Rules.can_stack("PR", "PB") == True  # +4 can stack on +4

    # print("\nTesting Auto Penalty:")
    # Rules.enforce_auto_penalty("B9", game_state, ["R5", "G6"])  # Should penalize



# ===== File: bot.py =====
# from deck import Deck
# from rules import Rules

import random

class Bot:
    def __init__(self, player_id):
        self.player_id = player_id
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
        print(f"[PLAYER {self.player_id}] Choose color: {chosen_color}")
        return chosen_color

    def __str__(self):
        return f"[BOT] Player {self.player_id}: {self.hand}"


# ===== File: playerSubmitted.py =====
import random
# from rules import Rules

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
        print(f"[PLAYER {self.player_id}] Choose color: {chosen_color}")
        return chosen_color

    def play_card(self, card, top_card, game):
        """Play the card (assume it's already been checked as valid)."""
        if card in self.hand:
            self.hand.remove(card)

    def __str__(self):
        return f"[PLAYER] {self.player_id}: {self.hand}"



# ===== File: game_engine.py =====
import random
# from deck import Deck
# from rules import Rules

class Game:
    def __init__(self):
        self.deck = Deck()
        self.players = {0: [], 1: []}  # 0 = human, 1 = bot
        self.current_player = 0
        self.direction = 1
        self.played_cards = []
        self.initialize_hands()

    def initialize_hands(self):
        for pid in self.players:
            self.players[pid] = [self.deck.draw_card() for _ in range(7)]
        first_card = self.deck.draw_card()
        while first_card[1:] in ["W", "WR"]:  # Avoid wilds as first card
            self.deck.cards.append(first_card)
            random.shuffle(self.deck.cards)
            first_card = self.deck.draw_card()
        self.played_cards.append(first_card)

    def next_turn(self):
        self.current_player = (self.current_player + 1) % 2

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
            
    def check_winner(self):
        """Check if a player has won the game."""
        for player, hand in self.players.items():
            if not hand:
                print(f"Player {player} wins!")
                return True
        return False

    def get_game_state(self):
        """Returns the game state with player card counts."""
        return {
            "player_card_counts": {player: len(hand) for player, hand in self.players.items()},
            "current_player": self.current_player,
            "top_card": self.played_cards[-1],
            "direction": "clockwise" if self.direction == 1 else "counterclockwise"
        }

    def play_turn(self, player, player_move=None, agent=None):
        """Handle a player's move."""
        if player != self.current_player:
            print("Not your turn!")
            return

        if player_move and Rules.is_valid_move(player_move, self.played_cards[-1]):
            self.played_cards.append(player_move)
            self.players[player].remove(player_move)
            Rules.apply_card_effect(player_move, self, agent)
            if not self.check_winner():
                self.next_turn()
        else:
            print("No valid moves, drawing a card...")
            drawn_card = self.deck.draw_card()
            self.players[player].append(drawn_card)
            if Rules.is_valid_move(drawn_card, self.played_cards[-1]):
                print(f"You drew {drawn_card}, and it can be played!")
            self.next_turn()

    
    def prompt_color_choice(self,action, agent):
        # chosen_color = input("Choose a color [R, G, B, Y]: ").strip().upper()
        chosen_color = agent.choose_color()
        print(self.players[self.current_player], "choose color")
        while chosen_color not in {'R', 'G', 'B', 'Y'}:
            # chosen_color = input("Invalid color. Choose from [R, G, B, Y]: ").strip().upper()
            chosen_color = agent.choose_color()
        self.set_next_color(chosen_color,action)

    
    def set_next_color(self, color, action):
        print(action + color, "color+action")
        self.played_cards[-1] = action + color  # <- correctly update top card
        print(self.played_cards[-1], "current top card")
        print(f"Color changed to {color}")

    
    def draw_card(self, player_name):
        if self.turn_order[self.current_player_idx] != player_name:
            return {'error': 'Not your turn'}
        drawn_card = self.deck.draw_card()
        self.players[player_name].append(drawn_card)
        self.next_turn()
        return {'message': 'Card drawn', 'card': drawn_card}


# ===== File: main.py =====

# from game_engine import Game
# from bot import Bot
# from rules import Rules
# from playerSubmitted import Player  # <- Import player submission

def main():
    game = Game()
    bot = Bot(player_id=1)
    player = Player(player_id=0)  # <- Create instance of player code
    while True:
        state = game.get_game_state()
        current_player = state["current_player"]
        top_card = state["top_card"]

        print("\n---------------------------")
        print(f"Top card on pile: {top_card}")
        print(f"Your cards: {game.players[0]}")
        print(f"Bot has {len(game.players[1])} cards.")

        if current_player == 0:
            # Use player's bot logic
            player_move = player.choose_card(game.players[0], top_card)
            print(f"Player plays: {player_move if player_move else 'draws a card'}")
            if player_move:
                game.play_turn(0, player_move, player)
            else:
                game.play_turn(0)

        else:
            # Predefined bot turn
            bot_move = bot.choose_card(game.players[1], top_card)
            print(f"Bot plays: {bot_move if bot_move else 'draws a card'}")
            if bot_move:
                game.play_turn(1, bot_move, bot)
            else:
                game.play_turn(1)

        # Check for winner
        if game.check_winner():
            break

if __name__ == "__main__":
    main()



