################################################################
# tp_objects.py
#
# Ski Survival by Evan Nygard
# 15-112 term project
# 
# File containing all classes necessary for running the game
#################################################################

from cmu_112_graphics import *
from tkinter import *
from tp_collisiondata import *
import math, copy, random, time

######################################################################
#
# CLASS OBSTACLE (object)
# 
# - Defines the basic set of functions shared by all obstacles
# - List of obstacles in the game:
# -- Trees
# -- Rocks
# -- Rivers
# -- Fallen logs
# -- Slalom poles
# -- Snowdrifts (slow you down as you ski over them)
# -- Werewolves (are a special kind of obstacle; they are a NPC that detects 
#    and attempts to intercept the player)
#
######################################################################

class Obstacle(object):
    def __init__(self):
        pass
    
    def isJumpable(self):
        pass
    
    def name(self):
        pass

    def getLocation(self):
        pass

    def getLowestYPoint(self):
        # for the redrawAll() fn - if the player's center x and y is lower than
        # an obstacle's lowest point, the obstacle is drawn first (this is for
        # purposes of 3D-like graphics)
        pass

    def draw(self, app, canvas):
        pass

    def drawable(self, width, height):
        pass

    def move(self, dx, dy):
        pass

    def isNPC(self):
        return False # defaults to False
    
    def detectPlayer(self, player):
        # for NPC's only
        pass

    def doInterception(self, player):
        # for NPC's only
        pass

    def collisionResult(self):
        # defines what happens when a player hits an object
        # if the function returns 0, game over. If it returns any other number,
        # the player's speed is decreased by that amount
        # By default, the function returns 0 (a collision results in game over)
        return 0

    def getCollisionField(self):
        pass

    def collidedWithPlayer(self, player):
        selfObj = self.getCollisionField()
        return selfObj.collidedWithPlayer(player)

    def collidedWithObstacle(self, obstacle):
        selfObj = self.getCollisionField()
        dataObj = obstacle.getCollisionField()
        return selfObj.collidedWithObject(dataObj)


###########################################################################
#
# CLASS "TREE" (Obstacle)
# - A tree is a non-jumpable obstacle that is worth no points to avoid
#
# - Its collision field consists of its trunk (NOT including its leaves)
# - This means that tree leaves can overlap each other. This is fine and
#   intentional. If you're looking at a bird's eye view of a mountainside
#   forest, some tree leaves might overlap each other
#
###########################################################################

class Tree(Obstacle):

    def __init__(self, x, y, noPines=None, pineXOffset=None, yOffset=None):

        self.x = x
        self.y = y
        # all coordinates relating to the tree's components are relative to
        # self.x and self.y

        # trunk variables
        self.trunkLeftX = x-7
        self.trunkRightX = x+7
        if(yOffset == None):
            self.trunkTopY = y-random.randint(20, 30)
        else:
            self.trunkTopY = y-yOffset
        self.trunkBottomY = y+3

        if(noPines == None):
            noPines = random.randint(2, 3) # How many "^"s on top of the trunk?
        
        self.pines = [] # list of tuples containing coordinates for drawing
        pineBottomY = self.trunkTopY
        if(pineXOffset == None):
            pineXOffset = random.randint(18, 28)
        pineLeftX = x - pineXOffset
        pineRightX = x + pineXOffset
        pineHeight = 20

        for i in range(noPines):
            self.pines.append([pineLeftX, pineRightX, pineBottomY,
            pineBottomY-pineHeight])
            pineBottomY -= (pineHeight - 7)
    
    def isJumpable(self):
        return False # you can't jump over a tree

    def name(self):
        return "Tree"
    
    def getLocation(self):
        return (f"x0: {self.trunkLeftX}, y0:{self.trunkTopY}, x1: {self.trunkRightX}, y1: {self.trunkBottomY}")
    
    def getLowestYPoint(self):
        return self.trunkBottomY

    def draw(self, app, canvas):
        # draw the object on a canvas

        canvas.create_rectangle(self.trunkLeftX, self.trunkTopY,
        self.trunkRightX, self.trunkBottomY, fill='brown')

        for obj in self.pines: # draw each pine leaf set
            canvas.create_polygon(obj[0], obj[2], (obj[1]-obj[0]) / 2 + obj[0], obj[3],
            obj[1], obj[2], fill="green")
    
    def drawable(self, width, height):
        # checks if any part of the object is on the visible screen (and is
        # thus drawable)

        if(self.trunkBottomY < 0 or self.pines[-1][3] > height or
        self.pines[0][0] > width or self.pines[0][1] < 0):
            return False
        else: return True

    def move(self, dx, dy):
        # moves the tree by dx and dy

        self.x += dx
        self.y += dy

        self.trunkLeftX += dx
        self.trunkRightX += dx
        self.trunkBottomY += dy
        self.trunkTopY += dy

        for obj in self.pines:
            obj[0] += dx
            obj[1] += dx
            obj[2] += dy
            obj[3] += dy


    def getCollisionField(self):
        xWidth = self.trunkRightX - self.trunkLeftX
        yHeight = (self.trunkBottomY - self.trunkTopY) / 2
        useHeight = (self.trunkTopY + self.trunkBottomY) / 2
        dataDict = {
            "type": "rect",
            "locData": [self.trunkLeftX, useHeight, xWidth, yHeight],
            "jumpable": False,
            "name": "Tree"
        }
        return CollisionData(dataDict)


