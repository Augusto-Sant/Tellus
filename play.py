import curses
from math import sqrt
import random
import sys

import text_tools
import world

class Entity():
    """Entity for play"""
    def __init__(self,name,symbol,x,y):
        self.name = name
        self.symbol = symbol
        self.x = x
        self.y = y
        #
        self.waiting = False
    
    def move(self,x_input,y_input,terrain,obstacles):
        """Move entity towards target"""
        #trying to use pathfinding A* issue: will get stuck in corners or if cursor close..
        nodes = []
        current = (self.y,self.x)
        if current != (y_input,x_input):
            #verify if not obstacle
            #up
            if self.y-1 >= 0:
                if terrain[self.y-1,self.x] not in obstacles:
                    nodes.append((self.y-1,self.x))
            #down
            if self.y+1 <= 38-1:
                if terrain[self.y+1,self.x] not in obstacles:
                    nodes.append((self.y+1,self.x))
            #left
            if self.x-1 >= 0:
                if terrain[self.y,self.x-1] not in obstacles:
                    nodes.append((self.y,self.x-1))
            #right
            if self.x+1 <= 154-1:
                if terrain[self.y,self.x+1] not in obstacles:
                    nodes.append((self.y,self.x+1))
            #up-right
            if self.x+1 <= 154-1 and self.y+1 <= 38-1:
                if terrain[self.y+1,self.x+1] not in obstacles:
                    nodes.append((self.y+1,self.x+1))
            #down-left
            if self.x-1 >= 0 and self.y-1 >= 0:
                if terrain[self.y-1,self.x-1] not in obstacles:
                    nodes.append((self.y-1,self.x-1))
            #up_left
            if self.x-1 >= 0 and self.y+1 <= 38-1:
                if terrain[self.y+1,self.x-1] not in obstacles:
                    nodes.append((self.y+1,self.x-1))
            #down-right
            if self.x+1 <= 154-1 and self.y-1 >= 0:
                if terrain[self.y-1,self.x+1] not in obstacles:
                    nodes.append((self.y-1,self.x+1))

            smaller_f = 9999
            for node in nodes:
                #0=y 1=x
                #distance from node to current
                g = sqrt((current[1]-node[1])**2+(current[0]-node[0])**2)
                #distance from node to end
                h = sqrt((x_input-node[1])**2+(y_input-node[0])**2)
                #total cost
                f = g+h
                if f < smaller_f:
                    smaller_f = f
                    smaller = node
            
            if smaller == (self.y-1,self.x):
                self.y -= 1
            elif smaller == (self.y+1,self.x):
                self.y += 1
            elif smaller == (self.y,self.x-1):
                self.x -= 1
            elif smaller == (self.y,self.x+1):
                self.x += 1
            elif smaller == (self.y+1,self.x+1):
                self.x += 1
                self.y += 1
            elif smaller == (self.y-1,self.x-1):
                self.x -= 1
                self.y -= 1
            elif smaller == (self.y+1,self.x-1):
                self.x -= 1
                self.y += 1
            elif smaller == (self.y-1,self.x+1):
                self.x += 1
                self.y -= 1
    
    def idle(self,terrain,obstacles):
        """Idle random walk for entity"""
        chance = random.randint(1,8)
        
        #up
        if self.y-1 >= 0 and chance == 1:
            if terrain[self.y-1,self.x] not in obstacles:
                self.y -= 1
        #down
        if self.y+1 <= 38-1 and chance == 2:
            if terrain[self.y+1,self.x] not in obstacles:
                self.y += 1
        #left
        if self.x-1 >= 0 and chance == 3:
            if terrain[self.y,self.x-1] not in obstacles:
                self.x -= 1
        #right
        if self.x+1 <= 154-1 and chance == 4:
            if terrain[self.y,self.x+1] not in obstacles:
                self.x += 1
        #up-right
        if self.x+1 <= 154-1 and self.y+1 <= 38-1 and chance == 5:
            if terrain[self.y+1,self.x+1] not in obstacles:
                self.x += 1
                self.y += 1
        #down-left
        if self.x-1 >= 0 and self.y-1 >= 0 and chance == 6:
            if terrain[self.y-1,self.x-1] not in obstacles:
                self.x -= 1
                self.y -= 1
        #up_left
        if self.x-1 >= 0 and self.y+1 <= 38-1 and chance == 7:
            if terrain[self.y+1,self.x-1] not in obstacles:
                self.x -= 1
                self.y += 1
        #down-right
        if self.x+1 <= 154-1 and self.y-1 >= 0 and chance == 8:
            if terrain[self.y-1,self.x+1] not in obstacles:
                self.x += 1
                self.y -= 1

