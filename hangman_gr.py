#!/usr/bin/env python

##
#    Author: Richard Opsal
#
#   Purpose: CS2321 Demonstration program.
#            Graphical version of the Hangman word game.
#
#      Name: hangman_gr.py
#
#   Started: 2010/03/09
#   Revised: 2010/03/11
##

from graphics import *
from hangman  import *
from button   import Button

class Keyboard:
    """Representation of a Qwerty keyboard with all 26 characters."""

    def __init__(self, win, pnts):
        self.keys = []
        self.letters = list('QWERTYUIOPASDFGHJKLZXCVBNM')
        rows = [10, 9, 7]

        pt1, pt2 = pnts
        width = abs(pt1.getX()-pt2.getX()) / 10
        height= abs(pt1.getY()-pt2.getY()) / 3

        i = 0        
        start = Point(pt1.getX() + width/2, pt1.getY() + 5*height/2)
        for cnt in rows:
            pnt = start
            for k in range(cnt):
                self.keys.append(Button(win, pnt, width, height, self.letters[i], 'ivory'))
                i += 1
                pnt = Point(pnt.getX()+width, pnt.getY())
            start = Point(start.getX()+width/2, pnt.getY()-height)

    def clicked(self, pnt):
        hit = None
        for key in self.keys:
            if key.clicked(pnt):
                hit = key.getLabel()
                break
        return hit

    def reactivate(self):
        for key in self.keys:
            key.activate()

    def deactivate(self, char):
        try:
            index = self.letters.index(char)
            self.keys[index].deactivate()
        except:
            pass


class Actions:
    """User selections for the Exit, Start Over, and New Game actions.
       Also takes care of Wins and Losses counter."""

    (BUTTON_EXIT, BUTTON_START_OVER, BUTTON_NEW_GAME) = range(3)

    def __init__(self, win, pnts):
        self.height = 40
        self.margin = 20
        self.win = win
        self.buttons = []
        self.__makeExit(pnts[0], pnts[1])
        self.__makeStartOver(pnts[0], pnts[1])
        self.__makeNewGame(pnts[0], pnts[1])

    def clicked(self, pnt):
        ident = None
        for k, button in enumerate(self.buttons):
            if button.clicked(pnt):
                ident = k
                break
        return ident

    def __makeExit(self, pt1, pt2):
        center = Point((pt1.getX() + pt2.getX())/2, pt2.getY() - self.height/2 )
        width  = abs(pt2.getX() - pt1.getX())
        self.buttons.append(Button(self.win, center, width, self.height, 'Exit', 'red'))
        self.buttons[Actions.BUTTON_EXIT].activate()

    def __makeStartOver(self, pt1, pt2):
        center = Point((pt1.getX() + pt2.getX())/2, pt1.getY() + 3*self.height/2 + self.margin )
        width  = abs(pt2.getX() - pt1.getX())
        self.buttons.append(Button(self.win, center, width, self.height, 'Start Over', 'blue'))
        self.buttons[Actions.BUTTON_START_OVER].activate()

    def __makeNewGame(self, pt1, pt2):
        center = Point((pt1.getX() + pt2.getX())/2, pt1.getY() + self.height/2 )
        width  = abs(pt2.getX() - pt1.getX())
        self.buttons.append(Button(self.win, center, width, self.height, 'New Game', 'blue'))
        self.buttons[Actions.BUTTON_NEW_GAME].activate()


