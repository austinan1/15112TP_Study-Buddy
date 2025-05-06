from cmu_graphics import *
from utilities.button import Button
from utilities.dropdown import Dropdown
from utilities.textbox import Textbox
from calendar import Calendar
from eventEditor.eventManager import EventManager
import math

class GoalSetter:
    def __init__(self, app):
        self.app = app
        self.buttons = {
            'cancel': Button(10, 10, 140, 30, 'Cancel', 16, align='left-top'),
            'save': Button(app.width - 150, 10, 140, 30, 'Save', 16, align='left-top'),
        }
        self.textboxes = {
            'goalName': Textbox(150, 100, 300, 40, 'Enter goal name'),
            'goalDescription': Textbox(150, 160, 300, 40, 'Enter goal description'),
            'goalDeadline': Textbox(150, 220, 300, 40, 'Enter deadline (e.g., YYYY-MM-DD)'),
        }
        self.dropdowns = {
            'goalPriority': Dropdown(500, 100, 200, 40, ['High', 'Medium', 'Low'], 'Priority', 'Select Priority'),
            'goalCategory': Dropdown(500, 200, 200, 40, ['Work', 'Health', 'Personal'], 'Category', 'Select Category')
        }
        self.errorMessage = ''
    
    def draw(self):
        for button in self.buttons.values():
            button.draw()
        for textbox in self.textboxes.values():
            textbox.draw()
        for dropdown in self.dropdowns.values():
            if dropdown.isExpanded:
                dropdown.draw()
                break
            else:
                dropdown.draw()
        if self.errorMessage:
            drawLabel(self.errorMessage, self.app.width / 2, self.app.height - 50, size=16, fill='red', align='center')
        
        
       
    
    def handleMousePress(self, mouseX, mouseY):
        if self.buttons['cancel'].isClicked(mouseX, mouseY):
            self.resetToDefault()
            self.app.view = 'goalViewer'
        elif self.buttons['save'].isClicked(mouseX, mouseY):
            self.saveGoal()
        
        for textbox in self.textboxes.values():
            textbox.handleClick(mouseX, mouseY)
        for dropdown in self.dropdowns.values():
            dropdown.handleMousePress(mouseX, mouseY)

    def handleKeyPress(self, key):
        for textbox in self.textboxes.values():
            textbox.handleKeyPress(key)

    # this function is called when the user clicks on the calendar icon and selects a date
    def resetToDefault(self):
        for textbox in self.textboxes.values():
            textbox.reset()
        for dropdown in self.dropdowns.values():
            dropdown.selected = dropdown.default
            dropdown.close()
        self.errorMessage = ''
        #self.subtasks = []

    
    def saveGoal(self):
        goalName = self.textboxes['goalName'].text.strip()
        goalDescription = self.textboxes['goalDescription'].text.strip()
        goalDeadline = self.textboxes['goalDeadline'].text.strip()
        goalPriority = self.dropdowns['goalPriority'].selected
        goalCategory = self.dropdowns['goalCategory'].selected
        
        if not (goalName and goalDeadline and goalPriority != 'Select Priority' and goalCategory != 'Select Category'):
            self.errorMessage = 'Please fill out all fields correctly.'
            return
        
        self.app.goals.append({
            'name': goalName,
            'description': goalDescription,
            'deadline': goalDeadline,
            'priority': goalPriority,
            'category': goalCategory,
            'progress': 0,
            'subtasks': [] ,
            'estimatedTime': 0
        })
        self.resetToDefault()
        self.errorMessage = ''
        self.app.view = 'menu'

    