###########################################################################
# CLASS ROCK (Obstacle)
#
# - A rock is a non-jumpable obstacle that is worth no points to avoid
#
#
###########################################################################

class Rock(Obstacle):
    
    def __init__(self, x, y, r=None):
        self.cx = x
        self.cy = y
        if(r == None):
            self.r = random.randint(14, 21)
        else: self.r = r
    
    def name(self):
        return "Rock"
    
    def getLocation(self):
        return f"cx: {self.cx}, cy: {self.cy}, r: {self.r}"
    
    def getLowestYPoint(self):
        return self.cy+self.r
    
    def draw(self, app, canvas):
        canvas.create_arc(self.cx-self.r, self.cy-self.r, self.cx+self.r,
        self.cy+self.r, extent=180, style=CHORD, fill='gray')

    
    def isJumpable(self):
        return True
    
    def drawable(self, width, height):
        if(self.cx+self.r < 0 or self.cx-self.r > width or 
        self.cy+self.r < 0 or self.cy-self.r > height):
            return False
        else: return True

    def getCollisionField(self):
        # by = self.cy + self.r
        dataDict = {
            "type": "arc", # Todo change this
            # "locData": [self.cx-self.r, self.cy-self.r, self.cx+self.r, self.cy+self.r]
            "locData": [self.cx, self.cy, self.r],
            "jumpable": True,
            "name": "Rock"
        }
        return CollisionData(dataDict)

    def move(self, dx, dy):
        self.cx += dx
        self.cy += dy

###########################################################################
#
# CLASS "RIVER" (Obstacle)
#
# This is a jumpable obstacle. Horizontally spanning the entire screen, a river
# must be jumped over to be avoided. It is randomly generated using an algebraic
# x/y formula - k0*x^4 + k1*x^3 + k2*x^2 + k3*x, where k0, k1, k2, and k3 are
# randomly generated constants.
#
# The span of a river is randomly generated, but will always be small enough to
# be jumped over.
#
#
#
###########################################################################

class SimpleRiver(Obstacle):
    def __init__(self, width, y):
        self.width = width
        self.topY = y
        self.span = random.randint(20, 30)
        self.fillColor = 'blue'
    
    def name(self):
        return "SimpleRiver"
    
    def getLocation(self):
        return f"topY: {self.topY}, bottomY: {self.topY + self.span}"
    
    def getLowestYPoint(self):
        return self.topY+self.span

    def drawable(self, width, height):
        if(self.topY + self.span < 0 or self.topY > height):
            return False
        else: return True
    
    def draw(self, app, canvas):
        canvas.create_rectangle(0, self.topY, self.width, self.topY + self.span,
        fill=self.fillColor)
    
    def isJumpable(self):
        return True

    def getCollisionField(self):
        dataDict = {
            "type": "rect",
            "locData": [0, self.topY, self.width, self.span],
            "jumpable": True,
            "name": "SimpleRiver"
        }
        return CollisionData(dataDict)
    


    def move(self, x, y):
        # x is a dummy variable (only needed for proper inheritance)
        # Rivers span the entire screen
        self.topY += y


