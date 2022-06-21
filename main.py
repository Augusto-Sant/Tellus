from os import name, system
import random
from time import sleep

class Player():
    def __init__(self,name,age,race):
        self.name = name
        self.age = age
        self.inventory = []
        self.race = race
        #STATS
        self.strength = 0
        self.dexterity = 0
        self.intelligence = 0
        self.hp = 0
        self.weapon_force = 0
        #
        self.xp = 0
        self.level = 1
    
    
    def level_up(self):
        if self.xp >= 100:
            self.level += 1
            #stats up
            self.strength += 1
            self.dexterity += 1
            self.intelligence += 1
            self.hp += 10
            #
            print(text_with_color("Red",(self.name,"is now level:",self.level)))

    
    def attack(self):
        """Attacks"""
        #attack = strength+weapon_force+d6
        return self.strength+self.weapon_force+rolld6()
    
    def charinfo(self):
        print("-----------------")
        print(text_with_color("Red",("{} {} {} years".format(self.name,self.race,self.age))))
        print(text_with_color("Red","HP: "+str(self.hp)))
        print(text_with_color("Red","STR: "+str(self.strength)))
        print(text_with_color("Red","DEX: "+str(self.dexterity)))
        print(text_with_color("Red","INT: "+str(self.intelligence)))
        #WEAPON EQUIPPED ALWAYS index = 0
        print(text_with_color("Red",("Weapon Equipped: {}".format(self.inventory[0]))))
        print("-----------------")

    def __str__(self):
        return ("{n}, {a}, {r}".format(n=self.name,a=self.age,r=self.race))

class Enemy_generic():
    def __init__(self,name,hp,strg,dex,level):
        self.name = name
        #STATS
        self.strength = strg
        self.dexterity = dex
        #self.intelligence = intel
        self.hp = hp
        #
        self.level = level    
    
    def attack(self):
        """Attacks"""
        #attack = strength+d6
        return self.strength+rolld6()
    
    def charinfo(self):
        print("-----------------")
        print(text_with_color("Red",("{} {} {} years".format(self.name,self.race,self.age))))
        print(text_with_color("Red","HP: "+str(self.hp)))
        print(text_with_color("Red","STR: "+str(self.strength)))
        print(text_with_color("Red","DEX: "+str(self.dexterity)))
        #print(text_with_color("Red","INT: "+str(self.intelligence)))
        print("-----------------")

    def __str__(self):
        return ("{n}, {a}, {r}".format(n=self.name,a=self.age,r=self.race))

#UTILITIES
def clear():
  
    # for windows
    if name == 'nt':
        _ = system('cls')

def rolld6():
    return random.randint(1,6)

def text_with_color(color,text):
    """Changes text color"""

    if color == "Red":
        coloring = "\u001b[31m"
    elif color == "White":
        coloring = "\u001b[37m"
    elif color == "Blue":
        coloring = "\u001b[34m"
    elif color == "Yellow":
        coloring = "\u001b[33m"
    elif color == "Green":
        coloring = "\u001b[32m"
    
    return (coloring+text+"\u001b[0m")

#EVENTS
def random_battle(fighter):
    #monster = [id:[name,str,dex]]
    #GENERIC MONSTERS Without special abilities for now (only base attack)
    monsters = {0:['Cockatrice',9,8],1:['Gorgon',15,6],2:['Dire Wolf',5,7],3:['Bear',10,6],4:['Skeleton Warrior',6,3],
        5:['Golem',12,1],6:['Goblin',7,5],7:['Human Bandit',7,5],8:['Kobold',5,8],9:['Ghoul',8,4],10:['Orc Warrior',9,4],
        11:['Lizardfolk',10,3],12:['Tribal Elf',12,8],13:['Hobgoblin',9,6],14:['Troll',12,3],15:['Orc Champion',15,4],
        16:['Wyrmling Dragon',15,3],
    }
    i = random.randint(0,17)
    random_monster = monsters[i]
    gen_monster = Enemy_generic(random_monster[0],random_monster[1]*10,random_monster[1],random_monster[2],1)
    print(text_with_color("Red","**Battle Has started with a "+gen_monster.name+"**"))
    sleep(3)
    clear()
    while (gen_monster.hp > 0) and (fighter.hp > 0):
        print(text_with_color("Red",(gen_monster.name+" HP: "+str(gen_monster.hp))))
        print(text_with_color("Red",fighter.name+" HP: "+str(fighter.hp)))
        print("----BATTLE-----")
        sleep(2)
        #dex could be here to determine who first
        organs = ["arm","leg","torso"]
        #
        fighter_atk = fighter.attack()
        #
        monster_atk = gen_monster.attack()
        #player attack
        print("{} Attack: {}".format(fighter.name,str(fighter_atk)))
        #player rolls dex
        miss_player = (fighter.dexterity+rolld6())
        miss_monster = (gen_monster.dexterity+rolld6())
        if fighter.dexterity < (miss_monster/2):
            print("and misses..")
        else:
            if fighter_atk > 15:
                organ_name = "head"
            else:
                organ_name = random.choice(organs)
            print(text_with_color("Red","and {} hits {}".format(fighter.name,organ_name)))
            gen_monster.hp -= fighter_atk
        #
        print((gen_monster.name+" Attack: "+str(monster_atk)))
        if gen_monster.dexterity < (miss_player/2):
            print("and misses..")
        else:
            if monster_atk > miss_player and gen_monster.dexterity > fighter.dexterity:
                organ_name = "head"
            else:
                organ_name = random.choice(organs)
            print(text_with_color("Red","and {} hits {}".format(gen_monster.name,organ_name)))
            fighter.hp -= monster_atk  
        sleep(5)
        print("--------------")
        clear()
    
    if fighter.hp <= 0:
        print(text_with_color("Red","YOU DIED"))
    else:
        clear()#Finish may not be aproppriate to monster
        finishes = [" cuts the head of the "," leaves the bleeding "," strangles to death the "]
        print(text_with_color("Red",fighter.name+random.choice(finishes)+random_monster[0]))
        random_xp = random.randint(0,30)
        print(text_with_color("Green",("XP Gained: {}".format(random_xp))))
        fighter.xp += random_xp
        sleep(5)

        
def main():
    player_name = input("What is your name: ")
    player_age = input("How old are you: ")
    player_race = input("Choose Race 1.Human 2.Elf 3.Dwarf: ")#ONLY HUMANS WORK FOR NOW
    if player_race == "1":
        player_race = "Human"
        new_hp = 150
        new_int = 6
        new_str = 5
        new_dex = 7
    elif player_race == "2":
        player_race = "Elf"
        new_hp = 100
        new_int = 7
        new_str = 3
        new_dex = 14
    elif player_race == "3":
        player_race = "Dwarf"
        new_hp = 200
        new_int = 7
        new_str = 8
        new_dex = 5
    player = Player(player_name,player_age,player_race)
    player.hp += new_hp
    player.strength += new_str
    player.dexterity += new_dex
    player.intelligence += new_int
    #item
    player.inventory.append("Sword")
    #later create system for inventory
    player.weapon_force = 5
    #-----
    #MAIN LOOP
    while player.hp > 0:
        clear()
        player.charinfo()
        sleep(4)
        random_battle(player)

if __name__ == "__main__":
    main()