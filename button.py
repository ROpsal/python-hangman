# button.py

from graphics import *

class Button:
    """ A button is a labled rectangle in a window.
    It is activated or deactivated with the activate() and deactivate() methods.
    The clicked(p) method returns true if the button is active and p is inside it."""

    def __init__(self, win, center, width, height, label, color):
            """Creates a rectangular button, eg:
            qb = Button(myWin, centerPoint, width, height, 'Quit') """
            w, h = width/2.0, height/2.0
            self.x,self.y = center.getX(), center.getY()
            self.xmax, self.xmin = self.x+w, self.x-w
            self.ymax, self.ymin = self.y+h, self.y-h
            p1 = Point(self.xmin, self.ymin)
            p2 = Point(self.xmax, self.ymax)
            self.rect = Rectangle(p1, p2)
            self.rect.setFill(color)
            self.rect.draw(win)
            self.label = Text(center, label)
            self.label.draw(win)
            self.deactivate()

    def clicked(self, p):
        "Returns true if button active and p is inside"
        return self.active and \
               self.xmin <= p.getX() <= self.xmax and \
               self.ymin <= p.getY() <= self.ymax

    def getLabel(self):
        "Returns the label string of this button"
        return self.label.getText()

    def setLabel(self, word):
        self.label.setText(word)
        
    def activate(self):
        "Sets this button to 'active' "
        self.label.setFill('black')
        self.rect.setWidth(4)
        self.active = True

    def deactivate(self):
        "Sets this button to 'inactive' "
        self.label.setFill('darkgrey')
        self.rect.setWidth(1)
        self.active = False

    def resetFill(self, colour):
        self.rect.setFill(colour)

    def erase(self, colour):
        self.rect.setWidth(1)
        self.rect.setOutline(colour)
        self.label.setFill(colour)
        self.rect.setFill(colour)

    def undrawB(self):
        self.rect.undraw()
        self.label.undraw()
        
    def isActive(self):
        return self.active

    def resetLabel(self, colour):
        self.label.setFill(colour)

    def findCenter(self):
        return self.x, self.y