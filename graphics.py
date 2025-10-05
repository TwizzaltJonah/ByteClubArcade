import pygame
import math
import os

# Initialize Pygame
# =================================================================================================
pygame.init()


# Global Variables
# =================================================================================================

# Basic colors to be added
COLOR_MAP = {
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255, 255),
    "RED": (255, 0, 0),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255),
    "YELLOW": (255, 255, 0),
    "CYAN": (0, 255, 255),
    "MAGENTA": (255, 0, 255),
    "GRAY": (128, 128, 128)
}

# Special keys that can be pressed
KEY_MAP = {
    "space": pygame.K_SPACE,
    "enter": pygame.K_RETURN,
    "return": pygame.K_RETURN,
    "left": pygame.K_LEFT,
    "right": pygame.K_RIGHT,
    "up": pygame.K_UP,
    "down": pygame.K_DOWN,
    "shift": pygame.K_LSHIFT,
    "ctrl": pygame.K_LCTRL,
    "alt": pygame.K_LALT,
    "tab": pygame.K_TAB,
    "backspace": pygame.K_BACKSPACE
}

# Modes and Options used
# =================================================================================================
VALID_MODES = ("CENTER", "CORNER")


# Errors Messages to be used
# =================================================================================================
NEGATIVE_VALUE = "Value must be a positive number."
INVALID_COLOR_OPTION = "Color must be an rgb tuple"
INVALID_MODE = "Mode must be CENTER or CORNER."
INVALID_BOOL = "Value must be a boolean (True or False)."
INVALID_POLYGON_POINTS = "Points must be entered as a list of tuples. Ex-[(1, 2), (3, 4), ...]"


# Helper Classes
# =================================================================================================
class GraphicsError(Exception):
    """Base class for errors in the graphics module."""
    pass


# Helper Functions
# =================================================================================================
def invalidValueCheck(*args, zero=False):
    """Function to be used to check if certain arguments are valid based when
    creating objects are using object methods."""
    for arg in args:
        if not isinstance(arg, (int, float)):
            raise GraphicsError(f"Expected an int or float. Instead received {arg}.")
        elif arg < 0:
            raise GraphicsError(NEGATIVE_VALUE)
        elif arg == 0 and not zero:
            raise GraphicsError("Value must be greater than 0.")



# Sound/Music Classes
# =================================================================================================
"""Pygame handles smaller sound files and larger music files differently. For efficiency purposes
when needing a smaller sound effect create a Sound object whereas needing to use a larger file
for background music use Music."""
class Sound:
    def __init__(self, file, loop=0):
        """Creates a sound object. Loops is how many times the sound plays.
        -1 means the sound loops indefinitely."""
        self.loop = loop
        self.sound = pygame.mixer.Sound(file)

    def play(self):
        self.sound.play(self.loop)

    def stop(self):
        self.sound.stop()


class Music(Sound):
    def __init__(self, file, loop=0):
        super().__init__(file, loop)