###########################################################################
#
# CLASS "SLALOMPOLE" (Obstacle)
#
# This class defines a slalom pole. Slalom poles are red or blue poles that
# appear on the map. If you pass by close enough to a slalom pole on the
# proper side, you'll get points.
#
###########################################################################

def createArrow(app, canvas, x0, y0, x1, y1, direction):
    # draw an arrow inside a white rectangle, pointing right or left
    # in practice, this arrow is always drawn above a SlalomPole, and specifies
    # the direction in which the user ought to skirt the pole in order to get
    # points

    canvas.create_rectangle(x0, y0, x1, y1, fill='white')
    width = x1 - x0
    height = y1 - y0
    xOffset = width / 8
    yOffsetMiddle = height / 2 # for the 'body' of the arrow: '---'
    yOffsetArrow = height / 4 # for the pointer of the arrow: '>' or '<'
    canvas.create_line(x0 + xOffset, y0 + yOffsetMiddle, x1 - xOffset,
    y0 + yOffsetMiddle) # draw '---'

    if(direction == "right"):
        canvas.create_line(x0 + width / 2, y0 + yOffsetArrow, x1 - xOffset,
        y0 + yOffsetMiddle) # draw '\'
        canvas.create_line(x0 + width / 2, y1 - yOffsetArrow, x1 - xOffset,
        y0 + yOffsetMiddle) # draw '/'

    else: # direction == "left"
        canvas.create_line(x0 + xOffset, y0 + yOffsetMiddle, x0 + width / 2,
        y0 + yOffsetArrow) # draw '/'
        canvas.create_line(x0 + xOffset, y0 + yOffsetMiddle, x0 + width / 2,
        y1 - yOffsetArrow) # draw '\'


class SlalomPole(Obstacle):
    def __init__(self, x, y):
        self.xLeft = x
        self.yTop = y
        self.width = 5
        self.height = 25
        self.jumpable = False
        # pick the pole's color. If it's blue, you get extra points for
        # passing to the right of the pole (the character's left). If it's red,
        # you get extra points for passing to the left (the character's right)
        self.color = "blue" if random.randint(0, 1) == 1 else "red"
        self.triggerDistance = 17 # how close the player needs to pass to the pole
        self.triggered = False # you can only trigger the pole once
    
    def name(self):
        return "SlalomPole"
    
    def getLocation(self):
        return f"x0: {self.xLeft}, y0: {self.yTop}, x1: {self.xLeft+self.width}, y1: {self.yTop+self.height}"
    
    def getLowestYPoint(self):
        return self.yTop+self.height
    
    def drawable(self, width, height):
        if(self.xLeft > width or (self.xLeft+self.width < 0) or 
        self.yTop > height or (self.yTop+self.height < 0)):
            return False
        else: return True
    
    def draw(self, app, canvas):
        canvas.create_rectangle(self.xLeft, self.yTop, self.xLeft+self.width,
        self.yTop+self.height, fill=self.color)

        arrowLeft = self.xLeft - 3
        arrowRight = self.xLeft + self.width + 3
        arrowBottom = self.yTop
        arrowTop = self.yTop - 10
        createArrow(app, canvas, arrowLeft, arrowTop, arrowRight, arrowBottom,
        "right" if self.color == 'blue' else "left")
    
    def getCollisionField(self):
        useHeight = self.height / 2
        collideTop = self.yTop + useHeight
        dataDict = {
            "type": "rect",
            "locData": [self.xLeft, collideTop, self.width, useHeight],
            "jumpable": False,
            "name": "SlalomPole"
        }

        return CollisionData(dataDict)
    
    def move(self, dx, dy):
        self.xLeft += dx
        self.yTop += dy
    
    def isJumpable(self):
        return self.jumpable
    
    def detectPlayer(self, player):
        # checks to see if the player passed self.triggerDistance away from the
        # bottom of the pole. If so, return True (and timerFired, which calls
        # this method, will add extra points)

        cx, cy = player.getXYCoords()
        xRight = self.xLeft + self.width
        yBottom = self.yTop + self.height
        if(self.color == "red"):
            if(math.sqrt((cy - yBottom)**2 + (cx - self.xLeft) ** 2) < self.triggerDistance
            and cx < self.xLeft # avoid triggering this if the player passes super close to the right side as well
            and not self.triggered):
                self.triggered = True
                return True
            else: return False
        else:
            if(math.sqrt((cy - yBottom)**2 + (cx - xRight) ** 2) < self.triggerDistance
            and cx > xRight
            and not self.triggered):
                self.triggered = True
                return True
            else:
                return False


