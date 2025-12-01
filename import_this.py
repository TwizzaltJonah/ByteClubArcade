import graphics
from inputs import (hasJoystickChangedDirections,
                    get_joystick_angle,
                    get_joystick_magnitude,
                    hasKeybindBeenPressed,
                    isKeybindFirstPressed,
                    isKeybindDown)

win: graphics.Window = None
frame_time = 0.005
