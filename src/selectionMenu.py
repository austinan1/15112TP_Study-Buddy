from cmu_graphics import *
from utilities.button import Button
import urllib

class selection:
    def __init__(self, app):
        self.buttons = {

            'Calendar': Button((app.width/2)-220,290,200,100,'',16, align = 'left-top'),
            'Pomodoro Timer':Button((app.width/2)+20,290,200,100,'',20,align = 'left-top'),
            'Preferences': Button((app.width/2)-220,403,200,100,'Set Preferences',16, align = 'left-top'),
            'Goals': Button((app.width/2)+20,403,200,100,'Goal Tracker',16, align = 'left-top')
        }
        self.calIcon = 'icons/icon_calendar.png'
        self.pomodoroIcon = 'icons/icon_timer.png'
    def draw(self):
        drawRect(250,80,500,100, fill = 'black',opacity = 20)
        drawLabel('School Buddy', app.width/2, 130, size=60, align='center')
        for button in self.buttons.values():
            button.draw()
        drawImage(self.calIcon, 380,340,width=50, height=50,
          opacity=100, rotateAngle=0, align='center', visible=True)
        drawImage(self.pomodoroIcon, 620,340, width=50, height=50,
          opacity=100, rotateAngle=0, align='center', visible=True)