###########################################################################
#
# CLASS "FALLENLOG" (Obstacle)
#
# This class defines an falling log obstacle, a jumpable obstacle that is worth
# no points to avoid.
#
###########################################################################

class FallenLog(Obstacle):
    def __init__(self, x, y):
        self.xLeft = x
        self.yTop = y
        self.xWidth = random.randint(20, 30)
        self.yHeight = random.randint(9, 15)
        self.jumpable = True
        self.fillColor = 'brown'
    
    def name(self):
        return "FallenLog"
    
    def getLocation(self):
        return f"x0: {self.xLeft}, y0: {self.yTop}, x1: {self.xLeft+self.xWidth}, y1: {self.yTop+self.yHeight}"
    
    def getLowestYPoint(self):
        return self.yTop+self.yHeight
    
    def move(self, x, y):
        self.xLeft += x
        self.yTop += y

    def isJumpable(self):
        return self.jumpable
    
    def drawable(self, width, height):
        if((self.xLeft > width) or (self.xLeft + self.xWidth < 0) or 
        (self.yTop > height) or (self.yTop + self.yHeight < 0)):
            return False
        else:
            return True
    
    def draw(self, app, canvas):
        xRight = self.xLeft + self.xWidth
        yBottom = self.yTop + self.yHeight
        canvas.create_rectangle(self.xLeft, self.yTop, xRight, yBottom,
        fill='brown')
        
    def getCollisionField(self):
        dataDict = {
            "type": "rect",
            "locData": [self.xLeft, self.yTop, self.xWidth, self.yHeight],
            "jumpable": True,
            "name": "FallenLog"
        }
        return CollisionData(dataDict)


###########################################################################
#
# CLASS "WEREWOLF" (Obstacle)
#
# - Werewolves are the only NPC's in the game. They stay put unless the player
#   comes too close to them; then they will chase down the player until
#   they catch the player or go off screen
# - To that end, each werewolf comes with a detection and tracking algorithm.
# -- the detectPlayer(player) method resets the werewolf to the chase state
#    if the player comes within 150-200 pixels of the werewolf (the exact
#    amount is randomly calculated)
# -- If the chase state is triggered, the werewolf will calculate the optimal
#    point of interception and will move to reach that precise point. Each time
#    the player changes direction, the werewolf recalculates that point and 
#    adjusts accordingly
# -- The werewolf moves almost (but not quite) as quickly as the player does.
#    Generally, the best way to avoid it is by putting horizontal distance
#    between yourself and the werewolf. It'll still calculate the interception
#    point, but you'll be able to outdistance it.
# -- of course, this can be easier said than done later in the game when there
#    are tons of obstacles on each side
###########################################################################

