################################################################
# button.py
#
# Ski Survival by Evan Nygard
# 15-112 term project
# 
# File containing the Button class, used as a representation of a button
# on the home screen
#
#################################################################

from cmu_112_graphics import *

class Button(object):
    def __init__(self, x, y, text):
        self.cx = x
        self.cy = y
        self.xOffset = 55
        self.yOffset = 15
        self.text = text
    
    def getXYCoords(self, app):
        xLeft = self.cx-self.xOffset
        yTop = self.cy-self.yOffset
        xRight = self.cx+self.xOffset
        yBottom = self.cy+self.yOffset

        return (xLeft, yTop, xRight, yBottom)
    
    def draw(self, app, canvas):
        xLeft, yTop, xRight, yBottom = self.getXYCoords(app)

        canvas.create_rectangle(xLeft, yTop, xRight, yBottom, fill='#afe1f0', width=3)
        canvas.create_text(self.cx, self.cy, text=self.text)