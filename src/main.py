from cmu_graphics import *
from utilities.button import Button
from cal import Calendar
from selectionMenu import selection
from pomodoro.pomodoroTimer import Pomodoro
from eventEditor.eventManager import EventManager
from preferences import PreferencesView
from eventEditor.eventEditor import EditEventView
import webbrowser

from goal.goalViewer import GoalViewer
from goal.goalSetter import GoalSetter


def onAppStart(app):
    
    app.width, app.height = 1000, 840
    
    ## CHANGE LATER
    app.view = 'menu'

    app.buttons = {
        'resize': Button(app.width-50, app.height-50, 50, 50, '', 20, 'left-top'),
        'menu': Button(app.width-150, app.height-50, 50, 50, 'Menu', 16, 'left-top'),
        'help': Button(app.width-100, app.height-50,50,50,'Help',16,'left-top')
    }

    #change later set defualt preferences for ease of use
    app.userPreferences = {}  
    app.resetIconURL = 'icons/icon_reset.png'
    app.calendar = Calendar(app)
    app.pomodoro = Pomodoro(app)
    app.menuSelection = selection(app)
    app.addEvent = EventManager(app)
    app.preferences = PreferencesView(app)
    app.editor = EditEventView(app)
    app.goalViewer = GoalViewer(app)
    app.goalSetter = GoalSetter(app)

    app.goals = []
    app.eventList = {}
    app.loaded = False
    

def onStep(app):
    if app.view == 'pomodoro': 
        app.pomodoro.updateTime()


#redraws all the elements on the screen
def redrawAll(app):
    drawImage(app.resetIconURL, app.width, app.height, width=50, height=50,opacity=100, align='right-bottom')
    app.buttons['resize'].draw()
    app.buttons['help'].draw()


    if app.view == 'menu':
        app.menuSelection.draw()
    elif app.view == 'calendar':
        app.calendar.draw()
        app.buttons['menu'].draw()
    elif app.view == 'pomodoro':
        app.pomodoro.draw(app)
        app.buttons['menu'].draw()
    elif app.view == 'preferences':
        app.preferences.draw()
        app.buttons['menu'].draw()
    elif app.view == 'addEvent':
        app.addEvent.draw()
        app.buttons['menu'].draw()
    elif app.view == 'editEvent':
        app.editor.draw()
        app.buttons['menu'].draw()

    elif app.view == 'goalViewer':
        app.goalViewer.draw()
        app.buttons['menu'].draw()

    elif app.view == 'goalSetter':
        app.goalSetter.draw()
        app.buttons['menu'].draw()
    

#handles mouse press events
def onMousePress(app, mouseX, mouseY):
    if app.buttons['resize'].isClicked(mouseX, mouseY):
        app.width, app.height = 1000, 875
    elif app.buttons['help'].isClicked(mouseX, mouseY):
        url = "https://pastebin.com/kMbtuET5"
        webbrowser.open(url)
    elif app.view == 'menu':
        handleMenuClick(app, mouseX, mouseY)            
    elif app.view == 'pomodoro':
        handlePomodoroClick(app, mouseX, mouseY)
    elif app.view == 'calendar':
        handleCalendarClick(app, mouseX, mouseY)
    elif app.view == 'addEvent':
        handleAddEventPress(app, mouseX, mouseY)
    elif app.view == 'preferences':
        handlePreferencesClick(app, mouseX, mouseY)
    elif app.view == 'editEvent':
        handleEditEventClick(app, mouseX, mouseY)
    elif app.view == 'goalSetter':
        handleGoalSetterClick(app, mouseX, mouseY)
    elif app.view == 'goalViewer':
        handleGoalViewerClick(app, mouseX, mouseY)

def handleGoalViewerClick(app, mouseX, mouseY):
    app.goalViewer.handleMousePress(mouseX, mouseY)
    if app.buttons['menu'].isClicked(mouseX, mouseY):
        app.view = 'menu'

def handleGoalSetterClick(app, mouseX, mouseY):
    app.goalSetter.handleMousePress(mouseX,  mouseY)
    if app.buttons['menu'].isClicked(mouseX, mouseY):
        app.view = 'menu'

def handleEditEventClick(app, mouseX, mouseY):
    app.editor.handleMousePress(mouseX, mouseY)
    if app.buttons['menu'].isClicked(mouseX, mouseY):
        app.view = 'menu'

def handlePreferencesClick(app, mouseX, mouseY):
    app.preferences.handleMousePress(mouseX, mouseY)
    if app.buttons['menu'].isClicked(mouseX, mouseY):
        app.view = 'menu'

