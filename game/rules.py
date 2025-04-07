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
    def apply_card_effect(card, game_state):
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
            game_state.prompt_color_choice("P", game_state) #Player chooses a color
        elif card.endswith("P"):  # Draw 2 (RP, BP, GP, YP)
            game_state.next_player_draw(2)
            game_state.skip_turn()
        elif card.startswith("W"):  # Wild Color (WC, WC, WC, WC)
            game_state.prompt_color_choice("W", game_state) #Player chooses a color


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

    game_state = MockGameState()

    # Test cases
    print("Testing UNO Check:")
    assert Rules.is_next_uno(game_state, 0, 1) == True  # Player 1 has UNO
    assert Rules.is_any_uno(game_state, [0, 1, 2]) == True

    print("\nTesting Special Cards:")
    Rules.apply_card_effect("RS", game_state)  # Skip
    Rules.apply_card_effect("RR", game_state)  # Reverse
    Rules.apply_card_effect("WR", game_state)  # Wild
    Rules.apply_card_effect("PR", game_state)   # +4
    Rules.apply_card_effect("RP", game_state)  # +2

    print("\nTesting Deck and Draw:")
    deck = ["R3", "B4", "Y5"]
    discard = ["R2"]
    hand = ["G6"]
    drawn = Rules.deck_draw(deck, discard, hand)
    print(f"Drawn card: {drawn}, New hand: {hand}")

    print("\nTesting UNO Penalty:")
    Rules.check_uno_penalty(game_state, 1, [0, 1, 2])  # Player 1 should get penalty

    print("\nTesting +4 Challenge:")
    result = Rules.challenge_plus_four(1, 0, game_state)
    print(f"Challenge result: {'Successful' if result else 'Failed'}")

    print("\nTesting Stacking:")
    assert Rules.can_stack("RP", "BP") == True  # +2 can stack on +2
    assert Rules.can_stack("PR", "PB") == True  # +4 can stack on +4

    print("\nTesting Auto Penalty:")
    Rules.enforce_auto_penalty("B9", game_state, ["R5", "G6"])  # Should penalize