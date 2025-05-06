from cmu_graphics import *

class Dropdown:
    def __init__(self, x, y, width, height, options, note,default="Select", align='left-top', textSize=16):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.options = options
        self.default = default
        self.selected = default
        self.isExpanded = False
        self.align = align
        self.textSize = textSize
        self.optionHeight = height
        self.label = note

    def draw(self):
        drawLabel(self.label, self.x, self.y - 20, size=self.textSize, align='left')
        drawRect(self.x, self.y, self.width, self.height, fill='white', border='black', align=self.align)
        drawLabel(self.selected, self.x + self.width / 2, self.y + self.height / 2, size=self.textSize, align='center')

        if self.isExpanded:
            for i, option in enumerate(self.options):
                optionY = self.y + self.height * (i + 1)
                drawRect(self.x, optionY, self.width, self.optionHeight, fill='gray', border='black', align=self.align, opacity = 20)
                drawLabel(option, self.x + self.width / 2, optionY + self.optionHeight / 2, size=self.textSize, align='center')

    def isClicked(self, mouseX, mouseY):
        return self.x <= mouseX <= self.x + self.width and self.y <= mouseY <= self.y + self.height

    def handleMousePress(self, mouseX, mouseY):
        if self.isClicked(mouseX, mouseY):
            self.isExpanded = not self.isExpanded  
            
        elif self.isExpanded:
            for option in self.options:
                optionY = self.y + self.height * (self.options.index(option) + 1)
                if optionY <= mouseY <= optionY + self.optionHeight:
                    self.selected = option  
                    self.isExpanded = False
                    return

    def updatePosition(self, x, y):
        self.x = x
        self.y = y

    def close(self):
        self.isExpanded = False

    

    def select(self, option):
        if option in self.options:
            self.selected = option
        else:
            self.selected = self.default  