class Werewolf(Obstacle):

    def __init__(self, cx, cy, imageDict):
        self.cx = cx
        self.cy = cy
        self.r = 10
        self.detectionRadius = random.randint(150, 200)

        self.imageDict = imageDict
        self.currentImage = self.imageDict["rest"]

        self.inChaseState = False
        self.speed = 10 # 6 px moved per call of timerFired when chasing

        # optimal point of intercept "interceptionX, interceptionY"
        self.ix = None
        self.iy = None
    
    def name(self):
        return "Werewolf"
    
    def getLocation(self):
        return f"cx: {self.cx}, cy: {self.cy}, r: {self.r}"
    
    def getLowestYPoint(self):
        width, height = self.currentImage.size
        return self.cy + (height / 2)
    
    def move(self, dx, dy):
        self.cx += dx
        self.cy += dy
    
    def isJumpable(self):
        return False
    
    def getCollisionField(self):
        width, height = self.currentImage.size

        yTop = self.cy - height / 3 # we need to account for the whitespace
        xLeft = self.cx - width / 3 # around the image
        useWidth = width * 2/3 # otherwise a collision will happen
        useHeight = height * 2/3 # when it appears that it shouldn't

        dataDict = {
            "type": "rect",
            "locData": [xLeft, yTop, useWidth, useHeight],
            "jumpable": False,
            "name": "Werewolf"
        }
        return CollisionData(dataDict)

    def drawable(self, width, height):
        if(self.cx+self.r < 0 or self.cx-self.r > width or 
        self.cy+self.r < 0 or self.cy-self.r > height):
            return False
        else: return True
    
    def draw(self, app, canvas):
        # image code in this fn (and in player draw fns) from here:
        # https://www.kosbie.net/cmu/spring-20/15-112/notes/notes-animations-part2.html
        canvas.create_image(self.cx, self.cy, image=ImageTk.PhotoImage(self.currentImage))
    
    def isNPC(self):
        return True
    
    def detectPlayer(self, player):
        # tests to see whether the player is within the object's detection
        # radius
        px, py = player.getXYCoords()
        distance = math.sqrt((px-self.cx)**2+(py-self.cy)**2)
        if(distance <= self.detectionRadius):
            self.currentImage = self.imageDict["chase"]
            self.inChaseState = True
        
    def doInterception(self, player):
        # having detected the player, move the werewolf toward the interception
        # point
        # Mathematical calculations were used from here:
        # https://www.codeproject.com/Articles/990452/Interception-of-Two-Moving-Objects-in-D-Space

        #### DEBUG NOTES ####
        # currently, this fn works properly and successfully moves the werewolf
        # towards an interception point. However, this interception point is not
        # optimized. It tends to undershoot where the player is going to be.
        #
         
        if(not self.inChaseState): return
        px, py = player.getXYCoords() # current player coordinates
        dpx, dpy = player.getMoveState() # player's direction (vector variable - VsubR)

        
        playerSpeed = math.sqrt(dpx**2 + dpy**2)
        # (wpVX, wpVY) is a vector FROM the player TO the werewolf - D
        wpVX = self.cx - px # "werewolf player vector X"
        wpVY = self.cy - py # "werewolf player vector Y"
        playerDistance = math.sqrt(wpVX**2 + wpVY**2) # dist btwn werewolf and player
        DTimesVR = wpVX * dpx + wpVX * dpy + wpVY * dpx + wpVY * dpy # D * VsubR
        cosTheta = DTimesVR / abs(playerSpeed * playerDistance)

        # with all of these variables, we can use the quadratic formula to solve
        # for the time it'll take to intercept, which we can subsequently use
        # to calculate the exact point of interception. More details at the
        # source which was cited above.

        a = self.speed**2 - playerSpeed**2
        b = 2 * playerDistance * playerSpeed * cosTheta
        c = -playerDistance**2

        passIntoSqrt = b**2 - (4 * a * c)
        if(passIntoSqrt < 0): # there is no possible interception point
            if(self.inChaseState):
                self.moveTowardPlayer(px, py) # if already chasing, keep pursuing
            return

        t1 = (-b + math.sqrt(passIntoSqrt)) / (2 * a)
        t2 = (-b - math.sqrt(passIntoSqrt)) / (2 * a)

        # find the actual time to intercept. If one is negative, use the
        # positive one. If both are positive, use the smaller one. If both are
        # negative, interception is impossible; use the "dumb" intercept fn.
        interceptTime = -1

        if(t1 < 0 and t2 < 0):
            if(self.inChaseState):
                self.moveTowardPlayer(px, py)
            return
        elif(t1 < 0 and t2 >= 0): interceptTime = t2
        elif(t2 < 0 and t1 >= 0): interceptTime = t1
        else: 
            interceptTime = min(t1, t2) # original

        # now, get the interception point
        self.ix = px + dpx * interceptTime
        self.iy = py + dpy * interceptTime


        # using similar triangles, calculate the x and y moves that move in
        # the direction of the interception point.
        # See diagram __ in __ file

        xInterceptionDiff = self.ix - self.cx
        yInterceptionDiff = self.iy - self.cy
        interceptionDistance = math.sqrt(xInterceptionDiff**2 +
                                yInterceptionDiff**2)

        moveX = xInterceptionDiff * (5 / interceptionDistance)
        moveY = yInterceptionDiff * (5 / interceptionDistance)

        # finally, move!
        self.move(moveX, moveY)
    
    def moveTowardPlayer(self, px, py):
        # this is a "dumb" interception function
        # it's used when the werewolf is in the middle of a chase state
        # but doInterception calculates that an interception is impossible.
        # In this case, the werewolf will keep moving towards where the player
        # happens to be at that time.
        # The function is called mainly because, say the player is speeding
        # away from the pursuing werewolf but runs into a group of obstacles.
        # To correct for that, the player turns back in a direction that the
        # werewolf can viably intercept the player. Having moved in the player's
        # general direction, the werewolf is in an ideal position to intercept
        # the player using the "smart" doInterception() function.

        # We use similar triangles to calculate the x and y movements of the
        # werewolf towards the player. See diagram __ in __ file

        xInterceptionDiff = px - self.cx
        yInterceptionDiff = py - self.cy

        interceptionDistance = math.sqrt(xInterceptionDiff**2 +
                                yInterceptionDiff**2)

        moveX = xInterceptionDiff * (5 / interceptionDistance)
        moveY = yInterceptionDiff * (5 / interceptionDistance)

        self.move(math.ceil(moveX), math.ceil(moveY))
        
