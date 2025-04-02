`class Rules:
    @staticmethod
    def is_valid_move(card, top_card):
        """Check if the played card is valid based on UNO rules."""
        if not top_card:
            return True  # First move
        return (card[0] == top_card[0]) or (card[1:] == top_card[1:]) or (card.startswith("W") or card.startswith("P"))

    @staticmethod
    def apply_card_effect(card, game_state):
        """Apply the effect of action/wild cards."""
        if 'S' in card:
            game_state.skip_turn()
        elif 'R' in card:
            game_state.reverse_turn_order()
        elif 'P' in card and card.startswith("P"):
            game_state.next_player_draw(4)
        elif 'P' in card:
            game_state.next_player_draw(2)

# Example Usage
if __name__ == "__main__":
    print(Rules.is_valid_move("R5", "R2"))  # True (same color)
    print(Rules.is_valid_move("B9", "R2"))  # False
    print(Rules.is_valid_move("WR", "R2"))  # True (wild)
`