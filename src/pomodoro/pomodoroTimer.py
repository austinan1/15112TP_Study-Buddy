from cmu_graphics import *
import datetime
from utilities.button import Button




class Pomodoro:

    def __init__(self, app):
        self.breakTime = .03
        self.studyTime = .03
        self.mode = 'paused'  
        self.pausedTime = 0  
        self.timerStarted = False
        self.fill = 'blue'

        self.timerArcStartAngle = 90
        self.timerArcSweepAngle = 360
        self.timerCenterX, self.timerCenterY = 400, 250
        self.timerArcWidth, self.timerArcHeight = 200, 200
        self.remainingTime = self.studyTime * 60  

        self.buttons = {
            'study-': Button(10, 10, 30, 30, '-', 20, align='left-top'),
            'study+': Button(120, 10, 30, 30, '+', 20, align='left-top'),
            'break-': Button(10, 50, 30, 30, '-', 20, align='left-top'),
            'break+': Button(120, 50, 30, 30, '+', 20, align='left-top'),
            'start': Button(10, 90, 140, 30, '', 16, align='left-top'),
            'reset': Button(10, 130, 140, 30, '', 16, align='left-top')
        }


    def start(self):
        #if the timer is paused, it will start the timer
        if self.mode in ['paused', 'break-paused']:
            self.startTime = datetime.datetime.now() - datetime.timedelta(seconds=self.pausedTime)
        else:
            self.startTime = datetime.datetime.now()
            if self.mode == 'paused':
                self.remainingTime = self.studyTime * 60 
            elif self.mode == 'break-paused':
                self.remainingTime = self.breakTime * 60  

        self.timerStarted = True

        if self.mode in ['paused', 'running']:
            self.mode = 'running'
        elif self.mode in ['break-paused', 'break']:
            self.mode = 'break'

        self.buttons['start'].text = 'Pause'

    def pause(self):
        #if the timer is running or on break, it will pause the timer
        if self.mode in ['running', 'break']:
            elapsedTime = (datetime.datetime.now() - self.startTime).total_seconds()
            self.pausedTime = elapsedTime

        self.timerStarted = False

        if self.mode == 'running':
            self.mode = 'paused'
        elif self.mode == 'break':
            self.mode = 'break-paused'

        self.buttons['start'].text = 'Start'

    #displays the current event and the next event on the screen
    def getEventInfo(self, app):
        now = datetime.datetime.now()
        current_day = now.strftime("%Y-%m-%d")
        current_time = now.strftime("%H:%M")

        current_event = None
        next_event = None

        if current_day in app.eventList:
            events = app.eventList[current_day]
            for event in events:
                if event['start'] <= current_time < event['end']:
                    current_event = event
                elif event['start'] > current_time:
                    if not next_event or event['start'] < next_event['start']:
                        next_event = event
        return current_event, next_event
    
    #gets called every step in the main python file, it updates the time on the timer
    def updateTime(self):
        if not self.timerStarted:
            return
        elapsedTime = (datetime.datetime.now() - self.startTime).total_seconds()
        
        if self.mode == 'running':
            totalTime = self.studyTime * 60
        elif self.mode == 'break':
            totalTime = self.breakTime * 60
        else:
            return  


        #if the timer is running, it will update the time on the timer and the arc
        self.remainingTime = max(0, totalTime - elapsedTime)
        self.timerArcSweepAngle = 360 * (self.remainingTime / totalTime)

        #if the timer runs out, it will start the break timer
        if self.remainingTime <= 0:
            if self.mode == 'running':
                self.startBreak()
            elif self.mode == 'break':
                self.resetToStudy()


    def startBreak(self):
        self.mode = 'break'
        self.timerStarted = False
        self.remainingTime = self.breakTime * 60
        self.pausedTime = 0  
        self.start()  
        self.playSound()
        
    def resetToStudy(self):
        self.mode = 'paused'
        self.remainingTime = self.studyTime * 60
        self.timerStarted = False
        self.buttons['start'].text = 'Start'
        self.pausedTime = 0
        self.timerArcSweepAngle = 360
        self.fill = 'blue'
        self.playSound()

    def handleMousePress(self, mouseX, mouseY):
        if self.buttons['study-'].isClicked(mouseX, mouseY) and self.mode in ['paused', 'break-paused']:
            self.studyTime = max(1, self.studyTime - 1)
        elif self.buttons['study+'].isClicked(mouseX, mouseY) and self.mode in ['paused', 'break-paused']:
            self.studyTime += 1
        elif self.buttons['break+'].isClicked(mouseX, mouseY) and self.mode in ['paused', 'break-paused']:
            self.breakTime += 1
        elif self.buttons['break-'].isClicked(mouseX, mouseY) and self.mode in ['paused', 'break-paused']:
            self.breakTime = max(1, self.breakTime - 1)

        if self.buttons['start'].isClicked(mouseX, mouseY):
            if self.mode in ['paused', 'break-paused']:
                self.start()  
            elif self.mode in ['running', 'break']:
                self.pause()  

        if self.buttons['reset'].isClicked(mouseX, mouseY):
            self.resetToStudy()
    
    def playSound(self):
        sound1 =  '/Users/austinan/112TP/icons/sound1.mp3'
        app.sound = Sound(sound1)
        app.sound.play()


    def draw(self, app):
        for button in app.pomodoro.buttons.values():
            button.draw()
        if self.mode == 'pomodoro':
            self.fill = 'blue'
        elif self.mode == 'break':
            self.fill = 'green'
        drawLabel('Study', 80, 25, size=20)
        drawLabel('Break', 80, 65, size=20)
        
        if self.mode in ['paused', 'break-paused']:
            textStuff = 'Start'
        else:
            textStuff = 'Pause'
        

        drawLabel(textStuff, 75, 105, size=16)
        drawLabel('Reset', 75, 145, size=16)
        
        for button in self.buttons.values():
            button.draw()
        
        drawLabel(f'{self.studyTime} Minutes', 190, 25)
        drawLabel(f'{self.breakTime} Minutes', 190, 65)
        

        drawArc(self.timerCenterX, self.timerCenterY, self.timerArcWidth, self.timerArcHeight, self.timerArcStartAngle, max(self.timerArcSweepAngle, 1), fill=self.fill, border='black')
        
        drawCircle(self.timerCenterX, self.timerCenterY, 80, fill='white', border='black')
        
        minutes = int(self.remainingTime // 60)
        seconds = int(self.remainingTime % 60)
        timeText = f"{minutes:02}:{seconds:02}"
        drawLabel(timeText, self.timerCenterX, self.timerCenterY, size=30)

        if self.mode == 'running':
            drawLabel('STUDY',150,300, size = 20)
        elif self.mode == 'break':
            drawLabel('RELAX TIME',150,300, size = 20)
        elif self.mode == 'paused':
            drawLabel('PAUSED',150,300, size = 20)
        elif self.mode == 'break-paused':
            drawLabel('BREAK PAUSED',150,300, size = 20)

        current_event, next_event = self.getEventInfo(app)
        
        if current_event:
            drawLabel(f"Current: {current_event['name']} ({current_event['start']} - {current_event['end']})", 
                      400, 400, size=16, align='center')
        else:
            drawLabel("Current: None", 400, 400, size=16, align='center')

        if next_event:
            drawLabel(f"Next: {next_event['name']} ({next_event['start']} - {next_event['end']})", 
                      400, 430, size=16, align='center')
        else:
            drawLabel("Next: None", 400, 430, size=16, align='center')