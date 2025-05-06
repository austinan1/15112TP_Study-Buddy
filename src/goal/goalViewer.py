from cmu_graphics import *
from eventEditor.studyPlanner import StudySessionScheduler
from utilities.button import Button
from utilities.textbox import Textbox
from eventEditor.eventManager import EventManager
import math
from utilities.dropdown import Dropdown

class GoalViewer:
    def __init__(self, app):
        self.app = app
        self.currentGoalIndex = 0

        self.addButton = Button(app.width / 2 - 150, app.height - 180, 300, 40, '+ add goal', 16, align='left-top')
        self.removeButton = Button(app.width / 2 - 150, app.height - 230, 300, 40, 'Remove Goal', 16, align='left-top')

        self.textbox = Textbox(app.width / 2 - 60, app.height - 60, 120, 30, 'Hours')  # Initialize self.textbox
        self.subtaskNameBox = Textbox(20, 320, 120, 30, 'Subtask Name')
        self.subtaskTimeBox = Textbox(20, 360, 120, 30, 'Hours')
        self.colorDropdown = Dropdown(150, 320, 120, 30, ['Red', 'Blue', 'Green', 'Yellow', 'Purple', 'Orange', 'Pink', 'Brown', 'Black', 'White'], '', 'Color:')

        self.buttons = {
            'prev': Button(10, 10, 140, 30, 'Previous', 16, align='left-top'),
            'next': Button(app.width - 150, 10, 140, 30, 'Next', 16, align='left-top'),
            'addSubtask': Button(20,400, 120, 30, 'Add Subtask', 14, align='left-top'),
            'removeSubtask': Button(300,310, 140, 30, 'Remove Subtask', 14, align='left-top'),
            'markDone': Button(300,220, 140, 30, 'Mark Done', 14, align='left-top'),
            'markUnDone': Button(300,265, 140, 30, 'Mark Undone', 14, align='left-top')
        }

        self.errorMessage = ''
        self.remainingTime = 0

    # Update the remaining time for the current goal
    def updateRemainingTime(self):
        currentGoal = self.app.goals[self.currentGoalIndex]
        subtaskList = currentGoal.get('subtasks')
        if subtaskList:
            self.remainingTime = sum(subtask['time'] for subtask in subtaskList if not subtask.get('done', False))
        else:
            self.remainingTime = currentGoal['estimatedTime']
    

    
    def draw(self):
        drawLabel(self.errorMessage, self.app.width / 2, self.app.height - 100, size=16, fill='red', align='center')
        drawLabel(f'Goal {self.currentGoalIndex+1}/{len(self.app.goals)}', app.width/2, 20, size=16)
        for button in self.buttons.values():
            button.draw()
        self.subtaskNameBox.draw()
        self.subtaskTimeBox.draw()
        self.addButton.draw()
        self.colorDropdown.draw()
        self.removeButton.draw()
        if not self.app.goals:
            drawLabel("No goals available.", self.app.width / 2, self.app.height / 2, size=20, align='left-top')
            return
        if self.currentGoalIndex >= len(self.app.goals):
            self.currentGoalIndex = len(self.app.goals)-1
        currentGoal = self.app.goals[self.currentGoalIndex]
        drawLabel(f"Goal Name: {currentGoal['name']}", 30, 70, size=20, align='left-top')
        drawLabel(f"Description: {currentGoal['description']}", 30,100, size=16, align='left-top')
        drawLabel(f"Deadline: {currentGoal['deadline']}", 30, 130, size=16, align='left-top')
        drawLabel(f"Total Time: {currentGoal['estimatedTime']} hrs", 30, 160, size=16, align='left-top')
        drawLabel(f"Time Left: {self.remainingTime} hrs", 30, 190, size=16, align='left-top')
        drawLabel(f"Progress: {currentGoal['progress']//1}%", 30, 220, size=16, align='left-top')
        drawLabel(f"Priority: {currentGoal['priority']}", 30, 250, size=16, align='left-top')
        drawLabel(f"Category: {currentGoal['category']}", 30, 280, size=16, align='left-top')

        # Progress Bar
        barX = 300
        barY = 160
        barWidth = 400
        barHeight = 20
        progressWidth = (currentGoal['progress'] / 100) * barWidth

        drawRect(barX, barY, barWidth, barHeight, fill='lightgrey', border='black', borderWidth=2)
        if progressWidth > 1:
            drawRect(barX, barY, progressWidth, barHeight, fill='green')

        # percent label (irrelevant)
        drawLabel(f"{int(currentGoal['progress'])}%", barX + barWidth / 2, barY + barHeight / 2, size=14, align='center', fill='white')

        # draw subtasks if they exist 
        drawLabel("Subtasks:", 500,220, size=18, align='left-top')
        if currentGoal.get('subtasks'):
            y = 250
            for i, subtask in enumerate(currentGoal['subtasks']):
                labelText = f"{i + 1}. {subtask['name']} ({subtask['time']} hrs)"
                drawLabel(labelText, self.app.width / 2, y, size=16, align='left-top')
                
                # Add a strikethrough if the subtask is done
                if subtask.get('done', False):
                    textWidth = len(labelText) * 7  # Approximation of text width
                    drawLine(500, y + 8, 
                            500 + textWidth, y + 8, 
                            fill='red', lineWidth=2)
                y += 30
        else:
            drawLabel("No subtasks defined.", self.app.width / 2, 470, size=16, align='left-top')



    def handleMousePress(self, mouseX, mouseY):
        if self.addButton.isClicked(mouseX, mouseY):
            self.app.view = 'goalSetter'

        if not self.app.goals:
            return

        
        elif self.buttons['prev'].isClicked(mouseX, mouseY):
            self.currentGoalIndex = (self.currentGoalIndex - 1) % len(self.app.goals)
        elif self.buttons['next'].isClicked(mouseX, mouseY):
            self.currentGoalIndex = (self.currentGoalIndex + 1) % len(self.app.goals)
        elif self.buttons['addSubtask'].isClicked(mouseX, mouseY):
            self.addSubtask(app)
        elif self.buttons['removeSubtask'].isClicked(mouseX, mouseY):
            self.removeSubtask()
        elif self.buttons['markDone'].isClicked(mouseX, mouseY):
            self.markSubtaskDone()
        elif self.buttons['markUnDone'].isClicked(mouseX, mouseY):
            self.unMarkSubtaskDone()
        elif self.removeButton.isClicked(mouseX, mouseY):
            self.removeGoal()

        self.subtaskNameBox.handleClick(mouseX, mouseY)
        self.subtaskTimeBox.handleClick(mouseX, mouseY)
        self.colorDropdown.handleMousePress(mouseX, mouseY)


    # Remove the current goal 
    def removeGoal(self):
        if not self.app.goals:
            self.errorMessage = "No goals available to remove."
            return

        self.app.goals.pop(self.currentGoalIndex)
        if self.currentGoalIndex >= len(self.app.goals):
            self.currentGoalIndex = len(self.app.goals) - 1

        self.errorMessage = ''

    def handleKeyPress(self, key):
        self.subtaskNameBox.handleKeyPress(key)
        self.subtaskTimeBox.handleKeyPress(key)

    def updateProgress(self, positive):
        self.updateRemainingTime()
        currentGoal = self.app.goals[self.currentGoalIndex]
        try:
            hours = int(self.textbox.text.strip())
            if positive:
                currentGoal['progress'] += (hours / currentGoal['estimatedTime']) * 100
            else:
                currentGoal['progress'] -= (hours / currentGoal['estimatedTime']) * 100

            currentGoal['progress'] = max(0, min(100, currentGoal['progress']))
            self.errorMessage = ''
        except ValueError:
            self.errorMessage = "Please enter a valid number of hours."

    # Add a subtask to the current goal
    def addSubtask(self, app):
        if not self.app.goals:
            self.errorMessage = "No goals available to add a subtask."
            return
        
        currentGoal = self.app.goals[self.currentGoalIndex]
        if currentGoal is None:
            self.errorMessage = "Current goal is not defined."
            return

        # Get the subtask name and time from the textboxes
        name = self.subtaskNameBox.text.strip()
        # try to convert the time to an integer and catch any errors  
        try:
            time = int(self.subtaskTimeBox.text.strip())
            if name and time > 0:
                if currentGoal.get('subtasks') is None:
                    currentGoal['subtasks'] = []
                currentGoal['subtasks'].append({'name': name, 'time': time, 'done': False})
                startDay = self.app.goals[self.currentGoalIndex]['deadline']
                studySessions = math.ceil(time*60 / int(app.userPreferences['studyDuration']))
                scheduler = StudySessionScheduler(app.userPreferences)
                print(1)

                fill1 = self.colorDropdown.selected.lower()
                if fill1 == 'color:':
                    fill1 = 'gray'
                scheduler.scheduleStudySessions(app, startDay, int(studySessions), fill1,f'{currentGoal['name']} - {name}')
                
                
                self.recalculateGoalMetrics(currentGoal)
                self.subtaskNameBox.reset()
                self.subtaskTimeBox.reset()
                self.errorMessage = 'event scheduled!'
            else:
                self.errorMessage = "Invalid name or hours for subtask, check inputs"
        except ValueError:
            self.errorMessage = "Please enter valid hours for the subtask."



    # Remove the last subtask from the current goal 
    def removeSubtask(self):
        currentGoal = self.app.goals[self.currentGoalIndex]
        if 'subtasks' not in currentGoal or not currentGoal['subtasks']:
            self.errorMessage = "No subtasks to remove."
            return

        currentGoal['subtasks'].pop()

        # Recalculate metrics after removing subtask
        self.recalculateGoalMetrics(currentGoal)
        self.errorMessage = 'event removed!'

    # Mark the first incomplete subtask as done 
    def markSubtaskDone(self):
        currentGoal = self.app.goals[self.currentGoalIndex]
        if 'subtasks' not in currentGoal or not currentGoal['subtasks']:
            self.errorMessage = "No subtasks to mark as done."
            return

        for subtask in currentGoal['subtasks']:
            if not subtask.get('done', False):
                subtask['done'] = True
                if currentGoal['estimatedTime'] > 0:  # Prevent division by zero
                    currentGoal['progress'] += (subtask['time'] / currentGoal['estimatedTime']) * 100
                    currentGoal['progress'] = min(100, currentGoal['progress'])
                    self.updateRemainingTime()
                break
        self.errorMessage = ''

    # Mark the last completed subtask as undone 
    def unMarkSubtaskDone(self):
        currentGoal = self.app.goals[self.currentGoalIndex]
        if 'subtasks' not in currentGoal or not currentGoal['subtasks']:
            self.errorMessage = "No subtasks to mark as undone."
            return
        # Iterate through subtasks in reverse order to find the last completed subtask and mark it undone
        for subtask in reversed(currentGoal['subtasks']):
            if subtask.get('done', False):
                subtask['done'] = False
                if currentGoal['estimatedTime'] > 0:  # Prevent division by zero
                    currentGoal['progress'] -= (subtask['time'] / currentGoal['estimatedTime']) * 100
                    currentGoal['progress'] = max(0, currentGoal['progress'])
                    self.updateRemainingTime()

                break
        self.errorMessage = ''


    def reset(self):
        self.textbox.reset()
        self.subtaskNameBox.reset()
        self.subtaskTimeBox.reset()
        self.errorMessage = ''

    # Recalculate the estimated time and progress of a goal 
    def recalculateGoalMetrics(self, goal):
        totalTime = sum(subtask['time'] for subtask in goal['subtasks'])

        remainingTime = sum(subtask['time'] for subtask in goal['subtasks'] if not subtask.get('done', False))

        goal['estimatedTime'] = totalTime  # Total time, not remaining time
        completedTime = totalTime - remainingTime

        # Safeguard against zero totalTime
        if totalTime > 0:
            goal['progress'] = (completedTime / totalTime) * 100
        else:
            goal['progress'] = 0
