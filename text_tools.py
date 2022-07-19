import curses
from curses import textpad

class Button():
    """Standard button to be used"""
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
        """Creates a border for button"""
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
    """Title screen in Menu"""
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
