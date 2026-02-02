import random

class Dice:
    def __init__(self,f=6 , c="red", m="plastic"):  # constructeur
        self.faces = f
        self.color = c
        self.material = m
        
    def __str__(self): #methodes avec __xxx__ sont des dender methode
        return f"This is a {self.color} {self.material} dice with {self.faces} faces"
    
    def __eq__(self, another_dice):
        return self.faces == another_dice.faces and self.color == another_dice.color and self.material == another_dice.material

    def roll(self):  # méthode
        return random.randint(1, self.faces)
        
class RiggedDice(Dice):

    def roll(self, rigged=False):
        if not rigged:
            return super().roll()
        else :
            return self.faces
        
if __name__ == "__main__":

    d1 = Dice(10, "blue", "wood")
    d2 = Dice(20, "green", "metal")  
    d3 = Dice()

    print(d1)
    print(d2)
    print(d3)
