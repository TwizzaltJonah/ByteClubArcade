import time

import menu
import game_handler
import graphics as g
import inputs
import import_this

is_running = True
is_in_game = False

win: g.Window = None

prev_frame_time = 0.0

def initialize():
    global win, prev_frame_time
    win = g.Window(1920, 1080)
    win.setBackground((0, 0, 0))
    menu.win = win
    inputs.win = win
    game_handler.win = win
    menu.initialize()
    prev_frame_time = time.time()

def update():
    global is_in_game, prev_frame_time

    win.update()

    inputs.update()

    if is_in_game:

        if game_handler.should_close():
            game_handler.unload()
            menu.load()
            is_in_game = False
        else:
            game_handler.update()

    else:

        game = menu.game_to_play()
        if game != "":
            menu.unload()
            game_handler.load(game)
            is_in_game = True
        else:
            menu.update()

    now = time.time()
    import_this.frame_time = now - prev_frame_time
    prev_frame_time = now
    # print(import_this.frame_time)

def main():
    initialize()

    while is_running:
        update()

    if is_in_game:
        game_handler.unload()
    else:
        menu.unload()


if __name__ == '__main__':
    main()
