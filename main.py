from moves import *
from pokedex import pokedex
import sys
import time
import os
import random
 
class Pokemon:
    
    def __init__(self, name, type, level, stats, moves):
        self.name = name
        self.type = type
        self.level = level
        self.stats = self.setStats(stats, self.level)
        self.moves = moves
        self.maxHealth = stats["hp"]
        self.health = stats["hp"]
        
    def setStats(self, stats, level):
        for stat in stats:
            for i in range (1,level+1):
                stats[stat] += (stats[stat]/50)
                
            stats[stat] = int(round(stats[stat]))
            
        return stats
       
    def displayInfo(self, pokemon2, refresh):
        if refresh:
            clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')
            clearConsole() 
        print(f"Name: {self.name}\t\tName: {pokemon2.name}")
        print(f"LVL: {self.level}\t\t\tLVL: {pokemon2.level}")
        print(f"Type: {self.type}\t\tType: {pokemon2.type}")
        print(f"Health: {self.health}\t\tHealth: {pokemon2.health}")
        print("")

    def fight(self, pokemon2):
        
        while(True):
            #Displays the info for the pokemon in the battle
            self.displayInfo(pokemon2, True)  
            
            hit = True       
            chosenMove = self.selectMoves()   
                     
            if not chosenMove.doesHit():
                delay_print("Move missed")
                hit = False
            
            if hit:
                # Calculate damage without type advantage/disadvantage    
                damage =  chosenMove.use(self, pokemon2)
                
                if chosenMove.power > 0:
                    # Subtract health and check dead
                    pokemon2.health -= damage
                    
                    if pokemon2.health <= 0:
                        delay_print(f"\n{pokemon2.name} has fainted.")
                        break
                    
                    elif self.health <= 0:
                        delay_print(f"\n{self.name} has fainted.")
                        break
            
            # Player 2 turn          
            chosenMove = random.choice(pokemon2.moves)
            delay_print(f"\n{pokemon2.name} used "+chosenMove.name)
                       
            hit = True           
            if not chosenMove.doesHit():
                delay_print("Move missed")
                hit = False
            
            if hit:
                # Calculate damage without type advantage/disadvantage    
                damage =  chosenMove.use(pokemon2, self)
                
                if chosenMove.power > 0:
                    # Subtract health and check dead
                    self.health -= damage
                    if self.health <= 0:
                        delay_print(f"\n{self.name} has fainted.")
                        break
                    
                    elif pokemon2.health <= 0:
                        delay_print(f"\n{pokemon2.name} has fainted.")
                        break
                
            time.sleep(3)
                        
    def selectMoves(self):
        # Print out all the moves
            count = 1
            print("Moves:")
            for move in self.moves:
                print(f"{count}. {move.name} ({move.pp})")
                count += 1
                
            # Selecting move
            while (True):
                choice = int(input("Select move: "))
                if 1 <= choice <= len(self.moves):
                    chosenMove = self.moves[choice-1]
                    if chosenMove.checkPP:
                        break
                print("Invalid option\n")
            
            delay_print(f"\n{self.name} used "+chosenMove.name)
            
            return chosenMove
                                               
def delay_print(s):
    # Print one character at a time
    # https://stackoverflow.com/questions/9246076/how-to-print-one-character-at-a-time-on-one-line
    for c in s:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.05)
        
    sys.stdout.write("\n")
                                
def createPokemon():
    
    moves = [] 
         
    # count = 1 
    # level = int(input("Enter pokemon level: "))
      
    # while True:
    #     move = input(f"Move {count}: ")
        
    #     if move.lower() == "exit":
    #         break
        
    #     chosenMove = selectMove(move)
        
    #     if chosenMove != None:
    #         moves.append(chosenMove)
    #         count += 1
    #         if len(moves) == 4:
    #             break
    
    level = 15
    moves = [Tackle(), QuickAttack(), TakeDown(), Ember()]
            
    
    poke = random.choice(pokedex)
    return Pokemon(poke["name"], poke["types"][0], level, poke["baseStats"], moves)

def main():
    
    poke1 = createPokemon()
    poke2 = createPokemon()
    
    poke1.fight(poke2)
    
if __name__ == "__main__":
    main()