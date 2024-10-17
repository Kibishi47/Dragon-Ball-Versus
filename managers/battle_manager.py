from managers.deck_manager import DeckManager
from managers.hand_manager import HandManager
from managers.team_manager import TeamManager
from gauge.gauge import EnergyGain

class BattleManager:
    _instance = None

    def __init__(self):
        self.player_instances = [
            "player",
            "enemy"
        ]
        self.waiting_room = {}

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def draw_cards(self, player_instance, times=1):
        for i in range(times):
            card = DeckManager.get_instance(player_instance).draw()
            if card:
                HandManager.get_instance(player_instance).add_card(card)

    def deck_shuffle(self, player_instance):
        DeckManager.get_instance(player_instance).shuffle()
    
    def init_game(self):
        for player_instance in self.player_instances:
            self.deck_shuffle(player_instance)
            self.draw_cards(player_instance, 4)

    def new_turn(self):
        self.waiting_room = {}
        for player_instance in self.player_instances:
            self.draw_cards(player_instance)
            warrior = TeamManager.get_instance(player_instance).get_active_warrior()
            warrior.decor_stats(EnergyGain, 10)

    def calculate_speed(self, warrior, card):
        warrior_speed = warrior.get_speed()
        card_speed = card.get_speed()
        return (warrior_speed + card_speed) / 2

    def get_other_warriors(self, warrior):
        warriors = []
        for infos in self.waiting_room.values():
            for info in infos:
                if warrior != info["warrior"]:
                    warriors.append(info["warrior"])
        return warriors

    def select_cards(self, cards_by_player_instance):
        # Tri des cartes jouées par les joueurs en fonction de leur vitesse
        for card, player_instance in cards_by_player_instance:
            warrior = TeamManager.get_instance(player_instance).get_active_warrior()
            HandManager.get_instance(player_instance).remove_card(card)
            speed = self.calculate_speed(warrior, card)
            info = {
                "card": card,
                "warrior": warrior
            }
            if speed in self.waiting_room:
                self.waiting_room[speed].append(info)
            else:
                self.waiting_room[speed] = [info]
        
        # Trie la waiting_room par vitesse décroissante
        self.waiting_room = dict(sorted(self.waiting_room.items(), reverse=True))
        
        # Exécute les actions des guerriers par ordre de vitesse
        for infos in self.waiting_room.values():  # Utilise .values() pour accéder aux valeurs
            if len(infos) == 1:  # Si un seul guerrier à cette vitesse
                warrior = infos[0]["warrior"]
                card = infos[0]["card"]
                for target in self.get_other_warriors(warrior):  # Trouve les autres guerriers
                    warrior.use_card(card, target)  # Utilise la carte sur les cibles
            else:
                print("Même vitesse, résolution d'un conflit de vitesse")