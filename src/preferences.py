from cmu_graphics import *
from utilities.button import Button
from utilities.dropdown import Dropdown
from utilities.textbox import Textbox


class PreferencesView:
    def __init__(self, app):
        self.buttons = {
            'save': Button(app.width - 150, 10, 140, 30, 'Save', 16, align='left-top'),
            'cancel': Button(10, 10, 140, 30, 'Cancel', 16, align='left-top'),
        }
        self.dropdowns = {
            'studyTime': Dropdown(
                200, 200, 200, 40,
                ['Morning', 'Midday', 'Afternoon', 'Evening'],
                'Preferred Study Time',
                'Select One'
            ),
            'studyDuration': Dropdown(
                200, 300, 200, 40,
                ['30', '60', '90', '120', '150', '180'],
                'Preferred Study Duration',
                'Select One'
            ),
        }
        self.textboxes = {
            'bedtime': Textbox(500, 300, 300, 40, 'Bedtime (e.g., 22:00)'),
            'wakeupTime': Textbox(500, 200, 300, 40, 'Wakeup Time (e.g., 7:00)'),
        }
        self.errorMessage = ''
        self.preferencesData = None  # placeholder for preferences being edited


    #fills in user preferences using predetermined values
    def populatePreferences(self, preferences):
        self.preferencesData = preferences
        self.dropdowns['studyTime'].select(preferences.get('studyTime', 'Select One'))
        self.dropdowns['studyDuration'].select(preferences.get('studyDuration', 'Select One'))
        self.textboxes['bedtime'].setText(preferences.get('bedtime', ''))
        self.textboxes['wakeupTime'].setText(preferences.get('wakeupTime', ''))

    def draw(self):
        drawLabel('Prefered Wakeup Time',500,180,size = 16, align = 'left')
        drawLabel('Prefered Bedtime',500,280,size = 16, align = 'left')

        #draw all buttons, dropdowns, and textboxes
        for button in self.buttons.values():
            button.draw()

        for dropdown in self.dropdowns.values():
            if dropdown.isExpanded:
                dropdown.draw()
                break
            else:
                dropdown.draw()

        for textbox in self.textboxes.values():
            textbox.draw()

        if self.errorMessage:
            drawLabel(self.errorMessage, app.width / 2, app.height - 50, size=16, fill='red', align='center')

    def handleMousePress(self, mouseX, mouseY):
        if self.buttons['cancel'].isClicked(mouseX, mouseY):
            self.resetToDefault()
            app.view = 'menu'
        elif self.buttons['save'].isClicked(mouseX, mouseY):
            self.savePreferences(app)
            if self.errorMessage == '':
                app.view = 'menu'

        for dropdown in self.dropdowns.values():
            dropdown.handleMousePress(mouseX, mouseY)

        for textbox in self.textboxes.values():
            textbox.handleClick(mouseX, mouseY)

    def handleKeyPress(self, key):
        for textbox in self.textboxes.values():
            textbox.handleKeyPress(key)

    def resetToDefault(self):
        for dropdown in self.dropdowns.values():
            dropdown.selected = dropdown.default
            dropdown.close()

        for textbox in self.textboxes.values():
            textbox.reset()

        self.errorMessage = ''

    #saves user preferences to the app object and resets the view to the menu
    def savePreferences(self, app):
        studyTime = self.dropdowns['studyTime'].selected
        studyDuration = self.dropdowns['studyDuration'].selected
        bedtime = self.textboxes['bedtime'].text.strip()
        wakeupTime = self.textboxes['wakeupTime'].text.strip()

        if not (studyTime != 'Select One' and studyDuration != 'Select One' and bedtime and wakeupTime):
            self.errorMessage = "Please fill out all fields correctly."
            return

        app.userPreferences = {
            'studyTime': studyTime,
            'studyDuration': studyDuration,
            'bedtime': bedtime,
            'wakeupTime': wakeupTime
        }

        self.errorMessage = ''
        self.resetToDefault()
