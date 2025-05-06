from cmu_graphics import *

class Button:
    def __init__(self,x,y,width,height,label,howBig,align = 'center'):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.label = label
        self.align = align
        self.size = howBig

    def draw(self):
        drawRect(self.x,self.y,self.width,self.height, fill = None, border = 'black', align = self.align)
        drawLabel(self.label, self.x + self.width/2, self.y + self.height/2, size = self.size)

    
    def isClicked(self,mouseX,mouseY):
        return (self.x <= mouseX <= self.x + self.width) and  (self.y <= mouseY <= self.y + self.height)
    
    def updatePosition(self,x,y):
        self.x = x
        self.y = y
    