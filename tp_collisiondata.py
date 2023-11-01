################################################################
# tp_collisiondata.py
#
# Ski Survival by Evan Nygard
# 15-112 term project
# 
# File containing the CollisionData class and its subclasses.
# CollisionData is used by the obstacle classes and objects to
# determine whether one class has collided with another.
#################################################################

import math

def _getSimpleCollision(xLeft1, xRight1, yTop1, yBottom1, xLeft2, xRight2,
                       yTop2, yBottom2):
    # returns whether two rectangular objects have collided
    # the algorithm for this function was copied from my solution
    # to hw1, problem 7: rectanglesOverlap().
    #
    # This function should NOT be called by the user of this file.

    if(
    # top left of 2 intersects bottom right of 1?
    (yBottom1 >= yTop2 >= yTop1 and xLeft1 <= xLeft2 <= xRight1)
    # bottom left of 2 intersects top right of 1?
    or (yTop1 <= yBottom2 <= yBottom1 and xLeft1 <= xLeft2 <= xRight1)
    # bottom right of 2 intersects top left of 1?
    or (yTop1 <= yBottom2 <= yBottom1 and xLeft1 <= xRight2 <= xRight1)
    # top right of 2 intersects bottom left of 1?
    or (yBottom1 >= yTop2 >= yTop1 and xLeft1 <= xRight2 <= xRight1)
    # 2 overlaps entire width of 1?
    or (xLeft2 <= xLeft1 and xRight2 >= xRight1
        and (yBottom1 >= yBottom2 >= yTop1 or yBottom1 >= yTop2 >= yTop1))
    # 2 overlaps entire height of 1?
    or (yTop2 <= yTop1 and yBottom2 >= yBottom1 
        and (xLeft1 <= xLeft2 <= xRight1 or xLeft1 <= xRight2 <= xRight1))
    # 1 is inside 2?
    or (xLeft1 >= xLeft2 and xRight1 <= xRight2
        and yBottom1 <= yBottom2 and yTop1 >= yTop2)
    ):
        return True
    else:
        return False

"""# top right of rect intersects bottom left of arc?
    (math.sqrt((by - yTop)**2 + (cx - xRight)**2) < r)):
        print("hit elif 1")
        return True
    # bottom right of rect intersects top left of arc?
    elif (math.sqrt((by - yBottom)**2 + (cx - xRight)**2) < r):
        print("hit elif 2")
        return True
    # bottom left of rect intersects top right of arc?
    elif (math.sqrt((yBottom - by)**2 + (xLeft - cx)**2) < r):
        print("hit elif 3")
        return True
    # top left of rect intersects bottom right of arc?
    elif (math.sqrt((yTop - by)**2 + (xLeft-cx)**2) < r):
        print("hit elif 4")
        return True"""

def _getRectArcCollision(xLeft, xRight, yTop, yBottom, cx, by, r):
    if(by - r > yBottom): return False # handle the arc's flat bottom
    elif((abs(cx - xLeft) < r or abs(xRight - cx) < r) and ((yTop < by and yTop > by-r) or abs(by - yBottom) < r)):
        return True
    # rect covers arc?
    elif (xLeft < cx-r and xRight > cx+r and yTop < by-r and yBottom > by):
        return True
    # entire right side of rect intersects entire left side of arc?
    elif (cx - r < xRight and by < yBottom and by-r > yTop):
        return True
    # entire left side of rect intersects entire right side of arc?
    elif (cx + r > xLeft and by < yBottom and by-r > yTop):
        return True
    # entire bottom of rect intersects entire top of arc?
    elif (by - r > yBottom and xLeft < cx-r and xRight > cx+r):
        return True
    # entire top of rect intersects entire bottom of arc?
    elif (by > yTop and xLeft < cx-r and xRight > cx+r):
        return True
    else: return False

def _getRectCircleCollision(xLeft, xRight, yTop, yBottom, cx, cy, r):
    # checks to see whether a collision has occurred btwn a circular and a 
    # rectangular object

    distToXLeft = abs(xLeft - cx)
    distToXRight = abs(cx - xRight)
    distToYTop = abs(cy - yTop)
    distToYBottom = abs(yBottom - cy)

    # did one corner of the rectangle intersect w/ the circle?
    if((distToXLeft < r or distToXRight < r) and (distToYTop < r or distToYBottom < r)):
        return True
    # is the entire width of the rectangle intersecting w/ the circle?
    elif((distToYTop < r or distToYBottom < r) and (xLeft < cx - r) and (xRight > cx + r)):
        return True
    # is the entire height of the rectangle intersecting w/ the circle?
    elif((distToXLeft < r or distToXRight < r) and (yTop < cy - r) and (yBottom > cy + r)):
        return True
    # is the rectangle covering the circle?
    elif((xLeft < cx - r) and (xRight > cx + r) and (yTop < cy - r) and (yBottom > cy + r)):
        return True
    # is the circle covering the rectangle?
    elif((xLeft >= cx - r) and (xRight <= cx + r) and (yTop >= cy - r) and (yBottom <= cy + r)):
        return True
    # otherwise, no collision
    else:
        return False


