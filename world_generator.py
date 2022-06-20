import random
#REMOVER FUNÇÕES REPETIDAS DO MAIN E DAQUI
#WORLD GENERATOR (INSPIRED BY DWARF FORTRESS) ----------------------------------------------------------------------
import random
from os import system, name
#FUNCTIONS
def clear_console():
    # for windows
    if name == 'nt':
        _ = system('cls')

def text_with_color(color,text):
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
    elif color == "Grey":
        coloring = "\u001b[30;1m"
    
    return (coloring+text+"\u001b[0m")

class World():#NEED BETTER WORLD GENERATION
    def __init__(self,name):
        self.name = name
    
    def generate_world(self,number_rows,number_columns):
        #setup of coordinates and start positions
        for row in range(number_rows):
            for column in range(number_columns):
                if random.randint(0,100) == 100:
                    provinces.update({(row,column):"*"})
                else:
                    provinces.update({(row,column):"~"})

        #setup terrains
        for row in range(number_rows):
            for column in range(number_columns):
                if row > 1 and column > 1 and row < number_rows-1 and column < number_columns-1:
                    if ((provinces[(row-1,column)] == "*") and (provinces[(row,column-1)] == "*")):
                        if random.randint(0,20) > 16:
                            provinces.update({(row,column):"^"})
                    elif ((provinces[(row-1,column)] == "*") or (provinces[(row,column-1)] == "*")
                    or (provinces[(row+1,column)] == "*") or (provinces[(row,column+1)] == "*")):
                        if random.randint(0,20) > 5:
                            provinces.update({(row,column):"*"})
    
    def generate_populations(self,num_of_races):
        for i in range(num_of_races):
            found_race = False
            
            while found_race == False:
                new_race = random.choice(list_racial_names)
                if new_race not in used_races:
                    found_race = True
                    used_races.append(new_race)
                    in_world_races.append(Population(random.randint(1,1000),new_race))
        #CAN UPDATE RACE TRAITS HERE OR MAYBE IN CLASS POPULATION?

    def print_world(self,number_rows,number_columns):
        #Print World
        for row in range(number_rows):
            for column in range(number_columns):
                if provinces[(row,column)] == "*":#GROUND
                    print(text_with_color("Green",provinces[(row,column)]),end=" ")
                elif provinces[(row,column)] == "^":#MOUNTAIN
                    print(text_with_color("Grey",provinces[(row,column)]),end=" ")
                elif provinces[(row,column)] == "X":#CURSOR
                    print(text_with_color("Yellow",provinces[(row,column)]),end=" ")
                else:#SEA
                    print(text_with_color("Blue",provinces[(row,column)]),end=" ")
            print()
        #CAN UPDATE ANY TERRAIN WITH DICTIONARY UPDATE .update{(row,column):symbol} row and column = int
    
class Population():#SETUP FOR DIFFERENT POPULATIONS
    def __init__(self,quantity,race):
        self.quantity = quantity
        self.race = race

#DATA TO BE USED
list_racial_names = ["human","orc","elf","goblin","dwarf","gnome","giants","satyr"]
accept_world = ""
provinces = {}
#WORLD SETUP
while accept_world != "yes":
    provinces = {}
    used_races = []
    in_world_races = []
    clear_console()
    print(text_with_color("Green","World Generator"))
    world_size_row = int(input("Width of world: "))
    world_size_column = int(input("Height of world: "))
    num_world_races = int(input("How many races in world: "))
    player_world = World("")
    player_world.generate_world(world_size_row,world_size_column)
    player_world.generate_populations(num_world_races)
    player_world.print_world(world_size_row,world_size_column)
    print(text_with_color("Green","Races in World:"))
    for i in in_world_races:
        print(text_with_color("Green",((i.race).capitalize())),"population:"+str(i.quantity))
    accept_world = input(text_with_color("Green","Accept world? (yes/no): ")).strip().lower()
    if accept_world == "yes":
        player_world.name = input("World Name:")

#WORLD
clear_console()
print(text_with_color("Green",player_world.name))
player_world.print_world(world_size_row,world_size_column)

#CURSOR
while True:
    print("Choose coordinates for",text_with_color("Yellow","Cursor"),": ")
    cursor_input_x = int(input("x coordinate: "))
    cursor_input_y = int(input("y coordinate: "))
    saved_symbol = provinces[(cursor_input_x,cursor_input_y)]
    provinces.update({(cursor_input_x,cursor_input_y):"X"})
    clear_console()
    player_world.print_world(world_size_row,world_size_column)
    ans = input("See this region? (yes/no)").lower().strip()
    if ans == "yes":
        provinces.update({(cursor_input_x,cursor_input_y):saved_symbol})
        print(provinces[(cursor_input_x,cursor_input_y)]," this region is called...")
    else:
        provinces.update({(cursor_input_x,cursor_input_y):saved_symbol})