class Snowdrift(Obstacle):
    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy
        self.r = random.randint(12, 25)
        self.jumpable = True
        self.playerSlowSpeed = 5 # player slows down by 5 px/timerFired call
        self.fillColor = "#e9eaf5"
    
    def name(self):
        return "Snowdrift"
    
    def getLocation(self):
        return f"cx: {self.cx}, cy: {self.cy}, r: {self.r}"
    
    def getLowestYPoint(self):
        return 0 # should always be drawn before the player is drawn

    def isJumpable(self):
        return self.jumpable
    
    def drawable(self, width, height):
        if((self.cx-self.r > width) or (self.cx+self.r < 0) or 
        (self.cy-self.r > height) or self.cy+self.r<0):
            return False
        else: return True
    
    def draw(self, app, canvas):
        canvas.create_oval(self.cx-self.r, self.cy-self.r, self.cx+self.r, 
        self.cy+self.r, fill=self.fillColor, width=0)
    
    def getCollisionField(self):
        diameter = 2 * self.r
        dataDict = {
            "type": "circle", # Todo change this
            "locData": [self.cx, self.cy, self.r], # and this
            "jumpable": False,
            "name": "Snowdrift"
        }
        return CollisionData(dataDict)
    
    def move(self, dx, dy):
        self.cx += dx
        self.cy += dy
    
    def collisionResult(self):
        return self.playerSlowSpeed









