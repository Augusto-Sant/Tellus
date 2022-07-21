import text_tools
import curses
import world
import play

def main_menu(src):
    """Main menu"""
    max_y,max_x = src.getmaxyx()
    key_position = 2
    #hide cursor
    curses.curs_set(0)
    BLACK_WHITE,RED_BLACK,BLACK_RED,BLUE_BLACK,BLACK_BLUE,GREEN_BLACK = text_tools.curses_colors()
    src.border()

    search_button = text_tools.Button(src,"search",5,15,8,3,BLACK_BLUE)
    search_button.create()
    add_button = text_tools.Button(src,"add",5,15,13,3,BLACK_BLUE)
    add_button.create()
    remove_button = text_tools.Button(src,"remove",5,15,18,3,BLACK_RED)
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
                    src.clear()
                    src.addstr((max_y//2)-10,(max_x//2)-15,
                    f"Creating starting region: {region_start} in {player_world.name}",BLACK_BLUE)
                    src.refresh()
                    curses.napms(800)
                    src.clear()
                    play.run(src,player_world,region_start)
            elif key_position == 2:
                #WORLD
                world_made,player_world,region_start = world.world(src,BLUE_BLACK,max_y,max_x,[GREEN_BLACK,BLUE_BLACK,
                BLACK_BLUE])
            elif key_position == 3:
                #QUIT
                curses.endwin()
                break
        
        text_tools.title(src)
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

def run():
    """Wraps and runs Main Menu"""
    curses.wrapper(main_menu)