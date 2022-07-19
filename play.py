import curses
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
    
    def move(self,main_window,x_input,y_input):
        """Move entity towards (x,y)"""
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
        """Idle random walk for entity"""
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

def terrain(main_window,max_y,max_x,entities):
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
                            main_window.addstr(y_axis,x_axis,"¨",GREY)
                        else:
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

def run(main_window):
    """Plays the main game inside a previously created world."""
    BLACK_WHITE,RED_BLACK,BLACK_RED,BLUE_BLACK,BLACK_BLUE,GREEN_BLACK = text_tools.curses_colors()
    max_y,max_x = main_window.getmaxyx()
    main_window.border()
    main_window.addstr(max_y-1,1,"(q) to quit",RED_BLACK)
    main_window.addstr(0,1,"(c) to Call",BLUE_BLACK)
    main_window.addstr(0,25,"(.) to pass time",BLUE_BLACK)
    main_window.getkey()
    curses.curs_set(0)
    #creation of pops
    entity1 = Entity("1","e",1,1)
    entity2 = Entity("2","d",5,10)
    entity3 = Entity("3","u",6,10)
    #cursor is an entity, but first so its always on top
    cursor = Entity("cursor","X",0,0)
    entities = [cursor,entity1,entity2,entity3]
    main_window.nodelay(True)
    while True:
        cursor.symbol = " "
        curses.napms(200)
        terrain(main_window,max_y,max_x,entities)
        #activate cursor
        key = main_window.getch()
        if key == ord("p"):
            cursor.symbol = "X"
            main_window.nodelay(False)
            cursor_key = ""
            while cursor_key != "p":
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
                    for entity in entities:
                        entity.move(main_window,cursor.x,cursor.y)
                elif cursor_key == "q":
                    curses.endwin()
                    sys.exit()
                terrain(main_window,max_y,max_x,entities)
                main_window.refresh()
            main_window.refresh()  
            main_window.nodelay(True)
        elif key == ord("q"):
            main_window.nodelay(False)
            curses.endwin()
            main_window.clear()
            break


        for entity in entities:
            if entity.name != "cursor":
                entity.idle()