class Player(object):

    def __init__(self, x, y, imageDict):
        self.cx = x
        self.cy = y
        # self.r = r
        
        # an imageList should be a dict of images corresponding to the motion
        # state of the player
        # The dict should look something like this:
        # {
        #  "jump": jumpingImage
        #  "move": [images corresponding to moveStates (defined below)]
        # }
        self.imageDict = imageDict
        self.currentImage = self.imageDict["move"][3] # image that should be drawn

        self.speed = self.originalSpeed = 7
        self.moveStateIndex = 3

        self.moveStates = [ 
        (-self.speed*math.sin(math.pi/3), self.speed*math.cos(math.pi/3)), # left @ 60 deg
        (-self.speed*math.sin(math.pi/4), self.speed*math.cos(math.pi/4)), # left @ 45 deg
        (-self.speed*math.sin(math.pi/6), self.speed*math.cos(math.pi/6)), # left @ 30 deg
        (0, self.speed),                                          # straight down
        (self.speed*math.sin(math.pi/6), self.speed*math.cos(math.pi/6)),  # right @ 30 deg
        (self.speed*math.sin(math.pi/4), self.speed*math.cos(math.pi/4)),  # right @ 45 deg
        (self.speed*math.sin(math.pi/3), self.speed*math.cos(math.pi/3)) ]

        self.inJumpState = False
        self.jumpStateStartTime = -1
        self.jumpTimeInterval = 1 # 1 second of air time

        self.crashed = False
    
    def name(self):
        return "Player"

    def getLocation(self):
        return self.cx, self.cy
    
    def getXYCoords(self):
        return (self.cx, self.cy)
    
    def setCrashed(self):
        self.crashed = True
    
    def getCollisionField(self):
        width, height = self.currentImage.size
        yTop = self.cy # we only take the bottom half of the player into account
                         # when calculating a collision. This makes it look more
                         # 3D in the actual game.
        xLeft = self.cx - width / 3
        useWidth = width * 2/3
        useHeight = height / 3

        dataDict = {
            "type": "rect",
            "locData": [xLeft, yTop, useWidth, useHeight],
            "jumpable": False, # doesn't really matter, this is the Player
            "name": "Player"
        }
        return CollisionData(dataDict)
    
    def getMoveState(self):
        return self.moveStates[self.moveStateIndex]

    def getMoveStateIndex(self):
        return self.moveStateIndex

    def setSpeed(self, newSpeed):
        self.speed = newSpeed
        self.moveStates = [ # we need to recalculate this to update the speed
        (-self.speed*math.sin(math.pi/3), self.speed*math.cos(math.pi/3)),
        (-self.speed*math.sin(math.pi/4), self.speed*math.cos(math.pi/4)),
        (-self.speed*math.sin(math.pi/6), self.speed*math.cos(math.pi/6)),
        (0, self.speed),
        (self.speed*math.sin(math.pi/6), self.speed*math.cos(math.pi/6)),
        (self.speed*math.sin(math.pi/4), self.speed*math.cos(math.pi/4)),
        (self.speed*math.sin(math.pi/3), self.speed*math.cos(math.pi/3)) ]
    
    def getSpeed(self):
        return self.speed
    
    def getOriginalSpeed(self):
        return self.originalSpeed
    
    def jump(self):
        if(self.inJumpState): return # can't jump while in midair
        self.inJumpState = True
        self.jumpStateStartTime = time.time()
    
    def isInJumpState(self):
        return self.inJumpState
    
    def setMoveStateIndex(self, change):
        # changes the moveStateIndex by change unless the resultant change is
        # out of bounds

        if(self.moveStateIndex + change >= 0 and 
        self.moveStateIndex + change < len(self.moveStates)):
            self.moveStateIndex += change
        self.currentImage = self.imageDict["move"][self.moveStateIndex]
    
    def draw(self, app, canvas):
        if(self.crashed):
            self.currentImage = self.imageDict["crashed"]
        elif(self.inJumpState): # handle change of image while jumping
            # also, since draw() is guaranteed to be called continuously,
            # we can handle checking valid air time in here 
            currTime = time.time()
            if(currTime - self.jumpStateStartTime >= self.jumpTimeInterval):
                # the player has now landed
                self.inJumpState = False
                self.jumpStateStartTime = -1
                self.currentImage = self.imageDict["move"][self.moveStateIndex]
            else:
                self.currentImage = self.imageDict["jump"][0]

        canvas.create_image(self.cx, self.cy, image=ImageTk.PhotoImage(self.currentImage))
    
    def drawable(self, app, canvas):
        return True # the player doesn't move

