
from game_engine import Game
from bot import Bot
from rules import Rules
from playerSubmitted import Player  # <- Import player submission

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
