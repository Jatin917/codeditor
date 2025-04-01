# driver code

from game import Game
from utils import is_any_uno

def main():
    """Main function to run the UNO game."""
    game = Game(num_players=4)

    print("\n--- UNO Game Started! ---")
    print(f"Initial Hands: {game.players}")
    print(f"Starting Card: {game.played_cards[-1]}")

    while True:
        current_player = game.current_player
        player_hand = game.players[current_player]

        print(f"\nPlayer {current_player}'s Turn")
        print(f"Your Hand: {player_hand}")
        print(f"Top Card: {game.played_cards[-1]}")

        # Ask player for a move
        move = input("Enter the card to play (or 'draw' to pick a card): ").strip().upper()

        if move == "DRAW":
            game.players[current_player].append(game.deck.draw_card())
            print(f"Player {current_player} drew a card.")
        elif move in player_hand:
            if game.play_turn(move):  # Ensure turn is processed
                continue  # Move to next player
        else:
            print("Invalid move! Try again.")

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

if __name__ == "__main__":
    main()
