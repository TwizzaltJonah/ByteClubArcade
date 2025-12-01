import math

import graphics as g

win: g.Window = None
kbm = True

joystick_angle = 0
joystick_magnitude = 0

prev_joystick_angle = 0
prev_joystick_magnitude = 0


class Keybinding:

    def __init__(self, name: str, key: str):
        self.name = name
        self.key = key
        self.down = False
        self.prevDown = False


keybindings = (
    Keybinding("button1", "h"),
    Keybinding("button2", "j"),
    Keybinding("button3", "k"),
    Keybinding("button4", "l")
)


def update():
    global joystick_angle, joystick_magnitude, prev_joystick_angle, prev_joystick_magnitude

    prev_joystick_magnitude = joystick_magnitude
    prev_joystick_angle = joystick_angle

    if kbm:

        joystick_x = int(win.isKeyPressed("d")) - int(win.isKeyPressed("a"))
        joystick_y = int(win.isKeyPressed("s")) - int(win.isKeyPressed("w"))
        joystick_angle = math.degrees(math.atan2(joystick_y, joystick_x)) % 360.0
        if joystick_x == 0 and joystick_y == 0:
            joystick_magnitude = 0
        else:
            joystick_magnitude = 1

        for keybind in keybindings:
            keybind.prevDown = keybind.down
            keybind.down = win.isKeyPressed(keybind.key)

    else:
        pass

def getJoystickQuadrant():
    return ((joystick_angle + 45.0) % 360) // 90

def hasJoystickChangedDirections():
    return (joystick_magnitude != 0 and
            ((joystick_magnitude != 0 and prev_joystick_magnitude == 0) or
             ((joystick_angle + 45.0) % 360) // 90 != ((prev_joystick_angle + 45.0) % 360) // 90))

def get_joystick_angle():
    return joystick_angle

def get_joystick_magnitude():
    return joystick_magnitude

# the first frame when its first being pressed
def isKeybindFirstPressed(name: str):
    for i in keybindings:
        if i.name == name and i.down and not i.prevDown:
            return True
    return False

# when it has been pressed (just released)
def hasKeybindBeenPressed(name: str):
    for i in keybindings:
        if i.name == name and not i.down and i.prevDown:
            return True
    return False

def isKeybindDown(name: str):
    for i in keybindings:
        if i.name == name and i.down:
            return True
    return False
