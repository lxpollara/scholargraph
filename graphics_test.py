from graphics import *


win = Window(500,500)
circle = Circle((250,400), 60)

circle.draw(win)
circle.fill = Color('pink')

while True:
    x,y = getMouseNow()
    circle.moveTo(x,y)
