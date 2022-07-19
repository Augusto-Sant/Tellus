import curses
from curses import textpad
import random

#RPG LIKE GAME USING CURSES

#CLASSES--
class Button():
    def __init__(self,main_window,name,height,width,begin_y,begin_x,colors):
        self.main_window = main_window
        self.name = name
        self.height = height
        self.width = width
        self.begin_y = begin_y
        self.begin_x = begin_x
        
        #add more than one after
        self.colors = colors

    def create(self):
        """creates button window, border = True/False"""
        self.name = self.main_window.subwin(self.height,self.width,self.begin_y,self.begin_x)
        return self.name
    
    def border(self,border):
        if border == True:
            self.name.border()

    def update(self):
        """Refreshes button window"""
        return self.name.refresh()
    
    def string_center(self,content):
        """Show a string inside center of window"""
        size = len(content)
        return self.name.addstr(self.height//2,(self.width//2)-(size//2),f"{content}")
    
    def bg_color(self,on):
        """on = True/False"""
        if on == True:
            return self.name.bkgd(" ",self.colors)
        else:
            return self.name.bkgd(" ",curses.color_pair(0))

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

class Entity():
    def __init__(self,symbol,x,y):
        self.symbol = symbol
        self.x = x
        self.y = y
    
    def move(self,main_window,x_input,y_input):
        if self.x != x_input:
            if self.x < x_input:
                self.x += 1
            elif self.x > x_input:
                self.x -= 1
        elif self.y != y_input:
            if self.y < y_input:
                self.y += 1
            elif self.y > y_input:
                self.y -= 1
    
    def idle(self):
        chance = random.randint(0,4)
        if chance == 1:
            self.x += 1
            if self.x > 154-1:
                self.x -= 1
        elif chance == 2:
            self.x -= 1
            if self.x < 0:
                self.x += 1
        elif chance == 3:
            self.y += 1
            if self.y > 38-1:
                self.y -= 1
        else:
            self.y -= 1
            if self.y < 0:
                self.y += 1

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
        world_size_row = game_input(main_window,color,max_y,max_x,5,10).strip()
        world_size_row = int(world_size_row)
        main_window.clear()
        #WORLD HEIGHT
        main_window.addstr((max_y//2)-10,(max_x//2)-15,"Height (CTRL+G) to save",color)
        main_window.refresh()
        world_size_column = game_input(main_window,color,max_y,max_x,5,10).strip()
        world_size_column = int(world_size_column)
        main_window.clear()
        #NUM RACES WORLD
        main_window.addstr((max_y//2)-10,(max_x//2)-15,"Races in World Number (CTRL+G) to save",color)
        main_window.refresh()
        num_world_races = game_input(main_window,color,max_y,max_x,5,10).strip()
        num_world_races = int(num_world_races)
        main_window.clear()
        #WORLD NAME
        main_window.addstr((max_y//2)-10,(max_x//2)-15,"World name (CTRL+G) to save",color)
        main_window.refresh()
        world_name = game_input(main_window,color,max_y,max_x,5,10).strip()
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
        yes_button = Button(main_window,"yesb",3,10,(max_y//2),(max_x//2)-15,colors_list[2])
        yes_button.create()
        yes_button.string_center("YES")
        yes_button.border(True)
        yes_button.update()
        #no
        no_button = Button(main_window,"nob",3,10,(max_y//2),(max_x//2)-5,colors_list[2])
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

def play(main_window):
    BLACK_WHITE,RED_BLACK,BLACK_RED,BLUE_BLACK,BLACK_BLUE,GREEN_BLACK = curses_colors()
    max_y,max_x = main_window.getmaxyx()
    main_window.border()
    main_window.addstr(max_y-1,1,"(q) to quit",RED_BLACK)
    main_window.addstr(0,1,"(c) to Call",BLUE_BLACK)
    main_window.addstr(0,25,"(.) to pass time",BLUE_BLACK)
    main_window.getkey()
    curses.curs_set(0)
    entity1 = Entity("D",1,1)
    entity2 = Entity("@",5,10)
    entity3 = Entity("I",6,10)
    cursor = Entity("X",0,0)
    entities = [cursor,entity1,entity2,entity3]
    while True:
        curses.napms(16)
        terrain(main_window,max_y,max_x,entities)
        cursor_key = main_window.getkey()
        if cursor_key == "KEY_UP":
            cursor.y -= 1
            if cursor.y < 0:
                cursor.y += 1
        elif cursor_key == "KEY_DOWN":
            cursor.y += 1
            if cursor.y > 38-1:
                cursor.y -= 1
        elif cursor_key == "KEY_RIGHT":
            cursor.x += 1
            if cursor.x > 154-1:
                cursor.x -= 1
        elif cursor_key == "KEY_LEFT":
            cursor.x -= 1
            if cursor.x < 0:
                cursor.x += 1
        elif cursor_key == "c":
            for entity in entities:
                entity.move(main_window,cursor.x,cursor.y)
        elif cursor_key == "q":
            curses.endwin()
            main_window.clear()
            break

        for entity in entities:
            if entity.symbol != "X":
                entity.idle()

def terrain(main_window,max_y,max_x,entities):
    """Terrain for play function"""
    colors = curses_colors()
    curses.init_pair(7,curses.COLOR_CYAN,curses.COLOR_BLACK)
    GREY = curses.color_pair(7)
    y_axis = 1
    x_axis = 1
    #row == y column == x
    for row in range(38):
        for column in range(154):
            if len(entities) > 0:
                for entity in entities:
                    if entity.y == row and entity.x == column:
                        main_window.addstr(y_axis,x_axis,entity.symbol,colors[5])
                        main_window.refresh()
                        break
                    else:
                        #ground
                        main_window.addstr(y_axis,x_axis,"¨",GREY)
            else:
                #ground
                main_window.addstr(y_axis,x_axis," ")
            x_axis += 1
            main_window.refresh()
        y_axis += 1
        x_axis = 1
    main_window.refresh()

def game_input(main_window,bg_color,max_y,max_x,height=15,width=60,):
    """A small procedure to create input box for commands."""
    input_window = main_window.subwin(height,width,(max_y//2)-5,(max_x//2)-15)
    input_window.bkgd(bg_color)
    curses.curs_set(1)
    input_box = textpad.Textbox(input_window)
    input_box.edit()
    text_input = input_box.gather()
    input_window.refresh()
    curses.curs_set(0)
    return text_input

def title(main_window):
    """Title screen"""
    main_window.addstr(10,30,
    """
                                         _________ _______  _        _        __   __  _______ 
                                         \__   __/(  ____ \( \      ( \      (__) (__)(  ____ |
                                            ) (   | (    \/| (      | (               | (    \/
                                            | |   | (__    | |      | |      |\     /|| (_____ 
                                            | |   |  __)   | |      | |      | )   ( |(_____  )
                                            | |   | (      | |      | |      | |   | |      ) |
                                            | |   | (____/\| (____/\| (____/\| (___) |/\____) |
                                            )_(   (_______/(_______/(_______/(_______)\_______)
                                                                                                (By August Sant)
    """)

def curses_colors():
    """Returns colors for text"""
        #COLORS
    curses.init_pair(1,curses.COLOR_BLACK,curses.COLOR_WHITE)
    curses.init_pair(2,curses.COLOR_RED,curses.COLOR_BLACK)
    curses.init_pair(3,curses.COLOR_BLUE,curses.COLOR_BLACK)
    curses.init_pair(4,curses.COLOR_BLACK,curses.COLOR_BLUE)
    curses.init_pair(5,curses.COLOR_GREEN,curses.COLOR_BLACK)
    curses.init_pair(6,curses.COLOR_BLACK,curses.COLOR_RED)
    BLACK_WHITE = curses.color_pair(1)
    RED_BLACK = curses.color_pair(2)
    BLACK_RED = curses.color_pair(6)
    BLUE_BLACK = curses.color_pair(3)
    BLACK_BLUE = curses.color_pair(4)
    GREEN_BLACK = curses.color_pair(5)
    return BLACK_WHITE,RED_BLACK,BLACK_RED,BLUE_BLACK,BLACK_BLUE,GREEN_BLACK

#main--
def main(src):
    #INIT
    max_y,max_x = src.getmaxyx()
    key_position = 2
    #hide cursor
    curses.curs_set(0)
    BLACK_WHITE,RED_BLACK,BLACK_RED,BLUE_BLACK,BLACK_BLUE,GREEN_BLACK = curses_colors()
    src.border()

    search_button = Button(src,"search",5,15,8,3,BLACK_BLUE)
    search_button.create()
    add_button = Button(src,"add",5,15,13,3,BLACK_BLUE)
    add_button.create()
    remove_button = Button(src,"remove",5,15,18,3,BLACK_RED)
    remove_button.create()
    src.refresh()
    #world init
    world_made = False
    while True:
        src.border()
        src.addstr(max_y-1,1,"(q) to quit",RED_BLACK)
        src.addstr(0,1,"(c) to choose",BLUE_BLACK)
        key = src.getkey()

        #KEY INPUT
        if key == "q":
            curses.endwin()
            break
        elif key == "KEY_UP":
            if key_position > 1 and key_position <= 3:
                key_position -= 1
        elif key == "KEY_DOWN":
            if key_position >= 1 and key_position < 3:
                key_position += 1
        elif key == "c":
            if key_position == 1:
                #PLAY
                if world_made == True:
                    print("playing..")
                    print(player_world,region_start)
                    src.clear()
                    play(src)
            elif key_position == 2:
                #WORLD
                world_made,player_world,region_start = world(src,BLUE_BLACK,max_y,max_x,[GREEN_BLACK,BLUE_BLACK,BLACK_BLUE])
            elif key_position == 3:
                #QUIT
                curses.endwin()
                break
        
        title(src)
        search_button.string_center("Play")
        add_button.string_center("World")
        remove_button.string_center("Quit")

        if key_position == 1:
            search_button.bg_color(True)
            add_button.bg_color(False)
            remove_button.bg_color(False)
        elif key_position == 2:
            search_button.bg_color(False)
            add_button.bg_color(True)
            remove_button.bg_color(False)
        elif key_position == 3:
            search_button.bg_color(False)
            add_button.bg_color(False)
            remove_button.bg_color(True)

        #border for buttons--
        search_button.border(True)
        add_button.border(True)
        remove_button.border(True)
        search_button.update()
        add_button.update()
        remove_button.update()
        src.refresh()


curses.wrapper(main)