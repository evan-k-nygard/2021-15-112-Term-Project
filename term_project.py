
################################################################
# term_project.py
#
# Ski Survival by Evan Nygard
# 15-112 term project
# 
# Main file for running
#################################################################

from cmu_112_graphics import *
from tkinter import *
import math, copy, time, random
from tp_objects import *
from button import *

def appStarted(app):
    # set up screen/game mode controls
    app.onHomescreen = True
    app.gameMode = "" # can be "standard", "werewolfChase", "slalom"

    # homescreen vars
    app.buttons = [
        Button(app.width / 2, app.height * 3/7, "Standard Mode"),
        Button(app.width / 2, app.height * 4/7, "Werewolf Chase"),
        Button(app.width / 2, app.height * 5/7, "Slalom"),
        Button(app.width / 2, app.height * 6/7, "Instructions")
    ]
    app.gameModes = [
        "standard",
        "werewolfChase",
        "slalom",
        "instructions"
    ]
    app.highScoreFiles = [ # indices are coordinated to indices of app.gameModes
        "highScoreStandard.txt",
        "highScoreWerewolf.txt",
        "highScoreSlalom.txt"
    ]

    # instruction screen button var
    # this var is only not None if we're on the instruction screen
    app.instructionBackButton = None

    # general game variables
    app.startTime = time.time()
    app.objects = [] # a list containing all obstacles visible onscreen
    app.paused = False
    app.gameOver = False
    app.gameOverTime = None # time when game is over
    app.originalTimerDelay = 50 
    app.timerDelay = app.originalTimerDelay

    # score vars
    app.score = 0
    app.highScore = -1 # will be updated to actual high score when we start a game

    # image handling functions were obtained here:
    # https://www.kosbie.net/cmu/spring-20/15-112/notes/notes-animations-part2.html
    app.playerImages = {
        "jump": [
            app.scaleImage(app.loadImage("jumpDown.png"), 1/10)
        ],
        "move": [
            app.scaleImage(app.loadImage("skierLeft60.png"), 1/10),
            app.scaleImage(app.loadImage("skierLeft45.png"), 1/9),
            app.scaleImage(app.loadImage("skierLeft30.png"), 1/10),
            app.scaleImage(app.loadImage("skierDown.png"), 1/10),
            app.scaleImage(app.loadImage("skierRight30.png"), 1/11),
            app.scaleImage(app.loadImage("skierRight45.png"), 1/10),
            app.scaleImage(app.loadImage("skierRight60.png"), 1/9)
        ],
        "crashed": app.scaleImage(app.loadImage("skierCrashed.png"), 1/10)
    
    }

    # beef up the graphics
    # background color
    # score not in plaintext
    # trees - fractals?
    # homescreen
    # dynamic bang??
    # skier crash image in any case
    # instructions page (on homescreen)
    # leaderboard

    app.werewolfImages = {
        "rest": app.scaleImage(app.loadImage("werewolfRest.png"), 1/10),
        "chase": app.scaleImage(app.loadImage("werewolfChase.png"), 1/10)
    }

    app.player = Player(app.width / 2, app.height / 4, app.playerImages)

    # variables specifically for Slalom mode
    app.slalomTimeMessage = "Time left:"
    app.slalomTimeLimit = 60 # seconds
    app.timeLeft = app.slalomTimeLimit - 0

