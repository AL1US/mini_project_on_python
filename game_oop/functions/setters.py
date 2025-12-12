from classes.class_players import (
    Player,
    Warrior,
    Mage,
    Arrow,
    Tank
)

def create_player(name: str, player_class: int):
    if player_class == 1:
        return Warrior(name)
    elif player_class == 2:
        return Mage(name)
    elif player_class == 3:
        return Arrow(name)
    elif player_class == 4:
        return Tank(name)