def handleMenuClick(app, mouseX, mouseY):
    if app.menuSelection.buttons['Calendar'].isClicked(mouseX, mouseY):
        app.view = 'calendar'
    elif app.menuSelection.buttons['Pomodoro Timer'].isClicked(mouseX, mouseY):
        app.view = 'pomodoro'
    elif app.menuSelection.buttons['Preferences'].isClicked(mouseX, mouseY):
        app.view = 'preferences'
        app.preferences.populatePreferences(app.userPreferences)

    elif app.menuSelection.buttons['Goals'].isClicked(mouseX, mouseY):
        app.view = 'goalViewer'
    

def handleAddEventPress(app, mouseX, mouseY):
    app.addEvent.handleMousePress(mouseX, mouseY)
    if app.buttons['menu'].isClicked(mouseX, mouseY):
        app.view = 'menu'

def handlePomodoroClick(app, mouseX, mouseY):
    app.pomodoro.handleMousePress(mouseX, mouseY)
    if app.buttons['menu'].isClicked(mouseX, mouseY):
        app.view = 'menu'

def handleCalendarClick(app, mouseX, mouseY):
    app.calendar.handleMousePress(mouseX, mouseY)
    if app.buttons['menu'].isClicked(mouseX, mouseY):
        app.view = 'menu'
    
def onResize(app):
    app.buttons['resize'].updatePosition(app.width-50, app.height-50)
    app.buttons['menu'].updatePosition(app.width-100, app.height-50)


#takes inputs of keypress and depending on what view it is, sends the input to that view
def onKeyPress(app, key):
    if app.view == 'addEvent':
        app.addEvent.handleKeyPress(key)
    if app.view == 'preferences':
        app.preferences.handleKeyPress(key)
    if app.view == 'editEvent':
        app.editor.handleKeyPress(key)
    if app.view == 'goalSetter':
        app.goalSetter.handleKeyPress(key)
    if app.view == 'goalViewer':
        app.goalViewer.handleKeyPress(key)
    if key == '~':
        if app.loaded == False:
            loadAll(app)
            app.loaded = True
        elif app.loaded == True:
            unloadAll(app)
            app.loaded = False

#unloads all the events and goals
def unloadAll(app):
    app.goals = []
    app.eventList = {}
    app.userPreferecnes = {}