def keyPressed(app, event):
    if(event.key == 'r'): # restart game
        tmpMode = app.gameMode
        appStarted(app)
        app.onHomescreen = False # reinitialize the game mode and high score
        app.gameMode = tmpMode
        resetHighScore(app)
    elif(event.key == 'h'): # back to homescreen
        appStarted(app)
    elif(app.gameOver): return
    elif(event.key == 'p'): app.paused = not app.paused
    elif(app.paused): return
    elif(event.key == "Left"): # change the way the player moves
        if(app.gameMode == "werewolfChase" # can't move too far in one direction
        and app.player.getMoveStateIndex() == 1): return # in werewolf chase

        app.player.setMoveStateIndex(-1)
    elif(event.key == "Right"):
        if(app.gameMode == "werewolfChase" and 
        app.player.getMoveStateIndex() == 5): return
        app.player.setMoveStateIndex(1)
    elif(event.key == "Space"): # jump
        app.player.jump()
    # these next key events are for demonstration and debugging purposes and are
    # not intended to be called by a typical user. Therefore, they aren't listed
    # in the instructions screen, only in the readme file. These only work in
    # standard mode, due to the obstacle setups and rules of the other modes
    elif(app.gameMode == "standard" and event.key == 't'): # add tree
        app.objects.append(Tree(random.randint(1, app.width-1), app.height-1))
    elif(app.gameMode == "standard" and event.key == 'k'): # add rock
        app.objects.append(Rock(random.randint(1, app.width-1), app.height-1))
    elif(app.gameMode == "standard" and event.key == 'l'): # add fallen log
        app.objects.append(FallenLog(random.randint(1, app.width-1), app.height-1))
    elif(app.gameMode == "standard" and event.key == 'v'): # add river
        app.objects.append(SimpleRiver(app.width, app.height - 1))
    elif(app.gameMode == "standard" and event.key == 's'): # slalom pole
        app.objects.append(SlalomPole(random.randint(1, app.width-1), app.height-1))
    elif(app.gameMode == "standard" and event.key == 'd'): # snowdrift
        app.objects.append(Snowdrift(random.randint(1, app.width-1), app.height-1))
    elif(app.gameMode == "standard" and event.key == 'w'): # werewolf
        app.objects.append(Werewolf(random.randint(1, app.width-1), app.height-1, app.werewolfImages))



def mousePressed(app, event):
    # this function mainly handles button presses. It only does anything if
    # we're on the home screen or the instruction screen.
    if(app.gameMode == "instructions"):
        # check to see if we clicked the back button
        x0, y0, x1, y1 = app.instructionBackButton.getXYCoords(app)
        if(event.x > x0 and event.x < x1 and event.y > y0 and event.y < y1):
            appStarted(app) # we hit the back button, now we go back to homescreen
    elif(app.onHomescreen): # loop through our four buttons, see if we clicked any
        for i in range(len(app.buttons)):
            x0, y0, x1, y1 = app.buttons[i].getXYCoords(app)
            if(event.x > x0 and event.x < x1 and event.y > y0 and event.y < y1):
                app.onHomescreen = False
                app.gameMode = app.gameModes[i]
                if(app.gameMode != "instructions"):
                    # do specific actions for starting up a game
                    app.instructionBackButton = None # remove the button
                    # we don't use a score or a start time for the instructions page
                    resetHighScore(app, i) # update app.highScore to right number
                    app.startTime = time.time()
                else: # we clicked into the instruction screen and need to create
                    # our back button
                    app.instructionBackButton = Button(app.width / 9,
                    app.height / 20, "<- Back")
    else: return # we don't do mouse presses for any kind of game mode
    

def updateScore(app, score=0):
    if(score == 0): app.score += 1
    else: app.score += score

def resetHighScore(app, i=None):
    # get the current high score for our given mode and set app.highScore
    # equal to that score
    # The file handling code in this fn and in updateHighScore() was adapted
    # from here: https://docs.python.org/3/tutorial/inputoutput.html

    if(app.gameMode == "instructions" or app.onHomescreen):
        # no high score here
        return
    
    if(i == None): # get the right index if we don't have it already
        i = app.gameModes.index(app.gameMode)
    with open(app.highScoreFiles[i]) as scoreFile:
        # find the high score for our given mode
        app.highScore = int(scoreFile.read())


def updateHighScore(app):
    # set a new high score if we pass the previous one for a given game mode

    if(not app.gameOver): return # should only work once we hit game over
    if(app.score > app.highScore and app.highScore != -1):
        # score must be higher (first condition) and we can't write a new high
        # score over and over (second condition)
        index = app.gameModes.index(app.gameMode)
        with open(app.highScoreFiles[index], 'w') as scoreFile:
            scoreFile.write(str(app.score))