# Graphics Classes
# =================================================================================================
class Window:
    def __init__(self, width, height, title="Graphics Window"):
        pygame.init()
        invalidValueCheck(width, height)
        self.width = width
        self.height = height
        self.title = title
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.running = True
        self.clock = pygame.time.Clock()
        self.__startTime = pygame.time.get_ticks()
        self.elapsedTime = 0
        self.events = []   # List of events for event handling
        self.objects = []   # List of objects to be drawn on the screen
        self.keys_pressed = set()
        self.backgroundColor = (255, 255, 255)
        # self.EDGES = []

    def setBackground(self, color):
        """Sets the background of the screen to the color provided"""
        if isinstance(color, str):
            # If the color is a simple string use the color map above to grab the RGB values
            self.backgroundColor = COLOR_MAP.get(color.upper(), (0, 0, 0))
        else:
            self.backgroundColor = color

    def addObject(self, obj):
        """Method to be used upon the creation of a Graphics Object."""
        self.objects.append(obj)

    def removeObject(self, obj):
        """Method to be used when a Graphics Object is to be destroyed"""
        if obj in self.objects:
            self.objects.remove(obj)

    def update(self):
        """Updates the screen to show all objects that are to be drawn"""
        self.screen.fill(self.backgroundColor)
        # for obj in self.objects:
        #     if obj.getVisibility():
        #         obj.draw()
        # pygame.display.flip()
        self.clock.tick(60)
        self.events = pygame.event.get()
        self._updateKeys()
        self._updateRunningTime()
        pygame.display.update()
        self.close()

    def _updateKeys(self):
        """Internal method that grabs all keys that are being used by the user"""
        for event in self.events:
            if event.type == pygame.KEYDOWN:
                self.keys_pressed.add(event.key)
            elif event.type == pygame.KEYUP:
                self.keys_pressed.discard(event.key)

    def isKeyPressed(self, key):
        """Checks to see if key is being pressed"""
        if isinstance(key, str):
            key = key.lower()
            if len(key) == 1:
                keyCode = ord(key)
            else:
                keyCode = KEY_MAP.get(key)
            return keyCode in self.keys_pressed
        return key in self.keys_pressed

    def isMouseClicked(self, button):
        """Checks to see if button is being clicked by the user"""
        button_map = {
            "LEFT": 1,
            "MIDDLE": 2,
            "RIGHT": 3
        }
        for event in self.events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == button_map.get(button.upper(), 0):
                return True
        return False

    def getMousePosition(self):
        """Returns the position of the mouse"""
        return pygame.mouse.get_pos()

    def getPixelColor(self, x, y):
        """Returns the RGB value of the pixel at position (x,y)"""
        return self.screen.get_at((x, y))[:3]

    def getWidth(self):
        """Returns the width of the window"""
        return self.width

    def getHeight(self):
        """Returns the height of the window"""
        return self.height

    def close(self):
        """Checks to see if the user wants to close the Window"""
        for event in self.events:
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()

    def _updateRunningTime(self):
        self.elapsedTime = (pygame.time.get_ticks() - self.__startTime) // 1000

class GraphicsObject:
    def __init__(self, window, color=(255, 255, 255), visible=True, outlineWidth=1, outlineColor="BLACK"):
        self.window = window
        self.visible = visible
        self.color = color
        self.outlineWidth = outlineWidth
        self.outlineColor = outlineColor
        self.window.addObject(self)

    def getVisibility(self):
        """Gets the visibility of a GraphicsObject"""
        return self.visible

    def setVisibility(self, boolean):
        """Sets the visibility of a GraphicsObject.
        If True then the object is to be drawn and if False then it is not to be drawn."""
        if not isinstance(boolean, bool):
            raise GraphicsError(INVALID_BOOL)
        self.visible = boolean

    def setFill(self, color):
        """Sets the fill for a GraphicsObject"""
        self.color = color

    def setOutlineColor(self, color):
        """Sets the Outline color for a GraphicsObject. In order to see the Outline color the user must also have
        changed the outline width which is 0 by default."""
        self.outlineColor = color

    def setOutlineWidth(self, width):
        """Sets the Width of the Outline for a GraphicsObject."""
        self.outlineWidth = width


class Point(GraphicsObject):
    def __init__(self, x, y, window):
        super().__init__(window)
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

class Circle(GraphicsObject):
    def __init__(self, x, y, radius, window, color=(255, 255, 255), outlineWidth=0, outlineColor="BLACK"):
        super().__init__(window, color=color, outlineWidth=outlineWidth, outlineColor=outlineColor)
        invalidValueCheck(radius)
        self.x = x
        self.y = y
        self.radius = radius
        self.fillSurface = pygame.Surface((radius * 2, radius * 2))
        # self.fillSurface.fill(self.color)
        self.outlineSurface = pygame.Surface((radius * 2, radius * 2))
        # self.outlineSurface.fill(self.outlineColor)
        self.fillSurface.set_colorkey((0, 0, 0))
        self.outlineSurface.set_colorkey((0, 0, 0))
        self.fillSurface.set_alpha(255)
        self.outlineSurface.set_alpha(255)

    def draw(self):
        """Draws the Circle. First pass is the Circle itself if the user has not changed the outline width.
        The second is to draw a second circle at the same position with the outline changed and no fill color."""
        # pygame.draw.circle(self.window.screen, self.color, (self.x, self.y), self.radius)
        #
        # if self.outlineWidth != 0:
        #     pygame.draw.circle(self.window.screen, self.outlineColor, (self.x, self.y), self.radius, width=self.outlineWidth)

        pygame.draw.circle(self.fillSurface, self.color, (0.5 * self.radius, 0.5 * self.radius), self.radius)
        self.window.screen.blit(self.fillSurface, (self.x - 0.5 * self.radius, self.y - 0.5 * self.radius))
        if self.outlineWidth != 0:
            pygame.draw.circle(self.outlineSurface, self.outlineColor, (0.5 * self.radius, 0.5 * self.radius), self.radius, self.outlineWidth)
            self.window.screen.blit(self.outlineSurface, (self.x - 0.5 * self.radius, self.y - 0.5 * self.radius))


    def move(self, dx, dy):
        """Moves the Circle by dx and dy"""
        self.x += dx
        self.y += dy

    def setCenter(self, x, y):
        self.x = x
        self.y = y


