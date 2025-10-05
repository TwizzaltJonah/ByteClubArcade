import math

import graphics as g
import time

last60frametime = time.time()
frameNum = 0

win = g.Window(600, 400)

img = g.Image(300, 200, win, "test.png", True)
img.resizeImage(160, 160)


while win.running:
    scale = math.sin(time.time() * 1.5) * .5 + 1.5
    img.resizeImage(160 * scale, 160 * scale)
    img.rotateImageTo(math.sin(time.time() * 3) * 20)

    img.draw()
    win.update()

    frameNum += 1
    if frameNum % 60 == 0:
        t = time.time()
        print(60 / (t - last60frametime))
        last60frametime = t