def drawScore(app, canvas):
    # draws the score in the upper right hand corner
    if(app.score <= app.highScore):
        txt = f"Score: {app.score}"
    else:
        txt = f"High score: {app.score}"
    canvas.create_text(app.width * 4/5, 15, text=txt)

def drawSlalomTimeRemaining(app, canvas):
    # draw the time remaining (slalom mode only) in upper left corner if and
    # only if we're in slalom mode
    if(app.gameMode != app.gameModes[2]): return
    txt = f"{app.slalomTimeMessage} {app.timeLeft}"
    canvas.create_text(app.width*1/10, 15, text=txt)

def updateTimeLeft(app):
    # updates the amount of time we have left. If this time is 0, we hit game
    # over. Only works for Slalom mode
    if(app.gameMode != app.gameModes[2]): return
    if(app.gameOver or app.paused):
        return
    runTime = int(time.time() - app.startTime)
    app.timeLeft = app.slalomTimeLimit - runTime
    if(app.timeLeft <= 0):
        app.gameOver = True
        app.gameOverTime = time.time()

def generate(app):
    # Terrain generator
    # Generates obstacles randomly. The longer the game is played, the more
    # likely it is that obstacles will be generated.

    if(app.onHomescreen): return
    
    runTime = min(time.time() - app.startTime, 200)
    runTimeOffset = 50 # used in generating obstacles randomly
    app.timerDelay = app.originalTimerDelay - int(runTime / 5)

    newObstacleList = []

    if(app.gameMode == app.gameModes[0]):
        newObstacleList = [
            Tree(random.randint(1, app.width-1), app.height-1),
            Tree(random.randint(1, app.width-1), app.height-1),
            Tree(random.randint(1, app.width-1), app.height-1),
            Tree(random.randint(1, app.width-1), app.height-1),
            Tree(random.randint(1, app.width-1), app.height-1),
            Tree(random.randint(1, app.width-1), app.height-1),
            Rock(random.randint(1, app.width-1), app.height-1),
            Rock(random.randint(1, app.width-1), app.height-1),
            Rock(random.randint(1, app.width-1), app.height-1),
            FallenLog(random.randint(1, app.width-1), app.height-1),
            FallenLog(random.randint(1, app.width-1), app.height-1),
            FallenLog(random.randint(1, app.width-1), app.height-1),
            Werewolf(random.randint(1, app.width-1), app.height-1, app.werewolfImages),
            SlalomPole(random.randint(1, app.width-1), app.height-1),
            SlalomPole(random.randint(1, app.width-1), app.height-1),
            SimpleRiver(app.width, app.height - 1),
            Snowdrift(random.randint(1, app.width-1), app.height-1),
            Snowdrift(random.randint(1, app.width-1), app.height-1)
        ]
    elif(app.gameMode == app.gameModes[1]): # werewolf chase
        runTimeOffset = 20 # we don't want too many werewolves to be spawned from
                          # the get-go
        newObstacleList = [
            Tree(random.randint(1, app.width-1), app.height-1),
            Tree(random.randint(1, app.width-1), app.height-1),
            Werewolf(random.randint(1, app.width-1), app.height-1, app.werewolfImages),
            Werewolf(random.randint(1, app.width-1), app.height-1, app.werewolfImages),
            Werewolf(random.randint(1, app.width-1), app.height-1, app.werewolfImages),
            Werewolf(random.randint(1, app.width-1), app.height-1, app.werewolfImages),
            Werewolf(random.randint(1, app.width-1), app.height-1, app.werewolfImages),
            Werewolf(random.randint(1, app.width-1), app.height-1, app.werewolfImages),
            Werewolf(random.randint(1, app.width-1), app.height-1, app.werewolfImages)
        ]
    elif(app.gameMode == app.gameModes[2]): # slalom
        newObstacleList = [
            SlalomPole(random.randint(1, app.width-1), app.height-1),
            SlalomPole(random.randint(1, app.width-1), app.height-1),
            SlalomPole(random.randint(1, app.width-1), app.height-1),
            SlalomPole(random.randint(1, app.width-1), app.height-1),
            SlalomPole(random.randint(1, app.width-1), app.height-1),
            Tree(random.randint(1, app.width-1), app.height-1)
        ]

    if(app.gameMode == app.gameModes[0] or app.gameMode == app.gameModes[1]):
        # standard or werewolfChase. If it's slalom, score is only updated as
        # you pass a pole
        updateScore(app)
    
    # Create a new obstacle according to a random number generator (or if there
    # are no objects currently onscreen). The likelihood of a new obstacle being
    # generated is a function of how long the game has been played (runTime)
    # plus a little bit extra for difficulty (runTimeOffset) 

    if(random.randint(0, 500) < runTime + runTimeOffset or len(app.objects) == 0):
        newObstacle = newObstacleList[random.randrange(0, len(newObstacleList))]
        obstacleIsValid = True
        for obj in app.objects:
            if(obj.collidedWithObstacle(newObstacle)):
                obstacleIsValid = False
                break
        if(obstacleIsValid): app.objects.append(newObstacle)