def _getCircularCollision(cx1, cy1, r1, cx2, cy2, r2):
    # works for both circles and arcs
    distance = math.sqrt((cy2 - cy1)**2 + (cx2 - cx1)**2)
    if(distance < r1 + r2): return True
    else: return False

"""def _getArcCircleCollision(cx1, by1, r1, cx2, cy2, r2):
    if(cy2 - r2 > by1): return False # handle the arc's flat bottom
    elif(math.sqrt((cy2-by1)**2 + (cx2-cx1)**2) <= r1 + r2):
        return True ### TODO check this condition for when the circle is off to
        # the side and slightly lower than the arc bottom - might be a math buge
    else:
        return False

def _getArcArcCollision(cx1, by1, r1, cx2, by2, r2):
    if(by1 - r1 > by2 or by2 - r2 > by1): return False"""

    
def _evalCoefficients(coeffs, x):
    exp = 0
    y = 0
    for i in range(len(coeffs) - 1, -1, -1):
        y += coeffs[i] * x**exp
        exp += 1
    return y

def _getPartialAlgebraicCollision(coeffs, left1, width1, height1, buffer1, left2,
                                  top2, width2, height2, buffer2, rects=1000):
    # takes in location data for two CollisionData objects - one defined by an
    # algebraic equation, one that is not - and calculates the 
    for i in range(rects):
        x0 = left1 + i * (width1 / rects)
        x1 = left1 + (i + 1) * (width1 / rects)
        y0 = _evalCoefficients(coeffs, x0)
        y1 = y0 + height1
        
        xLeft, xRight, yTop, yBottom = _getRectangularPoints(left2, top2, width2,
        height2, buffer2)
        if(_getSimpleCollision(x0 - buffer1, x1 + buffer1, y0 - buffer1,
        y1 + buffer1, xLeft, xRight, yTop, yBottom)):
            return True
    return False

def _getRectangularPoints(left, top, width, height):
    xLeft = left
    xRight = left + width
    yTop = top
    yBottom = top + height
    return (xLeft, xRight, yTop, yBottom)




###########################################################################
# CLASS "COLLISIONDATA" (object)
#
# Returns data regarding an object's location for usage in calculating whether
# a collision has occured
# 
# Different objects have different means for determining whether a collision has
# occurred. For example, trees and fallen logs are basically rectangles, so
# one can compare the player's current range of points to the range of points
# on the rectangle using basic less-than, greater-than, equal-to, etc.
# comparisons. Rivers, on the other hand, use a y = kx**n equation in order to
# define their boundaries. Thus, one cannot use the same procedure to compare
# the location of the player to the location of a tree to the location of a
# river, etc.
#
# The CollisionData class abstracts this information regarding one's location
# on the board and 
###########################################################################

