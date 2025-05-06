from cmu_graphics import *

class Textbox:
    def __init__(self, x, y, width, height, placeholder='', align='left-top', textSize=16, maxLength=30):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.placeholder = placeholder
        self.text = ''
        self.isFocused = False
        self.align = align
        self.textSize = textSize
        self.maxLength = maxLength

    def draw(self):
        drawRect(self.x, self.y, self.width, self.height, fill='white', border='black', align='left-top')
        if self.text:
            drawLabel(self.text, self.x + 5, self.y + self.height / 2, size=self.textSize, align='left')
        else:
            drawLabel(self.placeholder, self.x + 5, self.y + self.height / 2, size=self.textSize, fill='gray', align='left')

        if self.isFocused:
            drawRect(self.x, self.y, self.width, self.height, border='blue', borderWidth=2, align='left-top', fill = None)
    def setText(self, text):
        self.text = text


    def isClicked(self, mouseX, mouseY):
        return self.x <= mouseX <= self.x + self.width and self.y <= mouseY <= self.y + self.height

    def handleClick(self, mouseX, mouseY):
        self.isFocused = self.isClicked(mouseX, mouseY)

    def handleKeyPress(self, key):
        if self.isFocused:
            if key == 'backspace':
                self.text = self.text[:-1]
            elif len(self.text) < self.maxLength:
                if key == 'space':
                    self.text += ' '  
                elif len(key) == 1:  
                    self.text += key

    def getInput(self):
        return self.text

    def reset(self):
        self.text = ''
        