def timerFired(app):
    # a lot of the meat of the app is done in here. The main role of this fn is
    # to constantly update the location of all obstacles relative to the player's
    # movement direction and 
    if(app.gameOver):
        updateHighScore(app)
        return
    if(app.paused or app.onHomescreen or app.gameMode == app.gameModes[3]):
        return
    # if we're in slalom mode, update the amount of time left
    updateTimeLeft(app)
    # if we don't have any obstacles on the board, create a new one
    generate(app)
    i = 0
    if(len(app.objects) == 0): return
    inCollision = False
    while(i < len(app.objects)):
        # move the objects; if any object turns out to be undrawable, remove it
        moveDirections = app.player.getMoveState()
        # the objects move in the opposite direction that the player is
        # percieved to be moving
        app.objects[i].move(-moveDirections[0], -moveDirections[1])
        
        if(not app.objects[i].drawable(app.width, app.height)):
            app.objects.pop(i)
            i -= 1
        # check to see if any objects have now collided with the player
        if(i < 0): return # ensures that we don't loop over app.objects while it's empty

        if(app.objects[i].collidedWithPlayer(app.player)):
            inCollision = True
            action = app.objects[i].collisionResult()
            if(action == 0): # 0 means game over
                app.player.setCrashed()
                app.gameOver = True
                app.gameOverTime = time.time()
            else: # reduce speed by value of action
                app.player.setSpeed(app.player.getOriginalSpeed() - action)
        
        # check if the current object is a slalom pole, and if so, see if the 
        # player passed close enough to earn points
        if(isinstance(app.objects[i], SlalomPole)):
            if(app.objects[i].detectPlayer(app.player)):
                if(app.gameMode != app.gameModes[2]): # we're in standard mode
                    updateScore(app, 70)
                else: # only way to get points is by passing a pole in Slalom mode
                    updateScore(app, 10)
        
        # check if the current object is a NPC, and if so, run the detection
        # algorithm
        if(app.objects[i].isNPC()):
            app.objects[i].detectPlayer(app.player)
            app.objects[i].doInterception(app.player)
        i += 1
    if(not inCollision): # we aren't being slowed down by anything, so
                        # make sure the player's speed is back to normal
                        # (example: we just came out of a snowdrift)
        app.player.setSpeed(app.player.getOriginalSpeed())

#### functions for redrawAll ####