class Rectangle(GraphicsObject):
    def __init__(self, x, y, width, height, window, color=(255, 255, 255), outlineWidth=0, outlineColor="BLACK",
                 mode="CORNER"):
        super().__init__(window, color=color, outlineWidth=outlineWidth, outlineColor=outlineColor)
        self.x = x
        self.y = y
        invalidValueCheck(width, height)
        self.width = width
        self.height = height
        self.mode = mode
        self.edges = {}

    def draw(self):
        """Draws the Rectangle. First pass is the Rectangle itself if the user has not changed the outline width.
                The second is to draw a second Rectangle at the same position with the outline changed and no fill color."""
        if self.mode == "CORNER":
            pygame.draw.rect(self.window.screen, self.color, (self.x, self.y, self.width, self.height))
            if self.outlineWidth != 0:
                pygame.draw.rect(self.window.screen, self.outlineColor, (self.x, self.y, self.width, self.height),
                                 width=self.outlineWidth)

        if self.mode == "CENTER":
            pygame.draw.rect(self.window.screen, self.color, (self.x - self.width / 2, self.y - self.height / 2,
                                                              self.width, self.height))
            if self.outlineWidth != 0:
                pygame.draw.rect(self.window.screen, self.outlineColor, (self.x - self.width / 2, self.y - self.height / 2,
                                 self.width, self.height), width=self.outlineWidth)

    def setMode(self, mode):
        """Sets the Mode of a Rectangle to either CENTER or CORNER. This determines if the coordinate pair is the
        center of the Rectangle or the top-left corner of the Rectangle."""
        if mode.upper() not in VALID_MODES:
            raise GraphicsError(INVALID_MODE)
        self.mode = mode.upper()

    def move(self, dx, dy):
        """Moves the Rectangle by dx and dy"""
        self.x += dx
        self.y += dy

    def setCoords(self, x, y):
        """Sets the coordinate pair of (x,y) to the new coordinates passed."""
        self.x = x
        self.y = y

    def collidesWith(self, other):
        """Checks to see the Rectangle has collided with another Graphics Object.
        Currently only supports other Rectangles, Circles, and Points."""
        if isinstance(other, Rectangle):
            pass
        elif isinstance(other, Circle):
            pass
        elif isinstance(other, Point):
            pass



class Arc(GraphicsObject):
    def __init__(self,  x, y, width, height, startAngle, endAngle, window, outlineWidth=1, outlineColor="BLACK"):
        super().__init__(window, outlineWidth=outlineWidth, outlineColor=outlineColor)
        self.x = x
        self.y = y
        invalidValueCheck(width, height)
        self.width = width
        self.height = height
        self.startAngle = startAngle * math.pi / 180
        self.endAngle = endAngle * math.pi / 180


    def draw(self):
        """Draws the Arc"""
        pygame.draw.arc(self.window.screen, self.outlineColor, (self.x - self.width /2 , self.y - self.height / 2,
                        self.width, self.height), self.startAngle, self.endAngle, width=self.outlineWidth)

    def move(self, dx, dy):
        """Moves the Arc by dx and dy"""
        self.x += dx
        self.y += dy

class Ellipse(GraphicsObject):
    def __init__(self, x, y, width, height, window, color=(255, 255, 255), outlineWidth=0, outlineColor="BLACK"):
        super().__init__(window, color=color, outlineWidth=outlineWidth, outlineColor=outlineColor)
        self.x = x
        self.y = y
        invalidValueCheck(width, height)
        self.width = width
        self.height = height

    def draw(self):
        """Draws the Ellipse"""
        pygame.draw.ellipse(self.window.screen, self.color, (self.x - self.width /2 , self.y - self.height / 2, self.width, self.height))

    def move(self, dx, dy):
        """Moves the Ellipse by dx and dy"""
        self.x += dx
        self.y += dy

