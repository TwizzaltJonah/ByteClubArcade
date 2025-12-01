from import_this import *

image = None

def load():
    global image
    image = graphics.Image(500, 800, win, "games/example_game/icon.png")

def should_close() -> bool:
    return hasKeybindBeenPressed("button3")


def update():
    pass


def unload():
    pass
