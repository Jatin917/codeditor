import random

class Deck:
    def __init__(self):
        self.cards = self.initialize_deck()
        random.shuffle(self.cards)

    def initialize_deck(self):
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

        wild_cards = ['WR', 'WG', 'WB', 'WY']
        plus_four_cards = ['PR', 'PG', 'PB', 'PY']
        deck.extend(wild_cards)
        deck.extend(plus_four_cards)

        return deck

    def draw_card(self):
        return self.cards.pop() if self.cards else None

    def reset_deck(self, played_cards):
        """Shuffle played cards back into the deck, keeping the last card in play."""
        last_card = played_cards.pop()
        self.cards = played_cards
        random.shuffle(self.cards)
        self.cards.insert(0, last_card)


# Example Usage
if __name__ == "__main__":
    deck = Deck()
    print("Initial Deck:", deck.cards[:10])
    print("Drawn Card:", deck.draw_card())