class Gallows:
    """The gallows where the body is hung."""

    def __init__(self, win, pnts):
        self.win = win
        self.__makeNoose  (pnts[0], pnts[1])
        self.__makeGallows(pnts[0], pnts[1])

    def nooseEnd(self):
        return self.nooseend

    def bodyHeight(self):
        return self.bodyheight

    def __makeNoose(self, pt1, pt2):
        height = abs(pt2.getY() - pt1.getY())
        center = Point((pt1.getX()+pt2.getX())/2, pt2.getY())
        self.nooseend   = Point(center.getX(), center.getY() - height/5)
        self.bodyheight = 7*height/10
        rope = Line(center, self.nooseend)
        rope.setWidth(6)
        rope.setFill('firebrick4')
        rope.draw(self.win)

    def __makeGallows(self, pt1, pt2):
        beams = []
        width = 16
        brace = abs(pt2.getY() - pt1.getY()) / 3
        beams.append(Rectangle(pt1, Point(pt2.getX(), pt1.getY()+width)))
        beams.append(Rectangle(pt1, Point(pt1.getX()+width/2, pt2.getY())))
        beams.append(Rectangle(Point(pt1.getX(), pt2.getY()-width), pt2))
        beams.append(Rectangle(Point(pt2.getX()-width/2, pt1.getY()), pt2))
        line = (Line(Point(pt1.getX()+width/4, pt2.getY()-brace),
                     Point(pt1.getX()+brace  , pt2.getY()-width/4)))
        line.setWidth(width/2)
        beams.append(line)
        line = (Line(Point(pt2.getX()-width/4, pt2.getY()-brace),
                     Point(pt2.getX()-brace  , pt2.getY()-width/4)))
        line.setWidth(width/2)
        beams.append(line)        
        for beam in beams:
            beam.setOutline('burlywood4')
            beam.setFill('burlywood4')
            beam.draw(self.win)


class Body:
    """The body parts to be drawn during the hanging."""

    def __init__(self, win, pntnoose, bodyheight):
        self.body = []
        self.win = win
        self.cparts = 6
        self.cdrawn = 0

        xmid = pntnoose.getX()
        radius = bodyheight/8
        center = Point(xmid, pntnoose.getY()-radius)

        self.body.append(Circle(center, radius))
        self.body.append(Line(Point(xmid, pntnoose.getY()-2*radius),
                              Point(xmid, pntnoose.getY()-5*radius)))

        pntarm = Point(xmid, pntnoose.getY()-3*radius)
        self.body.append(Line(pntarm, Point(xmid-2*radius, pntarm.getY()+radius)))
        self.body.append(Line(pntarm, Point(xmid+2*radius, pntarm.getY()+radius)))

        pntleg = Point(xmid, pntnoose.getY()-5*radius)
        self.body.append(Line(pntleg, Point(xmid-2*radius, pntleg.getY()-2*radius)))
        self.body.append(Line(pntleg, Point(xmid+2*radius, pntleg.getY()-2*radius)))

        for k, part in enumerate(self.body):
            part.setWidth(5)
            part.setOutline('purple4')
            if (0<k):   # Don't fill in the head.
                part.setFill('purple4')
        self.hangAll()

    def hangAll(self):
        while (self.cdrawn < self.cparts):
            self.body[self.cdrawn].draw(self.win)
            self.cdrawn += 1            

    def hangPart(self):
        if (self.cdrawn < self.cparts):
            self.body[self.cdrawn].draw(self.win)
            self.cdrawn += 1

    def undraw(self):
        for part in self.body:
            part.undraw()
        self.cdrawn = 0

    def status(self):
        return self.cdrawn, self.cparts
    

class Status:
    """Display of the various status text fields."""

    (FIELD_WORD, FIELD_STATUS, FIELD_LOSSES, FIELD_WINS) = range(4)

    def __init__(self, win, pointsStatus, pointsLossesWins):
        self.win = win
        self.fields = []
        self.cwins   = 0
        self.closses = 0

        ci = 0
        ptsize = 18
        style  = 'bold'
        colors = ['navy', 'red', 'red', 'blue']

        for pnts in [pointsStatus, pointsLossesWins]:
            pt1, pt2 = pnts
            xmid = (pt1.getX() + pt2.getX()) /2
            height = abs(pt2.getY() - pt1.getY())
            yoff = pt1.getY() + height/4
            for _ in range(2):
                text = Text(Point(xmid, yoff), '')
                text.setSize(ptsize)
                text.setTextColor(colors[ci])
                text.setFace('arial')
                text.draw(self.win)
                self.fields.append(text)
                yoff += height/2
                ci += 1

            ptsize = 14
            style  = 'normal'

        # Tweak to make the Hangman word a bit larger.
        self.fields[Status.FIELD_WORD].setSize(20)

    def addLoss(self):
        self.closses += 1
        text = 'Losses: ' + str(self.closses)
        self.fields[Status.FIELD_LOSSES].setText(text)

    def addWin(self):
        self.cwins += 1
        text = 'Wins: ' + str(self.cwins)
        self.fields[Status.FIELD_WINS].setText(text)

    def setTextWord(self, text):
        self.fields[Status.FIELD_WORD].setText(text)

    def setTextStatus(self, text):
        self.fields[Status.FIELD_STATUS].setText(text)