def drawHomescreen(app, canvas):
    # draws the home screen, containing the title, all the buttons, and a few
    # stationary obstacles for extra visual aesthetics

    title = "Ski Survival"
    canvas.create_text(app.width / 2, app.height / 4, text=title,
    font="Helvetica 36 bold")

    for button in app.buttons:
        button.draw(app, canvas)
    
    # draw a player and a few obstacles
    canvas.create_image(app.width * 3/10, app.height / 8,
    image=ImageTk.PhotoImage(app.playerImages["move"][3]))

    tree1 = Tree(app.width / 5, app.height / 2, 2, 20, 20)
    tree1.draw(app, canvas)
    tree2 = Tree(app.width * 6/7, app.height * 2/3, 3, 24, 26)
    tree2.draw(app, canvas)
    rock = Rock(app.width * 3/11, app.height * 10/11, 15)
    rock.draw(app, canvas)

def drawGameplay(app, canvas):
    # general drawing function used for each gameplay mode. Draws all objects
    # on the board. Object locations are updated in timerFired, so this fn just
    # needs to loop through the list of obstacles.
    
    nonJumpableObjectIndices = []

    for i in range(len(app.objects)): # draw all jumpable objects first.
        # that way, if the player jumps over them, the player won't appear
        # to pass under them
        if((app.objects[i].isJumpable() and app.player.isInJumpState())
        or app.player.getXYCoords()[1] > app.objects[i].getLowestYPoint()):
            app.objects[i].draw(app, canvas)
        else:
            # obstacle will be drawn after the player is drawn; store the index
            # for later reference
            nonJumpableObjectIndices.append(i)
    
    app.player.draw(app, canvas)

    for index in nonJumpableObjectIndices:
        # draw all the jumpable obstacles now
        app.objects[index].draw(app, canvas)
    
    
    drawScore(app, canvas)
    drawSlalomTimeRemaining(app, canvas) # this fn will draw only in slalom mode

def drawGameOver(app, canvas):
    # draws the game over message one second after game over
    if(app.gameOverTime != None and app.gameOver
    and int(time.time() - app.gameOverTime) >= 1):
        canvas.create_text(app.width / 2, app.height / 2,
        text="Game Over!", font="Helvetica 60 bold", fill='#ff2626')
        canvas.create_text(app.width / 2, app.height * 3/5,
        text="Press 'r' to restart; press 'h' to return to the homepage",
        font="Helvetica 18 bold")

def drawInstructionsScreen(app, canvas):
    if(app.instructionBackButton != None): # should never be None
        app.instructionBackButton.draw(app, canvas)
    
    canvas.create_text(app.width / 2, app.height / 8,
    text="Ski Survival Instructions", font="Helvetica 20 bold")

    standardModeInstructions = """STANDARD MODE:
    Survive as long as possible! Avoid all obstacles while evading the Werewolf
    and skirting around Slalom Poles in order to gain as many points as possible!""".strip()

    canvas.create_text(5, app.height * 3/11, text=standardModeInstructions,
    font="Helvetica 14", anchor='w')

    werewolfModeInstructions = """WEREWOLF CHASE:
    On this hill, there are a few scattered trees and endless packs of hungry 
    werewolves. How long will you survive them?""".strip()

    canvas.create_text(5, app.height * 5/11, text=werewolfModeInstructions,
    font="Helvetica 14", anchor='w')

    slalomModeInstructions = """SLALOM:
    Prove your ability as a skier by skirting around slalom poles to earn points!
    Each pole is worth 10 points, and you have one minute to score as high as you
    can!""".strip()

    canvas.create_text(5, app.height * 7/11, text=slalomModeInstructions,
    font="Helvetica 14", anchor='w')

    controls = """CONTROLS:
    Left/right arrows = move left or right
    Space = jump
    'r' = restart the game
    'p' = pause the game
    'h' = go back to home screen""".strip()

    canvas.create_text(5, app.height * 9/11, text=controls,
    font="Helvetica 14", anchor='w')


def redrawAll(app, canvas):
    if(app.onHomescreen): drawHomescreen(app, canvas)
    elif(app.gameMode == app.gameModes[3]):
        drawInstructionsScreen(app, canvas)
    else:
        drawGameplay(app, canvas)
        drawGameOver(app, canvas)
    

def main():
    runApp(width=550, height=500)

if(__name__ == '__main__'):
    main()