from cmu_graphics import *
from utilities.button import Button
from utilities.dropdown import Dropdown
from utilities.textbox import Textbox
import datetime



class EditEventView:
    def __init__(self, app):
        self.buttons = {
            'cancel': Button(10, 10, 140, 30, 'Cancel', 16, align='left-top'),
            'save': Button(app.width-150, 10, 140, 30, 'Save', 16, align='left-top'),
            'delete': Button(app.width-300, 10, 140, 30, 'Delete', 16, align='left-top'),
            'today': Button(820,150,100,40, 'Today',16, align= 'left-top')
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
        self.pomodoroButton = Button(150, 800, 700, 40, 'Start Pomodoro Timer', 16, align='left-top')
        self.errorMessage = ''
        self.eventData = None 
        self.mainEvent = None

    def populateEvent(self, event, selectedDate):
        self.mainEvent = event
        self.eventData = event
        self.originalDate = selectedDate  # Store the original date

        if isinstance(selectedDate, datetime.datetime):
            selectedDate = selectedDate.strftime("%Y-%m-%d")
        elif " " in selectedDate:  
            selectedDate = selectedDate.split(" ")[0]

        # fill in fields
        self.textboxes['eventName'].setText(event['name'])
        self.textboxes['startDay'].setText(selectedDate)
        self.textboxes['startTime'].setText(event['start'])
        self.textboxes['endTime'].setText(event['end'])
        self.dropdowns['Type of Event'].select(event['type'])
        self.dropdowns['Flexible'].select(event.get('flexible', 'Select One'))
        self.dropdowns['Color'].select(event.get('fill', 'Select One').capitalize())
        
        if event['type'] == 'Test':
            self.textboxes['studySessions'].setText(event.get('studySessions', ''))

        for dropdown in self.dropdowns.values():
            dropdown.isExpanded = False


    def draw(self):
        for button in self.buttons.values():
            button.draw()

        for textboxName, textbox in self.textboxes.items():
            if textboxName == 'studySessions' and self.dropdowns['Type of Event'].selected != 'Test':
                continue
            textbox.draw()
        
        for dropdown in self.dropdowns.values():
            if dropdown.isExpanded:
                dropdown.draw()
                break
            else:
                dropdown.draw()
        
        if self.dropdowns['Type of Event'].selected == 'Study Sessions':
            self.pomodoroButton.draw()

        if self.errorMessage:
            drawLabel(self.errorMessage, app.width / 2, app.height - 50, size=16, fill='red', align='center')

        

    def handleMousePress(self, mouseX, mouseY):
        if self.buttons['cancel'].isClicked(mouseX, mouseY):
            self.resetToDefault()
            app.view = 'calendar'
        elif self.buttons['save'].isClicked(mouseX, mouseY):
            self.saveEditedEvent(app)
            
            if self.errorMessage == '':
                app.view = 'calendar'
        elif self.buttons['today'].isClicked(mouseX, mouseY):
            self.textboxes['startDay'].setText(str(datetime.datetime.now()).split(" ")[0])
        elif self.buttons['delete'].isClicked(mouseX, mouseY):
            self.deleteEvent(app)
            app.view = 'calendar'
        elif self.pomodoroButton.isClicked(mouseX, mouseY):
            app.view = 'pomodoro'
            

        for textbox in self.textboxes.values():
            textbox.handleClick(mouseX, mouseY)
        for dropdown in self.dropdowns.values():
            dropdown.handleMousePress(mouseX, mouseY)

    def handleKeyPress(self, key):
        for textbox in self.textboxes.values():
            textbox.handleKeyPress(key)

    # Reset all fields to their default values if the user cancels the edit
    def resetToDefault(self):
        for dropdown in self.dropdowns.values():
            dropdown.selected = dropdown.default
            dropdown.close()

        for textbox in self.textboxes.values():
            textbox.reset()

    # Save the edited event to the event list
    def saveEditedEvent(self, app):
        if not self.eventData:
            self.errorMessage = "No event selected for editing."
            return

        eventName = self.textboxes['eventName'].text.strip()
        startDay = self.textboxes['startDay'].text.strip()

        if isinstance(startDay, datetime.datetime):
            startDay = startDay.strftime("%Y-%m-%d")

        startTime = self.textboxes['startTime'].text.strip()
        endTime = self.textboxes['endTime'].text.strip()

        # Validate and parse times, Chat gpt assisted on most of the try functions in this code.
        # Near the end of the code however, I started understanding and writing the code myself.
        try:
            start_time = int(startTime.split(':')[0]) * 60 + int(startTime.split(':')[1])
            end_time = int(endTime.split(':')[0]) * 60 + int(endTime.split(':')[1])
            if start_time >= end_time:
                self.errorMessage = "Start time must be before end time."
                return
        except (ValueError, IndexError):
            self.errorMessage = "Invalid time format. Use HH:MM."
            return

        eventType = self.dropdowns['Type of Event'].selected
        isFlexible = self.dropdowns['Flexible'].selected
        color = self.dropdowns['Color'].selected.lower()

        if not (eventName and startDay and startTime and endTime and eventType != 'Select One' and isFlexible != 'Select One' and color != 'Select One'):
            self.errorMessage = "Please fill out all fields."
            return

        if eventType == 'Test':
            studySessions = self.textboxes['studySessions'].text.strip()
            if not studySessions.isdigit():
                self.errorMessage = "Number of study sessions must be a valid number."
                return

        # Modify the event in place
        self.eventData['name'] = eventName
        self.eventData['start'] = startTime
        self.eventData['end'] = endTime
        self.eventData['type'] = eventType
        self.eventData['flexible'] = isFlexible
        self.eventData['fill'] = color
        self.eventData['studySessions'] = studySessions if eventType == 'Test' else None

        # Update the event list
        if self.originalDate != startDay:
            if self.originalDate in app.eventList:
                app.eventList[self.originalDate].remove(self.eventData)
                if not app.eventList[self.originalDate]:  
                    del app.eventList[self.originalDate]
            if startDay not in app.eventList:
                app.eventList[startDay] = []
            app.eventList[startDay].append(self.eventData)

        self.resetToDefault()
        self.errorMessage = ''



    # Delete the selected event from the event list and reset the fields
    def deleteEvent(self, app):
        if not self.eventData:
            self.errorMessage = "No event selected for deletion."
            return

        event_date = self.textboxes['startDay'].text

        if isinstance(event_date, datetime.datetime):
            event_date = event_date.strftime("%Y-%m-%d")
        event_date = event_date.strip()

        if event_date not in app.eventList:
            self.errorMessage = "Event date not found in the event list."
            return

        event_list = app.eventList[event_date]
        event_found = False

        for event in event_list:
            if (event['name'] == self.eventData['name'] and
                event['start'] == self.eventData['start'] and
                event['end'] == self.eventData['end'] and
                event['type'] == self.eventData['type'] and
                event['flexible'] == self.eventData['flexible']):
                event_list.remove(event)
                event_found = True
                break

        if not event_found:
            self.errorMessage = "Event not found in the event list."
            return

        if not event_list:
            del app.eventList[event_date]

        self.resetToDefault()
        self.errorMessage = ''

