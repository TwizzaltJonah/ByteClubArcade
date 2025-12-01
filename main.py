import menu
import game_handler
import graphics as g
import inputs

is_running = True
is_in_game = False

win: g.Window = None

def initialize():
    global win
    win = g.Window(1920, 1080)
    win.setBackground((0, 0, 0))
    menu.win = win
    inputs.win = win
    game_handler.win = win
    menu.initialize()


def update():
    global is_in_game

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
