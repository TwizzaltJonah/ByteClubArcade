import menu
import game_handler

is_running = True
is_in_game = False

def initialize():
    pass


def update():
    global is_in_game

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
    menu.load()

    while is_running:
        update()

    if is_in_game:
        game_handler.unload()
    else:
        menu.unload()


if __name__ == '__main__':
    main()
