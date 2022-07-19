import curses
import random
import text_tools


class World():#NEED BETTER WORLD GENERATION
    def __init__(self,name,provinces,list_racial_names,used_races,in_world_races):
        self.name = name
        self.provinces = provinces
        self.list_racial_names = list_racial_names
        self.used_races = used_races
        self.in_world_races = in_world_races
    
    def __str__(self):
        return f"Name: {self.name}"
    
    def generate_world(self,number_rows,number_columns):
        """Creates a procedural world"""
        #setup of coordinates and start positions
        for row in range(number_rows):
            for column in range(number_columns):
                if random.randint(0,100) == 100:
                    self.provinces.update({(row,column):"*"})
                else:
                    self.provinces.update({(row,column):"~"})

        #setup terrains
        for row in range(number_rows):
            for column in range(number_columns):
                if row > 1 and column > 1 and row < number_rows-1 and column < number_columns-1:
                    if ((self.provinces[(row-1,column)] == "*") and (self.provinces[(row,column-1)] == "*")):
                        if random.randint(0,20) > 16:
                            self.provinces.update({(row,column):"^"})
                    elif ((self.provinces[(row-1,column)] == "*") or (self.provinces[(row,column-1)] == "*")
                    or (self.provinces[(row+1,column)] == "*") or (self.provinces[(row,column+1)] == "*")):
                        if random.randint(0,20) > 5:
                            self.provinces.update({(row,column):"*"})
    
    def generate_populations(self,num_of_races):
        """Generate population for world"""
        for i in range(num_of_races):
            found_race = False
            
            while found_race == False:
                new_race = random.choice(self.list_racial_names)
                if new_race not in self.used_races:
                    found_race = True
                    self.used_races.append(new_race)
                    self.in_world_races.append(Population(random.randint(1,1000),new_race))
        #CAN UPDATE RACE TRAITS HERE OR MAYBE IN CLASS POPULATION?

    def print_world(self,number_rows,number_columns,main_window,max_y,max_x,colors):
        """Puts World Map on Screen"""
        y_axis = (max_y//2)-10
        x_axis = (max_x//2)-15
        for row in range(number_rows):
            for column in range(number_columns):
                if self.provinces[(row,column)] == "*":#GROUND
                    main_window.addstr(y_axis,x_axis,str(self.provinces[(row,column)]),colors[0])
                elif self.provinces[(row,column)] == "^":#MOUNTAIN
                    main_window.addstr(y_axis,x_axis,str(self.provinces[(row,column)]),colors[0])
                elif self.provinces[(row,column)] == "X":#CURSOR
                    main_window.addstr(y_axis,x_axis,str(self.provinces[(row,column)]),colors[0])
                else:#SEA
                    main_window.addstr(y_axis,x_axis,str(self.provinces[(row,column)]),colors[1])
                x_axis += 1
                main_window.refresh()
            y_axis += 1
            x_axis = (max_x//2)-15
        main_window.refresh()
        #CAN UPDATE ANY TERRAIN WITH DICTIONARY UPDATE .update{(row,column):symbol} row and column = int
    
class Population():#SETUP FOR DIFFERENT POPULATIONS
    def __init__(self,quantity,race):
        self.quantity = quantity
        self.race = race
    
    def __str__(self):
        return self.race
#FUNCTIONS--

def world(main_window,color,max_y,max_x,colors_list):
    """Procedure that executes world creation and input."""
    accept = ""
    while accept != "yes":
        #DATA TO BE USED
        list_racial_names = ["human","orc","elf","goblin","dwarf","gnome","giants","hobbit"]
        provinces = {}
        #WORLD SETUP
        provinces = {}
        used_races = []
        in_world_races = []
        main_window.clear()
        main_window.addstr((max_y//2)-10,(max_x//2)-15,"World Generator",color)
        main_window.refresh()
        curses.napms(1000)
        main_window.clear()
        #WORLD WIDTH
        main_window.addstr((max_y//2)-10,(max_x//2)-15,"Width (CTRL+G) to save",color)
        main_window.refresh()
        world_size_row = text_tools.game_input(main_window,color,max_y,max_x,5,10).strip()
        world_size_row = int(world_size_row)
        main_window.clear()
        #WORLD HEIGHT
        main_window.addstr((max_y//2)-10,(max_x//2)-15,"Height (CTRL+G) to save",color)
        main_window.refresh()
        world_size_column = text_tools.game_input(main_window,color,max_y,max_x,5,10).strip()
        world_size_column = int(world_size_column)
        main_window.clear()
        #NUM RACES WORLD
        main_window.addstr((max_y//2)-10,(max_x//2)-15,"Races in World Number (CTRL+G) to save",color)
        main_window.refresh()
        num_world_races = text_tools.game_input(main_window,color,max_y,max_x,5,10).strip()
        num_world_races = int(num_world_races)
        main_window.clear()
        #WORLD NAME
        main_window.addstr((max_y//2)-10,(max_x//2)-15,"World name (CTRL+G) to save",color)
        main_window.refresh()
        world_name = text_tools.game_input(main_window,color,max_y,max_x,5,10).strip()
        main_window.clear()
        #TERRAIN/POP--
        player_world = World(world_name,provinces,list_racial_names,used_races,in_world_races)
        player_world.generate_world(world_size_row,world_size_column)
        player_world.generate_populations(num_world_races)
        player_world.print_world(world_size_row,world_size_column,main_window,max_y,max_x,colors_list)
        main_window.refresh()
        main_window.getkey()
        main_window.clear()
        #SHOW RACES--
        main_window.addstr((max_y//2)-15,(max_x//2)-15,"Races in World:",color)
        y_race = (max_y//2)-10
        for race in in_world_races:
            cap_race = race.race.capitalize()
            main_window.addstr(y_race,(max_x//2)-15,f"{cap_race} Population: {race.quantity}",color)
            y_race += 1
        main_window.refresh()
        main_window.getkey()
        #ACCEPT--
        main_window.addstr((max_y//2)-5,(max_x//2)-15,"Accept World?",color)
        #yes
        yes_button = text_tools.Button(main_window,"yesb",3,10,(max_y//2),(max_x//2)-15,colors_list[2])
        yes_button.create()
        yes_button.string_center("YES")
        yes_button.border(True)
        yes_button.update()
        #no
        no_button = text_tools.Button(main_window,"nob",3,10,(max_y//2),(max_x//2)-5,colors_list[2])
        no_button.create()
        no_button.string_center("NO")
        no_button.border(True)
        no_button.update()
        main_window.refresh()
        key_position = 1
        while True:
            key = main_window.getkey()
            if key == "KEY_RIGHT":
                if key_position >= 1 and key_position < 2:
                    key_position += 1
            elif key == "KEY_LEFT":
                if key_position > 1 and key_position >= 2:
                    key_position -= 1
            elif key == "c":
                if key_position == 1:
                    accept = "yes"
                    break
                else:
                    break
            
            if key_position == 1:
                yes_button.bg_color(True)
                no_button.bg_color(False)
            elif key_position == 2:
                yes_button.bg_color(False)
                no_button.bg_color(True)

            yes_button.update()
            no_button.update()
            main_window.refresh()
        main_window.clear()
    #WORLD
    main_window.addstr((max_y//2)-15,(max_x//2)-15,f"{player_world.name}",colors_list[0])
    player_world.print_world(world_size_row,world_size_column,main_window,max_y,max_x,colors_list)
    main_window.getkey()
    main_window.clear()
    #MAP SELECT WITH CURSOR---
    cursor_row = 0
    cursor_column = 0
    while True:
        main_window.clear()
        main_window.addstr((max_y//2)-15,(max_x//2)-15,f"{player_world.name} ({cursor_row},{cursor_column})",colors_list[0])
        saved_symbol = provinces[(cursor_row,cursor_column)]
        provinces.update({(cursor_row,cursor_column):"X"})
        player_world.print_world(world_size_row,world_size_column,main_window,max_y,max_x,colors_list)
        main_window.refresh()
        cursor_key = main_window.getkey()
        if cursor_key == "KEY_UP":
            provinces.update({(cursor_row,cursor_column):saved_symbol})
            cursor_row -= 1
            if cursor_row < 0:
                cursor_row += 1
        elif cursor_key == "KEY_DOWN":
            provinces.update({(cursor_row,cursor_column):saved_symbol})
            cursor_row += 1
            if cursor_row > world_size_row-1:
                cursor_row -= 1
        elif cursor_key == "KEY_RIGHT":
            provinces.update({(cursor_row,cursor_column):saved_symbol})
            cursor_column += 1
            if cursor_column > world_size_column-1:
                cursor_column -= 1
        elif cursor_key == "KEY_LEFT":
            provinces.update({(cursor_row,cursor_column):saved_symbol})
            cursor_column -= 1
            if cursor_column < 0:
                cursor_column += 1
        elif cursor_key == "c":
            #CHOOSE START REGION--
            if saved_symbol == "*":
                main_window.clear()
                provinces.update({(cursor_row,cursor_column):saved_symbol})
                world_made = True
                main_window.addstr((max_y//2)-15,(max_x//2)-15,f"World {player_world.name} created.",colors_list[0])
                curses.napms(200)
                main_window.clear()
                #RETURNS OF WORLD--
                region_start = (cursor_row,cursor_column)
                return world_made,player_world,region_start
        else:
            provinces.update({(cursor_row,cursor_column):saved_symbol})
        main_window.refresh()