#loads all the events and goals just to see what it should look like in use 
def loadAll(app):
    app.userPreferences = {'studyTime': 'Evening', 'bedtime': '22:00', 'wakeupTime': '07:00', 'studyDuration': '90'}

    app.eventList = {
    '2024-12-04': [
        {'name': 'Math Study Group', 'start': '08:30', 'end': '09:30', 'type': 'Study Session', 'flexible': 'Yes', 'fill': 'blue'}
    ],
    '2024-12-06': [
        {'name': 'Morning Workout', 'start': '07:00', 'end': '08:00', 'type': 'Personal', 'flexible': 'Yes', 'fill': 'orange'}
    ],
    '2024-12-08': [
        {'name': 'Team Presentation', 'start': '14:00', 'end': '15:30', 'type': 'Meeting', 'flexible': 'No', 'fill': 'green'}
    ],
    '2024-12-09': [
        {'name': 'Physics Exam Review', 'start': '10:00', 'end': '11:30', 'type': 'Study Session', 'flexible': 'Yes', 'fill': 'blue'}
    ],
    '2024-12-10': [
        {'name': 'Weekly Planner Update', 'start': '12:00', 'end': '12:30', 'type': 'Personal', 'flexible': 'Yes', 'fill': 'orange'},
        {'name': 'CS Lecture', 'start': '14:00', 'end': '15:00', 'type': 'Class', 'flexible': 'No', 'fill': 'purple'}
    ],
    '2024-12-12': [
        {'name': 'Chemistry Lab Report', 'start': '10:00', 'end': '12:00', 'type': 'Study Session', 'flexible': 'Yes', 'fill': 'blue'}
    ],
    '2024-12-14': [
        {'name': 'Dentist Appointment', 'start': '09:00', 'end': '09:30', 'type': 'Personal', 'flexible': 'No', 'fill': 'red'}
    ],
    '2024-12-15': [
        {'name': 'Project Deadline', 'start': '20:00', 'end': '21:00', 'type': 'Work', 'flexible': 'No', 'fill': 'red'}
    ],
    '2024-12-17': [
        {'name': 'Grocery Shopping', 'start': '15:00', 'end': '15:45', 'type': 'Personal', 'flexible': 'Yes', 'fill': 'orange'}
    ],
    '2024-12-18': [
        {'name': 'Machine Learning Lecture', 'start': '10:00', 'end': '11:30', 'type': 'Class', 'flexible': 'No', 'fill': 'purple'}
    ],
    '2024-12-21': [
        {'name': 'Programming Hackathon', 'start': '08:00', 'end': '20:00', 'type': 'Event', 'flexible': 'No', 'fill': 'teal'}
    ],
    '2024-12-23': [
        {'name': 'Family Dinner', 'start': '18:00', 'end': '20:00', 'type': 'Personal', 'flexible': 'No', 'fill': 'red'}
    ],
    '2024-12-27': [
        {'name': 'CS Assignment Submission', 'start': '21:00', 'end': '22:00', 'type': 'Work', 'flexible': 'No', 'fill': 'red'}
    ],
    '2024-12-30': [
        {'name': 'New Year’s Eve Preparation', 'start': '17:00', 'end': '19:00', 'type': 'Personal', 'flexible': 'Yes', 'fill': 'orange'}
    ],
    '2025-01-02': [
        {'name': 'Goal Planning for 2025', 'start': '09:00', 'end': '10:00', 'type': 'Personal', 'flexible': 'Yes', 'fill': 'orange'}
    ],
    '2025-01-06': [
        {'name': 'Networking Event', 'start': '17:30', 'end': '19:30', 'type': 'Event', 'flexible': 'No', 'fill': 'teal'}
    ],
    '2025-01-08': [
        {'name': 'Math Tutoring Session', 'start': '14:00', 'end': '15:00', 'type': 'Study Session', 'flexible': 'Yes', 'fill': 'blue'}
    ],
    '2025-01-10': [
        {'name': 'Final Project Presentation', 'start': '09:00', 'end': '10:30', 'type': 'Work', 'flexible': 'No', 'fill': 'green'}
    ]
}

    app.goals = [
    {
        'name': 'Complete Python App',
        'description': 'Develop and finalize the Python productivity app with calendar and Pomodoro features.',
        'deadline': '2024-12-20',
        'estimatedTime': 15,
        'priority': 'High',
        'category': 'Work',
        'progress': 0,
        'subtasks': [
            {'name': 'Design UI mockups', 'time': 3, 'done': False},
            {'name': 'Implement calendar module', 'time': 5, 'done': False},
            {'name': 'Integrate Pomodoro timer', 'time': 4, 'done': False},
            {'name': 'Test and debug features', 'time': 3, 'done': False}
        ]
    },
    {
        'name': 'Prepare for Final Exams',
        'description': 'Create a study schedule and prepare for all final exams.',
        'deadline': '2024-12-18',
        'estimatedTime': 20,
        'priority': 'High',
        'category': 'Education',
        'progress': 0,
        'subtasks': [
            {'name': 'Review lecture notes for Statistics', 'time': 5, 'done': True},
            {'name': 'Practice past exams for Business Analytics', 'time': 7, 'done': False},
            {'name': 'Organize group study for Machine Learning', 'time': 3, 'done': False},
            {'name': 'Summarize key concepts for Hunger class', 'time': 5, 'done': False}
        ]
    },
    {
        'name': 'Apply for Summer Internships',
        'description': 'Submit applications for summer internships in consulting and product management.',
        'deadline': '2024-12-30',
        'estimatedTime': 10,
        'priority': 'Medium',
        'category': 'Career',
        'progress': 0,
        'subtasks': [
            {'name': 'Update resume and LinkedIn profile', 'time': 2, 'done': True},
            {'name': 'Research target companies', 'time': 3, 'done': True},
            {'name': 'Write and customize cover letters', 'time': 3, 'done': False},
            {'name': 'Submit 10 applications', 'time': 2, 'done': False}
        ]
    },
    {
        'name': 'Plan a Family Trip',
        'description': 'Organize a trip with family for the winter break.',
        'deadline': '2024-12-25',
        'estimatedTime': 5,
        'priority': 'Low',
        'category': 'Personal',
        'progress': 0,
        'subtasks': [
            {'name': 'Finalize destination', 'time': 1, 'done': True},
            {'name': 'Book flights and accommodations', 'time': 2, 'done': True},
            {'name': 'Plan itinerary', 'time': 1, 'done': True},
            {'name': 'Pack luggage and essentials', 'time': 1, 'done': True}
        ]
    }
]


def main():
    runApp()
main()