class Polygon(GraphicsObject):
    def __init__(self, points, window):
        super().__init__(window)
        if not isinstance(points, (list, tuple)):
            raise GraphicsError(INVALID_POLYGON_POINTS)
        self.points = list(points)

    def draw(self):
        pygame.draw.polygon(self.window.screen, self.color, self.points)

    def move(self, dx, dy):
        """Moves the Polygon by dx and dy"""
        for i in range(len(self.points)):
            self.points[i] = [self.points[i][0] + dx, self.points[i][1] + dy]

class Line(GraphicsObject):
    def __init__(self, x1, y1, x2, y2, window, color=(0, 0, 0), outlineWidth=1):
        super().__init__(window, color=color, outlineWidth=outlineWidth)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def draw(self):
        pygame.draw.line(self.window.screen, self.color, (self.x1, self.y1), (self.x2, self.y2), width=self.outlineWidth)

    def move(self, dx, dy):
        """Moves the Lines by dx and dy"""
        self.x1 += dx
        self.x2 += dx
        self.y1 += dy
        self.y2 += dy

class Text(GraphicsObject):
    def __init__(self, x, y, window, color=(0, 0, 0), mode="CORNER", fontSize=12):
        super().__init__(window, color=color)
        self.x = x
        self.y = y
        invalidValueCheck(fontSize)
        self.fontSize = fontSize
        self.mode = mode
        self.text = pygame.font.Font(None, self.fontSize)
        self.str = ""

    def setText(self, str):
        """Sets the Text of a Text object"""
        self.str = str

    def setSize(self, size):
        """Sets the Font size of the Text Object"""
        invalidValueCheck(size)
        self.fontSize = size

    def setMode(self, mode):
        """Sets the Mode of a Text Object to either CENTER or CORNER. This determines if the coordinate pair is the
        center of the Text Box or the top-left corner of the Text Box."""
        if mode.upper() not in VALID_MODES:
            raise GraphicsError(INVALID_MODE)
        self.mode = mode.upper()

    def draw(self):
        """Draws the Text object"""
        textSurface = self.text.render(self.str, True, self.color)
        if self.mode == "CORNER":
            self.window.screen.blit(textSurface, (self.x, self.y))
        else:
            self.window.screen.blit(textSurface, textSurface.get_rect(center=(self.x, self.y)))


class Image(GraphicsObject):
    def __init__(self, x, y, window, file, transparent=False):
        super().__init__(window)
        self.x = x
        self.y = y
        self.file = file
        self.transparent = transparent
        self.image = self._createImage()


    def _createImage(self):
        """Creates the Image object. If the image has a transparent background use convert_alpha otherwise convert.
        This is for efficiency purposes within pygame."""
        if self.transparent:
            return pygame.image.load(self.file).convert_alpha()
        return pygame.image.load(self.file).convert()

    def draw(self):
        """Draws the Image"""
        self.window.screen.blit(self.image, self.image.get_rect(center=(self.x, self.y)))

    def resizeImage(self, width, height):
        """Resizes the image to the width and height passed to the function."""
        invalidValueCheck(width, height)
        self.image = pygame.transform.scale(self.image, (width, height))

    def scaleImage(self, scalar):
        """Scales the size of the image based on the scalar passes to the function."""
        invalidValueCheck(scalar)
        width, height = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (width * scalar, height * scalar))

    def getHeight(self):
        """Returns the height of the image."""
        return self.image.get_size()[1]

    def getWidth(self):
        """Returns the width of the image."""
        return self.image.get_size()[0]

    def rotateImage(self, degrees):
        """Rotates the image by degrees."""
        if not isinstance(degrees, (int, float)):
            raise GraphicsError(f"Expected int or float. Instead received {degrees}")
        self.image = pygame.transform.rotate(self.image, degrees)

    def flipVertically(self):
        """Flips the image vertically."""
        self.image = pygame.transform.flip(self.image, False, True)

    def flipHorizontally(self):
        """Flips the image horizontally."""
        self.image = pygame.transform.flip(self.image, True, False)

    def move(self, dx, dy):
        """Moves the image by dx and dy."""
        self.x += dx
        self.y += dy



def testFunction():
    win = Window(600, 400)
    circ = Circle(200, 200, 50, win)
    circ.setFill("RED")
    while win.running:
        circ.draw()
        win.update()


if __name__ == '__main__':
    testFunction()