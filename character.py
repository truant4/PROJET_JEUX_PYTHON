from rich import print

class Character:
    def __init__(self, name, max_hp, attack_v, defense_v):
        self._name = name
        self._max_hp = max_hp
        self._hp = max_hp
        self._attack_value = attack_v
        self._defense_value = defense_v

    def __str__(self):
        return f"Hi ! My name is {self._name}. Attack: {self._attack_value}/Defense: {self._defense_value}"

    def is_alive(self):
        return self._hp > 0

    def show_healthbar(self):
        print(
            f"[{self._hp * "♥"}{(self._max_hp - self._hp) * " "}] {self._hp}/{self._max_hp}hp")

    def decrease_hp(self, amount):
        self._hp = max(0, self._hp - amount)
        self.show_healthbar()

    def compute_damages(self, target):
        return self._attack_value

    def attack(self, target):
        if (self.is_alive()):
            damages = self.compute_damages(target)
            print(
                f"[red]{self._name} attack {target._name} for {damages} damages.({self._attack_value} att)[/red]")
            target.defend(damages)

    def compute_wounds(self, damages):
        return damages - self._defense_value

    def defend(self, damages):
        wounds = self.compute_wounds(damages)
        print(f"[blue]{self._name} lost {wounds} hp. ({damages} dmg - {self._defense_value} def)[/blue]")
        self.decrease_hp(wounds)



if __name__ == "__main__":
    james = Character("James", 20, 8, 3)
    lisa = Character("Lisa", 20, 8, 3)

    print(james)
    print(lisa)

    while (james.is_alive() and lisa.is_alive()):
        james.attack(lisa)
        lisa.attack(james)