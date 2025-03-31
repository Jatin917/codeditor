# helper function

def is_next_uno(players, current_player, direction):
    """Check if the next player has only one card (UNO)."""
    next_player = (current_player + direction) % len(players)
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

