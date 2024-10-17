from states.warrior_state import NormalState, InjuredState, StunState
from races.race_factory import RaceFactory, Race

class Warrior:
    def __init__(self, name, race_type: str):
        self.name = name
        self.race_type = race_type
        self.race: Race = RaceFactory.create_race(race_type)
        self.state = NormalState()  # Le personnage commence dans un état normal

    def change_state(self, state):
        self.state = state

    def use_card(self, card, target):
        card.use(self, target)

    def decor_stats(self, decorator, amount):
        self.race.decor_stats(decorator, amount)

    def get_name(self):
        return self.name
    
    def get_race_name(self):
        return self.race.get_name()

    def get_life(self):
        return self.race.get_life()

    def get_stamina(self):
        return self.race.get_stamina()

    def get_energy(self):
        return self.race.get_energy()

    def get_shield(self):
        return self.race.get_shield()

    def get_speed(self):
        return self.race.get_speed()

    def get_force(self):
        return self.race.get_force()