class Surface():
    def __init__(self):
        #terrain is dict
        self.terrain = {}

    def print_terrain(self,main_window,entities):
        """Terrain for play"""
        colors = text_tools.curses_colors()
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
                            #aethetic detail of cursor, invisibility
                            if entity.name == "cursor" and entity.symbol == " ":
                                main_window.addstr(y_axis,x_axis,self.terrain[(row,column)],colors[5])
                            else:
                                main_window.addstr(y_axis,x_axis,entity.symbol,colors[3])
                                main_window.refresh()
                            break
                        else:
                            #ground
                            if self.terrain[(row,column)] == "O":
                                main_window.addstr(y_axis,x_axis,self.terrain[(row,column)],colors[1])
                            elif self.terrain[(row,column)] == "¨":
                                main_window.addstr(y_axis,x_axis,self.terrain[(row,column)],colors[5])
                            else:
                                main_window.addstr(y_axis,x_axis,self.terrain[(row,column)],colors[1])
                else:
                    #ground
                    main_window.addstr(y_axis,x_axis,self.terrain[(row,column)],GREY)
                x_axis += 1
                main_window.refresh()
            y_axis += 1
            x_axis = 1
        main_window.refresh()
        

    def make_terrain(self):
        """generates random terrain"""
        #setup of coordinates and start positions
        for row in range(38):
            for column in range(154):
                if random.randint(0,100) == 100:
                    self.terrain.update({(row,column):"O"})
                else:
                    #ground
                    self.terrain.update({(row,column):"¨"})
        
        #this is for mountains
        # for row in range(38):
        #     for column in range(154):
        #         if row > 1 and column > 1 and row < 38-1 and column < 154-1:
        #             if ((self.terrain[(row-1,column)] == "O") or (self.terrain[(row,column-1)] == "O")
        #             or (self.terrain[(row+1,column)] == "O") or (self.terrain[(row,column+1)] == "O")):
        #                 if random.randint(0,50) > 48:
        #                     self.terrain.update({(row,column):"O"})

class Settlement():
    def __init__(self,name,start_region,chosen_race,population):
        self.name = name
        self.start_region = start_region
        self.population = population
        #pops
        self.race_symbol = chosen_race[0]
        #resources--
        self.food = 0
        self.wood = 0
    
    def create_population(self):
        """Creates entities in range of self.population"""
        entities = []
        #cursor is an entity, but first so its always on top
        cursor = Entity("cursor","X",0,0)
        entities.append(cursor)
        for i in range(self.population):
            entities.append(Entity(str(i),self.race_symbol,1,1))
        return entities,cursor

