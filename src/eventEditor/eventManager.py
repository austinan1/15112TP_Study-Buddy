from cmu_graphics import *
from utilities.button import Button
from utilities.dropdown import Dropdown
from utilities.textbox import Textbox
from eventEditor.studyPlanner import StudySessionScheduler

class EventManager:
    def __init__(self, app):
        self.buttons = {
            'cancel': Button(10, 10, 140, 30, 'Cancel', 16, align='left-top'),
            'save': Button(850, 10, 140, 30, 'Save', 16, align='left-top')
        }
        self.dropdowns = {
            'Type of Event': Dropdown(150, 100, 200, 40, ['Test', 'Study Sessions', 'Other'], 'What kind of event is this?', 'Select One'),
            'Flexible': Dropdown(150, 200, 200, 40, ['Yes', 'No'], 'Is this event flexible?', 'Select One'),
            'Color': Dropdown(150, 300, 200, 40, ['Red', 'Blue', 'Green', 'Yellow', 'Purple', 'Orange', 'Pink', 'Brown', 'Black', 'White'], 'Select a color', 'Select One')

        }
        self.textboxes = {
            'eventName': Textbox(500, 100, 300, 40, 'Enter event name'),
            'startDay': Textbox(500, 150, 300, 40, 'Enter event date (e.g., year-month-day)'),
            'startTime': Textbox(500, 200, 300, 40, 'Enter event time (e.g., 13:00)'),
            'endTime': Textbox(500, 250, 300, 40, 'Enter end time (e.g., 14:00)'),
            'studySessions': Textbox(500, 300, 300, 40, 'Study Sessions (max 1/day)'),
        }
        self.errorMessage = ''
        self.daysUntilEvent = None
        self.preferences = app.userPreferences

    def draw(self):
        for button in self.buttons.values():
            button.draw()

        for textboxName, textbox in self.textboxes.items():
            if textboxName == 'studySessions' and self.dropdowns['Type of Event'].selected != 'Test':
                continue
            textbox.draw()

        if self.errorMessage:
            drawLabel(self.errorMessage, app.width / 2, app.height - 50, size=16, fill='red', align='center')

        for dropdown in self.dropdowns.values():
            if dropdown.isExpanded:
                dropdown.draw()
                break
            else:
                dropdown.draw()

        if self.daysUntilEvent is not None:
            drawLabel(f"{self.daysUntilEvent} days until the event!",
                      app.width / 2, app.height - 100, size=16, fill='blue', align='center')



    def handleMousePress(self, mouseX, mouseY):
        if self.buttons['cancel'].isClicked(mouseX, mouseY):
            self.resetToDefault()
            app.view = 'calendar'
        elif self.buttons['save'].isClicked(mouseX, mouseY):
            self.saveEvent(app)

        for textboxName, textbox in self.textboxes.items():
            previouslyFocused = textbox.isFocused
            textbox.handleClick(mouseX, mouseY)

            if textboxName == 'startDay' and previouslyFocused and not textbox.isFocused:
                self.updateDaysUntilEvent()

        for dropdown in self.dropdowns.values():
            dropdown.handleMousePress(mouseX, mouseY)

    def handleKeyPress(self, key):
        for textbox in self.textboxes.values():
            textbox.handleKeyPress(key)


    # this function is called when the user clicks off on the startDay textbox
    def updateDaysUntilEvent(self):
        import datetime
        try:
            enteredDate = datetime.datetime.strptime(self.textboxes['startDay'].text.strip(), '%Y-%m-%d')
            today = datetime.datetime.now()
            delta = (enteredDate - today).days
            if delta >= 0:
                self.daysUntilEvent = delta
                self.errorMessage = ''
            else:
                self.daysUntilEvent = None
                self.errorMessage = "The date must be in the future."
        except ValueError:
            self.daysUntilEvent = None
            self.errorMessage = "Invalid date format. Use YYYY-MM-DD."

    # this function is called when the user clicks on the cancel button
    def resetToDefault(self):
        for dropdown in self.dropdowns.values():
            dropdown.selected = dropdown.default
            dropdown.close()

        for textbox in self.textboxes.values():
            textbox.reset()
    
    # this function is called from save event when
    def validateTime(self, time):
        try:
            hour, minute = map(int, time.split(':'))
            if 0 <= hour < 24 and 0 <= minute < 60:
                return True
        except ValueError:
            pass
        return False

    # this function is called when the user clicks on the save button
    def saveEvent(self, app):
        

        eventName = self.textboxes['eventName'].text.strip()
        startDay = self.textboxes['startDay'].text.strip()

        #puts event into usable format
        year, month, day = startDay.split('-')
        if len(year) != 4:
            self.errorMessage = "Invalid year. Use YYYY."
            return
        if len(month)!= 2:
            month = '0' + month
        if len(day) != 2:
            day = '0' + day
        startDay = f'{year}-{month}-{day}'
        
        startTime = self.textboxes['startTime'].text.strip()
        endTime = self.textboxes['endTime'].text.strip()
        eventType = self.dropdowns['Type of Event'].selected
        isFlexible = self.dropdowns['Flexible'].selected
        color = self.dropdowns['Color'].selected.lower()

        if not (eventName and startDay and startTime and endTime and eventType != 'Select One' and isFlexible != 'Select One'):
            self.errorMessage = "Please fill out all fields."
            return

        if not self.validateTime(startTime) or not self.validateTime(endTime):
            self.errorMessage = "Invalid time. Use HH:MM (24-hour format)."
            return


        #checks if the start time is before the end time
        indexOfColonStart = startTime.find(':')
        indexOfColonEnd = endTime.find(':')
        start_time = int(startTime[:indexOfColonStart]) * 60 + int(startTime[indexOfColonStart+1:])
        end_time = int(endTime[:indexOfColonEnd]) * 60 + int(endTime[indexOfColonEnd+1:])
        if start_time >= end_time:
            self.errorMessage = "Start time must be before end time."
            return

        if eventType == 'Test':
            studySessions = self.textboxes['studySessions'].text.strip()
            if not studySessions.isdigit() or int(studySessions) <= 0:
                self.errorMessage = "Number of study sessions must be a valid positive number."
                return

            try:
                scheduler = StudySessionScheduler(app.userPreferences)
                scheduler.scheduleStudySessions(app, startDay, int(studySessions),color,f'Study Session\n{eventName}')
            except ValueError as e:
                self.errorMessage = str(e) 
                #chatgpt in order to get the try and except values, I don't understand how it did the e value
                return

        if startDay not in app.eventList:
            app.eventList[startDay] = []
        app.eventList[startDay].append({
            'name': eventName,
            'start': startTime,
            'end': endTime,
            'type': eventType,
            'flexible': isFlexible,
            'studySessions': self.textboxes['studySessions'].text if eventType == 'Test' else None,
            'fill': color.lower()
        })

        self.resetToDefault()
        self.errorMessage = ''
        app.view = 'calendar'
