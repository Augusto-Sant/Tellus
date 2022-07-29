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

    search_button = text_tools.Button(src,"search",5,15,14,65,BLACK_BLUE)
    search_button.create()
    add_button = text_tools.Button(src,"add",5,15,19,65,BLACK_BLUE)
    add_button.create()
    remove_button = text_tools.Button(src,"remove",5,15,24,65,BLACK_RED)
    remove_button.create()
    src.refresh()
    #world init
    world_made = False
    while True:
        #text in screen
        text_tools.title(src)
        search_button.string_center("Play")
        add_button.string_center("World")
        remove_button.string_center("Quit")
        #border for buttons--
        src.border()
        src.addstr(max_y-1,1,"(q) to quit",RED_BLACK)
        src.addstr(0,1,"(c) to choose",BLUE_BLACK)
        search_button.border(True)
        add_button.border(True)
        remove_button.border(True)
        search_button.update()
        add_button.update()
        remove_button.update()
        src.refresh()
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
                    src.addstr((max_y//2)-14,(max_x//2)-17,
                    f"Creating starting region: {region_start} in {player_world.name}",BLACK_BLUE)
                    src.addstr((max_y//2)-7,(max_x//2)-15,"Settlement Name (CTRL+G) to save:",BLUE_BLACK)
                    src.refresh()
                    settlement_name = (text_tools.game_input(src,GREEN_BLACK,max_y,max_x,5,20)).strip()
                    src.refresh()
                    src.clear()
                    #RACE CHOICE
                    final_race_position = ""
                    race_key_position = 1
                    src.addstr((max_y//2)-7,(max_x//2)-15,"CHOOSE RACE (UP-DOWN) (c) to choose:",BLUE_BLACK)
                    src.refresh()
                    while final_race_position == "":
                        race_key = src.getkey()
                        if race_key == "KEY_UP":
                            if race_key_position > 1 and race_key_position <= len(player_world.used_races):
                                race_key_position -= 1
                        elif race_key == "KEY_DOWN":
                            if race_key_position >= 1 and race_key_position < len(player_world.used_races):
                                race_key_position += 1
                        elif race_key == "c":
                            final_race_position = race_key_position
                        
                        for i,race in enumerate(player_world.used_races,start=1):
                            
                            if race_key_position == i:
                                src.clear()
                                src.addstr((max_y//2)-7,(max_x//2)-15,"CHOOSE RACE (UP-DOWN) (c) to choose:",BLUE_BLACK)
                                src.addstr((max_y//2)-5,(max_x//2)-15,f"{race.capitalize()}",BLACK_BLUE)
                            src.refresh()
                        
                            if final_race_position == i:
                                chosen_race = race
                    
                    src.clear()
                    #
                    src.refresh()
                    curses.napms(800)
                    src.clear()
                    play.run(src,player_world,region_start,settlement_name,chosen_race)
            elif key_position == 2:
                #WORLD
                world_made,player_world,region_start = world.world(src,max_y,max_x)
            elif key_position == 3:
                #QUIT
                curses.endwin()
                break

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

def run():
    """Wraps and runs Main Menu"""
    curses.wrapper(main_menu)