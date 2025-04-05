
from game import Game
from utils import is_any_uno

def main():
    """Main function to run the UNO game."""
    game = Game(num_players=4)

    print("\n--- UNO Game Started! ---")
    print("Initial Game State:", game.get_game_state())

    while True:
        current_player = game.current_player
        player_hand = game.players[current_player]

        print(f"\nPlayer {current_player}'s Turn")
        print(f"Your Hand: {player_hand}")
        print(f"Top Card: {game.played_cards[-1]}")

        # Ask player for a move
        move = input("Enter the card to play (or 'draw' to pick a card): ").strip().upper()

        if move == "DRAW":
            drawn_card = game.deck.draw_card()
            game.players[current_player].append(drawn_card)
            print(f"Player {current_player} drew {drawn_card}.")
            if game.play_turn(current_player, drawn_card):
                print("Updated Game State:", game.get_game_state())
                continue  # Move to next player
            else:
                print("No playable card drawn. Turn ends.")
                # next_turn already handled in play_turn if needed
        elif move in player_hand:
            if game.play_turn(current_player, move):  # Ensure turn is processed
                print("Updated Game State:", game.get_game_state())
                continue  # Move to next player
        else:
            print("Invalid move! Try again.")
            continue  # Ask again without skipping

        # Check if the game has a winner
        if len(game.players[current_player]) == 0:
            print(f"\n🎉 Player {current_player} wins! 🎉")
            break

        # Check if anyone has UNO
        if is_any_uno(game.players):
            print("\n⚠ Someone has UNO! ⚠")

        # If the last played card was a "+2" or "+4", the next player is skipped
        if game.played_cards[-1][1:] in ["P", "PR"]:
            game.skip_turn()

        print("Updated Game State:", game.get_game_state())

if __name__ == "__main__":
    main()