class Hangman:
    """The game of Hangman is represented by this class."""

    def __init__(self, size):
        self.size = size
        self.margin = 10
        self.__makeWindow()
        self.keyboard = Keyboard(self.win, self.__positionKeyboard())
        self.actions  =  Actions(self.win, self.__positionActions())
        self.gallows  =  Gallows(self.win, self.__positionGallows())
        self.body     =     Body(self.win, self.gallows.nooseEnd(), self.gallows.bodyHeight())
        self.status   =   Status(self.win, self.__positionStatus(), self.__positionWinsLosses())
        self.status.setTextStatus('Welcome to the Hangman Word Guessing Game')
        self.status.setTextWord("Press the 'New Game' Button to Start")
        self.wordlist = wordList()

    def play(self):
        fexit = False
        letterlist = hanglist = []
        while not fexit:
            pnt = self.win.getMouse()
            action = self.actions.clicked(pnt)
            key = self.keyboard.clicked(pnt)
            if (None != action):
                if (action == Actions.BUTTON_EXIT):
                    fexit = True
                else:
                    if (hanglist != letterlist):
                        self.status.addLoss()

                    if (action == Actions.BUTTON_NEW_GAME) or (None == letterlist):
                        letterlist = wordSplit(randWord(self.wordlist))

                    hanglist = wordSplit('_' * len(letterlist))
                    self.status.setTextStatus('')
                    self.status.setTextWord(joinLetterList(hanglist))
                    self.body.undraw()
                    self.keyboard.reactivate()

            elif (None != key) and (0 < len(letterlist)):
                self.keyboard.deactivate(key)
                fmatch = letterMatch_gr(key, letterlist, hanglist)
                if (False == fmatch):
                    self.body.hangPart()
                    cdrawn, cparts = self.body.status()
                    if (cdrawn == cparts):
                        self.status.addLoss()
                        self.status.setTextWord(joinLetterList(letterlist))
                        self.status.setTextStatus('Better luck on the next word!')
                        letterlist = hanglist = []

                elif (letterlist == hanglist):
                    self.status.addWin()
                    self.status.setTextWord(joinLetterList(letterlist))
                    self.status.setTextStatus('Congratulations on your win!')
                    letterlist = hanglist = []

                elif (True == fmatch):
                    self.status.setTextWord(joinLetterList(hanglist))

    def close(self):
        if (None != self.win):
            self.win.close()

    def __makeWindow(self):
        win = GraphWin( 'CS2321 Hangman', self.size, self.size )
        win.setCoords(0,0,self.size,self.size)
        win.setBackground("dark sea green")
        self.win = win

    def __positionKeyboard(self):
        size = self.size
        margin = self.margin
        pt1 = Point(margin, margin)
        pt2 = Point(size - margin, size/4 - margin)
        return pt1, pt2

    def __positionActions(self):
        size = self.size
        margin = self.margin
        pt1 = Point(8*size/10 + margin, 6*size/10 + margin)
        pt2 = Point(size-margin, size-margin)
        return pt1, pt2

    def __positionGallows(self):
        size = self.size
        margin = self.margin
        pt1 = Point(margin, 4*size/10 + margin)
        pt2 = Point(8*size/10 - margin, size-margin)
        return pt1, pt2

    def __positionStatus(self):
        size = self.size
        margin = self.margin
        pt1 = Point(margin, size/4 + margin)
        pt2 = Point(size - margin, 4*size/10 - margin)
        return pt1, pt2

    def __positionWinsLosses(self):
        size = self.size
        margin = self.margin
        pt1 = Point(8*size/10 + margin, 4*size/10 + margin)
        pt2 = Point(size - margin, 6*size/10 - margin)
        return pt1, pt2


# Create the game object and then invoke the play method.
if __name__=='__main__':

    hangman = Hangman(800)
    hangman.play()
    hangman.close()