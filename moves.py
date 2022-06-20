import random
from main import delay_print

#===== Functions used by all moves =====

class AllMoves:
    def doesHit(self):
        accuracy = self.accuracy
        
        # Chooses a random float betweeen 0 and 1 to determine whether the move hits or not
        if random.randrange(0,1) < accuracy:
            return True
        
        return False
                

    def checkPP(self):
        if self.pp > 0:
            return True
        return False

#===== Types of moves =====
            
class GenericAttack(AllMoves):

    def use(self, poke1, poke2):
        return self.attack(poke1, poke2)
    
    def attack(self, poke1, poke2):
        # Equation for calculating damage
        # https://gamerant.com/pokemon-damage-calculation-help-guide/
        damage = round((2 * poke1.level) / 5)
        damage *= self.power
        if self.category == "physical":
            damage *= (poke1.stats["atk"] / poke2.stats["def"])
        else:
            damage *= (poke1.stats["spa"] / poke2.stats["spd"])
        damage /= 50
        damage += 2
        damage = round(damage)
        
        # Multiplies by the type matchup (0, 0.5, 1, 1.5, 2)
        damage *= self.typeMatchup(poke2)
        damage = round(damage)
        damage = int(damage)
        
        if random.randint(0,100) >= 85:
            damage *= 1.5
            delay_print("Critical hit")
            damage = round(damage)
            damage = int(damage)
            
        delay_print(f"It did {damage} damage")
        
        # Reduce the pp of the move
        self.pp -= 1
        
        return damage
    
    def typeMatchup(self, poke2):
    
        # Dictionary of types and indexes in the matrix
        types = ["Normal", "Fire", "Water", "Grass", "Electric", "Ice", "Fighting", "Poison", "Ground",
                 "Flying", "Psychic", "Bug", "Rock", "Ghost", "Dragon", "Dark", "Steel", "Fairy"]
        
        matchup = [[1,1,1,1,1,1,1,1,1,1,1,1,0.5,0,1,1,0.5,1],
                   [1,0.5,0.5,2,1,2,1,1,1,1,1,2,0.5,1,0.5,1,2,1],
                   [1,2,0.5,0.5,1,1,1,1,2,1,1,1,2,1,0.5,1,1,1],
                   [1,0.5,2,0.5,1,1,1,0.5,2,0.5,1,0.5,2,1,0.5,1,0.5,1],
                   [1,1,2,0.5,0.5,1,1,1,0,2,1,1,1,1,0.5,1,1,1],
                   [1,0.5,0.5,2,1,0.5,1,1,2,2,1,1,1,1,2,1,0.5,1],
                   [2,1,1,1,1,2,1,0.5,1,0.5,0.5,0.5,2,0,1,2,2,0.5],
                   [1,1,1,2,1,1,1,0.5,0.5,1,1,1,0.5,0.5,1,1,0,2],
                   [1,2,1,0.5,2,1,1,2,1,0,1,0.5,2,1,1,1,2,1],
                   [1,1,1,2,0.5,1,2,1,1,1,1,2,0.5,1,1,1,0.5,1],
                   [1,1,1,1,1,1,2,2,1,1,0.5,1,1,1,1,0,0.5,1],
                   [1,0.5,1,2,1,1,0.5,0.5,1,0.5,2,1,1,0.5,1,2,0.5,0.5],
                   [1,2,1,1,1,2,0.5,1,0.5,2,1,2,1,1,1,1,0.5,1],
                   [0,1,1,1,1,1,1,1,1,1,2,1,1,2,1,0.5,1,1],
                   [1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,0.5,0],
                   [1,1,1,1,1,1,0.5,1,1,1,2,1,1,2,1,0.5,1,0.5],
                   [1,0.5,0.5,1,0.5,2,1,1,1,1,1,1,2,1,1,1,0.5,2],
                   [1,0.5,1,1,1,1,2,0.5,1,1,1,1,1,1,2,2,0.5,1],
                   ]
    
        x = types.index(self.type.capitalize())
        y = types.index(poke2.type.capitalize())
        
        multiplier = matchup[x][y]
        
        if multiplier == 0: delay_print("It doesn't affect " + poke2.name)
        elif multiplier == 0.5: delay_print("Not very effective...")
        elif multiplier == 2: delay_print("Super effective!")
              
        return multiplier   

class AttackWithStat(GenericAttack):
    
    def use(self, poke1, poke2):
        damage = self.attack(poke1, poke2)
        self.sideEffect(poke1, poke2, damage)
        return damage
        
class StatMove(AllMoves):
    
    def __init__(self):
        self.power = 0
    
    def use(self, poke1, poke2):
        self.effect(poke1, poke2)
        self.pp -= 1
        

#===== Actual Moves =====

class AquaJet(GenericAttack):
    def __init__(self):
        self.name = "Aqua Jet"
        self.pp = 20
        self.power = 40
        self.accuracy = 1
        self.type = "water"
        self.category = "physical"
        
class Ember(GenericAttack):
    def __init__(self):
        self.name = "Ember"
        self.pp = 25
        self.power = 40
        self.accuracy = 1
        self.type = "fire"
        self.category = "special"
        
class Heal(StatMove):
    def __init__(self):
        self.name = "Heal"
        self.pp = 10
        self.accuracy = 1
        self.type = "normal"
    
    def effect(self, poke1, poke2):       
        poke1.health += 15
        if poke1.health > poke1.maxHealth:
            healthDiff =  poke1.health - poke1.maxHealth
            poke1.health -= healthDiff
            delay_print(f"{poke1.name} recovered {healthDiff} hp")

class Inferno(GenericAttack):
    def __init__(self):
        self.name = "Inferno"
        self.pp = 5
        self.power = 100
        self.accuracy = 0.5
        self.type = "fire"
        self.category = "special"
        
class Tackle(GenericAttack):
    def __init__(self):
        self.name = "Tackle"
        self.pp = 35
        self.power = 40
        self.accuracy = 1
        self.type = "normal"
        self.category = "physical"

class TakeDown(AttackWithStat):
    def __init__(self):
        self.name = "Take Down"
        self.pp = 20
        self.power = 90
        self.accuracy = 0.85
        self.type = "normal"
        self.category = "physical"
        
    def sideEffect(self, poke1, poke2, damage):
        recoilDamage = int(round(damage/4))
        poke1.health -= recoilDamage
        delay_print(f"{poke1.name} took {recoilDamage} damage of recoil")
        
class QuickAttack(GenericAttack):
    def __init__(self):
        self.name = "Quick Attack"
        self.pp = 30
        self.power = 40
        self.accuracy = 1
        self.type = "normal"
        self.category = "physical"
        
def selectMove(move):
    if move.lower() == "aqua jet": return AquaJet()
    if move.lower() == "ember": return Ember()
    if move.lower() == "heal": return Heal()
    if move.lower() == "inferno": return Inferno()
    if move.lower() == "tackle": return Tackle()
    if move.lower() == "takedown": return TakeDown()
    if move.lower() == "quick attack": return QuickAttack()
    
    else: return None