class CollisionData(object):
    def __init__(self, dataDict):
        """
        dataDict is a dict - one can expect these inputs:
        {
            "type": "arc", "circle", or "rect"
            "locData": if an arc, [cx, by, r]; if a rect, [xLeft, yTop, width, height]; if a circle, [cx, cy, r]
            "jumpable": True or False
            "name": -name-
        }
        """
        self.dataDict = dataDict

    def getData(self):
        return self.dataDict

    def collidedWithObject(self, dataObj):
        if(self.dataDict["type"] == "rect" and dataObj.dataDict["type"] == "rect"):

            xLeft1, xRight1, yTop1, yBottom1 = _getRectangularPoints(
            self.dataDict["locData"][0], self.dataDict["locData"][1],
            self.dataDict["locData"][2], self.dataDict["locData"][3])

            xLeft2, xRight2, yTop2, yBottom2 = _getRectangularPoints(
            dataObj.dataDict["locData"][0], dataObj.dataDict["locData"][1],
            dataObj.dataDict["locData"][2], dataObj.dataDict["locData"][3])

            return _getSimpleCollision(xLeft1, xRight1, yTop1, yBottom1,
            xLeft2, xRight2, yTop2, yBottom2)
        elif(self.dataDict["type"] == "rect" and dataObj.dataDict["type"] == "arc"):

            xLeft1, xRight1, yTop1, yBottom1 = _getRectangularPoints(
            self.dataDict["locData"][0], self.dataDict["locData"][1],
            self.dataDict["locData"][2], self.dataDict["locData"][3])

            cx2 = dataObj.dataDict["locData"][0]
            by2 = dataObj.dataDict["locData"][1]
            r2 = dataObj.dataDict["locData"][2]

            return _getRectArcCollision(xLeft1, xRight1, yTop1, yBottom1, cx2,
            by2, r2)
        elif(self.dataDict["type"] == "arc" and dataObj.dataDict["type"] == "rect"):
            
            cx1 = self.dataDict["locData"][0]
            by1 = self.dataDict["locData"][1]
            r1 = self.dataDict["locData"][2]

            xLeft2, xRight2, yTop2, yBottom2 = _getRectangularPoints(
            dataObj.dataDict["locData"][0], dataObj.dataDict["locData"][1],
            dataObj.dataDict["locData"][2], dataObj.dataDict["locData"][3])

            return _getRectArcCollision(xLeft2, xRight2, yTop2, yBottom2, cx1,
            by1, r1)
        
        elif(self.dataDict["type"] == "arc" and dataObj.dataDict["type"] == "arc"):
            cx1 = self.dataDict["locData"][0]
            by1 = self.dataDict["locData"][1]
            r1 = self.dataDict["locData"][2]

            cx2 = dataObj.dataDict["locData"][0]
            by2 = dataObj.dataDict["locData"][1]
            r2 = dataObj.dataDict["locData"][2]

            return _getCircularCollision(cx1, by1, r1, cx2, by2, r2)
        elif(self.dataDict["type"] == "circle" and dataObj.dataDict["type"] == "rect"):
            cx1 = self.dataDict["locData"][0]
            by1 = self.dataDict["locData"][1]
            r1 = self.dataDict["locData"][2]

            xLeft2, xRight2, yTop2, yBottom2 = _getRectangularPoints(
            dataObj.dataDict["locData"][0], dataObj.dataDict["locData"][1],
            dataObj.dataDict["locData"][2], dataObj.dataDict["locData"][3])

            return _getRectCircleCollision(xLeft2, xRight2, yTop2, yBottom2, cx1,
            by1, r1)

        elif(self.dataDict["type"] == "rect" and dataObj.dataDict["type"] == "circle"):
            xLeft1, xRight1, yTop1, yBottom1 = _getRectangularPoints(
            self.dataDict["locData"][0], self.dataDict["locData"][1],
            self.dataDict["locData"][2], self.dataDict["locData"][3])

            cx2 = dataObj.dataDict["locData"][0]
            cy2 = dataObj.dataDict["locData"][1]
            r2 = dataObj.dataDict["locData"][2]

            return _getRectCircleCollision(xLeft1, xRight1, yTop1, yBottom1,
            cx2, cy2, r2)
        elif(self.dataDict["type"] == "arc" and dataObj.dataDict["type"] == "circle"):
            cx1 = self.dataDict["locData"][0]
            by1 = self.dataDict["locData"][1]
            r1 = self.dataDict["locData"][2]

            cx2 = dataObj.dataDict["locData"][0]
            cy2 = dataObj.dataDict["locData"][1]
            r2 = dataObj.dataDict["locData"][2]

            return _getCircularCollision(cx1, by1, r1, cx2, cy2, r2)
        elif(self.dataDict["type"] == "circle" and dataObj.dataDict["type"] == "arc"):
            cx1 = self.dataDict["locData"][0]
            cy1 = self.dataDict["locData"][1]
            r1 = self.dataDict["locData"][2]

            cx2 = dataObj.dataDict["locData"][0]
            by2 = dataObj.dataDict["locData"][1]
            r2 = dataObj.dataDict["locData"][2]

            return _getCircularCollision(cx1, cy1, r1, cx2, by2, r2)
        else: # self.dataDict["type"] == "circle" and dataObj.dataDict["type"] == "circle"
            cx1 = self.dataDict["locData"][0]
            cy1 = self.dataDict["locData"][1]
            r1 = self.dataDict["locData"][2]

            cx2 = dataObj.dataDict["locData"][0]
            cy2 = dataObj.dataDict["locData"][1]
            r2 = dataObj.dataDict["locData"][2]

            return _getCircularCollision(cx1, cy1, r1, cx2, cy2, r2)
            

    def collidedWithPlayer(self, player):
        playerField = player.getCollisionField()

        cx, cy = player.getLocation()
        selfBottomY = None
        if(self.dataDict["type"] == "rect"):
            selfBottomY = self.dataDict["locData"][1] + self.dataDict["locData"][3]
        elif(self.dataDict["type"] == "arc"):
            selfBottomY = self.dataDict["locData"][1]
        else: # self.dataDict["type"] == "circle"
            selfBottomY = self.dataDict["locData"][1] + self.dataDict["locData"][2]
        if(cy > selfBottomY):
            return False # for proper look in 3D - we've passed the obstacle
        elif(player.isInJumpState() and self.dataDict["jumpable"]):
            return False
        else: # test as though we're testing a normal object, except don't
              # account for the buffer
            return self.collidedWithObject(playerField)
        


