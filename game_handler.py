import importlib.util
import sys
import traceback
import gc

debug_mode = True
error_occurred = False
game_closed = False
game = None
game_name = "No game"

modules = {}

def handle_game_error(e):
    global game, error_occurred, game_name

    error_occurred = True

    if debug_mode:
        print("ERROR (" + game_name + "): " + str(e))
        traceback.print_exc()

        print("\nAttempting unload:\n")

    try:
        game.unload()
        if debug_mode:
            print("Unload successful\n")
    except Exception:
        if debug_mode:
            print("Unload unsuccessful\n")

    try:
        for i in sys.modules.copy():
            if i not in modules:
                sys.modules[i].__dict__.clear()
                sys.modules.pop(i)
        gc.collect()
    except Exception:
        if debug_mode:
            print("Unimport unsuccessful\n")

    game = None
    game_name = "No game"


def should_close():
    return error_occurred or game_closed


def load(new_game_name: str):
    global game, game_name, error_occurred, game_closed, modules

    try:
        game_name = new_game_name
        error_occurred = False
        game_closed = False

        modules = sys.modules.copy()

        spec = importlib.util.spec_from_file_location("game", "games/" + new_game_name + "/" + new_game_name + ".py")
        game = importlib.util.module_from_spec(spec)
        sys.modules["game"] = game
        spec.loader.exec_module(game)

        game.load()
    except Exception as e:
        handle_game_error(e)


def unload():
    global game, game_name, game_closed

    if not error_occurred:
        try:
            game.unload()

            for i in sys.modules.copy():
                if i not in modules:
                    sys.modules[i].__dict__.clear()
                    sys.modules.pop(i)
            gc.collect()

            game = None
            game_name = "No game"
            game_closed = True

        except Exception as e:
            handle_game_error(e)

def update():
    global game_closed

    try:
        if game.should_close():
            game_closed = True
        else:
            game.update()

    except Exception as e:
        handle_game_error(e)
