import random
from managers.deck_manager import DeckManager

class Deck:
    def __init__(self, cards=None):
        if cards is None:
            self.cards = []
        else:
            self.cards = cards

    def add_card(self, card):
        if len(self.cards) < DeckManager.max_card_amount: 
            self.cards.append(card)
            return True
        return False
    
    def remove_card(self, card):
        self.cards.remove(card)

    def get_card_number(self, card = None):
        if card is not None:
            card_names = list(map(lambda card: card.get_name(), self.cards))
            return card_names.count(card.get_name())
        return len(self.cards)

    def draw(self):
        if len(self.cards) == 0:
            return None
        return self.cards.pop(0)
    
    def shuffle(self):
        random.shuffle(self.cards)