def run(main_window,player_world,region_start,settlement_name,chosen_race):
    """Plays the main game inside a previously created world."""
    BLACK_WHITE,RED_BLACK,BLACK_RED,BLUE_BLACK,BLACK_BLUE,GREEN_BLACK = text_tools.curses_colors()
    max_y,max_x = main_window.getmaxyx()
    curses.curs_set(0)
    settlement = Settlement(settlement_name,region_start,chosen_race,population=3)
    entities,cursor = settlement.create_population()
    #initialize surface
    surface = Surface()
    surface.make_terrain()
    main_window.nodelay(True)
    #commands
    call_position = []
    cut_tree_position = []
    build_position = []
    #
    cut_tree_entity = ""
    build_entity = ""
    #obstacles list
    obstacles = ["#","O"]
    while True:
        #TEXTS
        main_window.border()
        main_window.addstr(max_y-1,1,"(q) to quit",RED_BLACK)
        main_window.addstr(0,27,"(p) to pause",BLUE_BLACK)
        main_window.addstr(0,47,f"{settlement_name}",BLUE_BLACK)
        main_window.addstr(0,57,f"region:{region_start}",BLUE_BLACK)
        main_window.addstr(0,77,f"Food:{settlement.food}",RED_BLACK)
        main_window.addstr(0,87,f"Wood:{settlement.wood}",RED_BLACK)
        #
        cursor.symbol = " "
        curses.napms(180)
        surface.print_terrain(main_window,entities)
        #activate cursor
        key = main_window.getch()
        if key == ord("p"):
            cursor.symbol = "X"
            main_window.nodelay(False)
            cursor_key = ""
            while cursor_key != "p":
                main_window.addstr(0,27,"    PAUSED    ",BLACK_BLUE)
                commands_show = curses.newwin(5,45,0,(max_x//2)+20)
                commands_show.addstr(2,2,"(c) to call   (b) to cut tree",GREEN_BLACK)
                commands_show.border()
                commands_show.refresh()
                cursor_key = main_window.getkey()
                if cursor_key == ("KEY_UP"):
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
                    call_position.clear()
                    call_position.append(cursor.x)
                    call_position.append(cursor.y)
                    #count if majority of entities arrived
                    in_position_count = 0
                elif cursor_key == "b":
                    cut_tree_position.append(cursor.x)
                    cut_tree_position.append(cursor.y)
                    cut_tree_position_count = 0
                    cut_tree_entity = entities[random.randint(1,settlement.population)]
                elif cursor_key == "e":
                    build_position.append(cursor.x)
                    build_position.append(cursor.y)
                    build_position_count = 0
                    build_entity = entities[random.randint(1,settlement.population)]
                elif cursor_key == "q":
                    curses.endwin()
                    sys.exit()
                surface.print_terrain(main_window,entities)
                main_window.refresh()
            main_window.clear()
            #reprint after pause
            surface.print_terrain(main_window,entities)
            main_window.border()
            main_window.addstr(max_y-1,1,"(q) to quit",RED_BLACK)
            main_window.addstr(0,27,"(p) to pause",BLUE_BLACK)
            main_window.addstr(0,47,f"{settlement_name}",BLUE_BLACK)
            main_window.addstr(0,57,f"region: {region_start}",BLUE_BLACK)
            main_window.refresh()
            #
            main_window.nodelay(True)
        elif key == ord("q"):
            main_window.nodelay(False)
            curses.endwin()
            main_window.clear()
            break
        
        #CUT TREE MECHANIC--
        if len(cut_tree_position) > 0 and cut_tree_entity != "":
            if surface.terrain[(cut_tree_position[1],cut_tree_position[0])] == "O":
                cut_x = 0
                cut_y = 0
                if  cut_tree_position[0]-1 > 0:
                    if surface.terrain[(cut_tree_position[1],cut_tree_position[0]-1)] not in obstacles:
                        cut_x = -1
                elif cut_tree_position[0]+1 <= 38-1:
                    if surface.terrain[(cut_tree_position[1],cut_tree_position[0]+1)] not in obstacles:
                        cut_x = 1
                elif cut_tree_position[1]-1 > 0:
                    if surface.terrain[(cut_tree_position[1]-1,cut_tree_position[0])] not in obstacles:
                        cut_y = -1
                elif cut_tree_position[1]-1 <= 154-1:
                    if surface.terrain[(cut_tree_position[1]+1,cut_tree_position[0])] not in obstacles:
                        cut_y = 1

                cut_tree_entity.move(cut_tree_position[0]+(cut_x),cut_tree_position[1]+(cut_y),surface.terrain,obstacles)
                
                if (cut_tree_entity.x == cut_tree_position[0]+(cut_x) 
                and cut_tree_entity.y == cut_tree_position[1]+(cut_y)):
                    cut_tree_position_count += 1
                
                if cut_tree_position_count >= 1:
                    #(y,x)
                    surface.terrain.update({(cut_tree_position[1],cut_tree_position[0]):"¨"})
                    settlement.wood += 10
                    cut_tree_position.clear()
                    cut_tree_entity = ""
            else:
                cut_tree_position.clear()
                cut_tree_entity = ""
        #BUILD IN POSITION MECHANIC--
        if len(build_position) > 0 and build_entity != "":
            if surface.terrain[(build_position[1],build_position[0])] == "¨":
                build_x = 0
                build_y = 0
                if  build_position[0]-1 > 0:
                    if surface.terrain[(build_position[1],build_position[0]-1)] not in obstacles:
                        build_x = -1
                elif build_position[0]+1 <= 38-1:
                    if surface.terrain[(build_position[1],build_position[0]+1)] not in obstacles:
                        build_x = 1
                elif build_position[1]-1 > 0:
                    if surface.terrain[(build_position[1]-1,build_position[0])] not in obstacles:
                        build_y = -1
                elif build_position[1]-1 <= 154-1:
                    if surface.terrain[(build_position[1]+1,build_position[0])] not in obstacles:
                        build_y = 1

                build_entity.move(build_position[0]+(build_x),build_position[1]+(build_y),surface.terrain,obstacles)
                
                if (build_entity.x == build_position[0]+(build_x) 
                and build_entity.y == build_position[1]+(build_y)):
                    build_position_count += 1
                
                if build_position_count >= 1:
                    #(y,x)
                    surface.terrain.update({(build_position[1],build_position[0]):"#"})
                    settlement.wood -= 2
                    build_position.clear()
                    build_entity = ""
            else:
                build_position.clear()
                build_entity = ""
        
        for entity in entities:
            if (len(call_position) > 0 and entity.name != "cursor" 
            and entity != cut_tree_entity and entity != build_entity):
                #MOVE TO CALL issue: not checking all correctly
                entity.move(call_position[0],call_position[1],surface.terrain,obstacles)
                if (entity.x == call_position[0] and entity.y == call_position[1] and entity.waiting == False):
                    in_position_count += 1
                    entity.waiting = True
                
                if in_position_count >= len(entities)-1:
                    call_position.clear()
                    entity.waiting = False
            else:
                entity.waiting = False
                if (entity.name != "cursor" and entity != cut_tree_entity and entity != build_entity 
                and entity.waiting == False):
                    entity.idle(surface.terrain,obstacles)