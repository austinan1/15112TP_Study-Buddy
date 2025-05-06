from time import strptime
from utilities.button import Button
from cmu_graphics import *
import calendar
from datetime import datetime, timedelta
import datetime



class Calendar:
    def __init__(self, app):

        self.view = 'month'         

        self.currentDate = datetime.datetime.now() 
        self.selectedDate = self.currentDate
        self.currentTime = datetime.datetime.now().time()
        
        self.eventRects = []  
        self.editingEvent = None

        self.buttons = {
            'month': Button(10, 10, 100, 30, 'Month View', 16,align='left-top'),
            'week': Button(120, 10, 100, 30, 'Week View', 16, align='left-top'),
            'day': Button(230, 10, 100, 30, 'Day View',16, align='left-top'),
            'prev': Button(350, 10, 50, 30, '<',20, align='left-top'),
            'next': Button(410, 10, 50, 30, '>',20, align='left-top'),
            'home': Button(470,10,80,30, 'Today',16, align = 'left-top'),
            'add': Button(580,50,400,30, 'Add Event',16, align = 'left-top')
        }

        

    def draw(self):
        drawLabel(self.currentDate.strftime('Current Date: %A, %B %d, %Y'), 780,30, size=20, align='center')
        for button in self.buttons.values():
            button.draw()
        
        if self.view == 'month':
            self.drawMonthView(app.eventList)
        elif self.view == 'week':
            self.drawWeeklyView(app.eventList, self.selectedDate.strftime('%Y-%m-%d'))
        elif self.view == 'day':
            self.drawDayView()


    def handleMousePress(self, mouseX, mouseY):
        if self.buttons['month'].isClicked(mouseX, mouseY):
            self.view = 'month'
        elif self.buttons['week'].isClicked(mouseX, mouseY):
            self.view = 'week'
        elif self.buttons['day'].isClicked(mouseX, mouseY):
            self.view = 'day'
        elif self.buttons['prev'].isClicked(mouseX, mouseY):
            self.goToPrevious()
        elif self.buttons['next'].isClicked(mouseX, mouseY):
            self.goToNext()
        elif self.buttons['home'].isClicked(mouseX,mouseY):
            self.selectedDate = self.currentDate
        elif self.buttons['add'].isClicked(mouseX, mouseY):
            app.view = 'addEvent'
        
        #if it is in day view, check if the user clicked on an event, if so, pull up the edit event view
        for eventRect in self.eventRects:
            rectX, rectY, rectW, rectH = eventRect['rect']
            if rectX <= mouseX <= rectX + rectW and rectY <= mouseY <= rectY + rectH:
                self.editingEvent = eventRect['event']  # Set the editing event
                app.editor.populateEvent(self.editingEvent,self.selectedDate)  # Populate EditEventView
                app.view = 'editEvent'  
                return
        
        # if not in day view, check if the user clicked on a day, if so, switch to day view for that date
        if self.view in {'month', 'week'}:
            for dayRect in self.dayRects:
                rectX, rectY, rectW, rectH = dayRect['rect']
                if rectX <= mouseX <= rectX + rectW and rectY <= mouseY <= rectY + rectH:
                    self.selectedDate = dayRect['date']
                    self.view = 'day'
                    break
        

    def drawMonthView(self,eventList):

        self.dayRects = []

        #used chatgpt to get the days in the month and the first day of the month
        nextMonth = self.selectedDate.replace(day=28) + datetime.timedelta(days=4)  
        daysInMonth = (nextMonth - datetime.timedelta(days=nextMonth.day)).day 
        firstDayOfMonth = (self.selectedDate.replace(day=1).weekday() + 1)%7  

        #draw the month and year label
        daySize = 90
        gridX, gridY = app.width/2 - ((daySize * 7)/2), 150
        drawLabel(self.selectedDate.strftime('%B %Y'), gridX, gridY - 30, size=20, align='left')

        # Draw the 7 day labels
        dayCounter = 1
        weekdays = ["Sun","Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        for col in range(7):
            drawRect(gridX + col*daySize, gridY, daySize, daySize, border='black', borderWidth=1, fill = rgb(124, 230, 242))
            drawLabel(weekdays[col], gridX + col * daySize + daySize / 2, gridY - 20 + daySize / 2, align='center')

        # Draw the days of the month in a grid layout
        for row in range(6):  
            for col in range(7): 
                x = gridX + col * daySize
                y = gridY + (row + 1) * daySize

                # skip the days before the first day of the month and after the last day of the month
                if (row == 0 and col < firstDayOfMonth) or dayCounter > daysInMonth:
                    continue
                 ##i used chatgpt here becasue the .day wasnt working
                if (dayCounter == self.currentDate.day and self.selectedDate.month == self.currentDate.month and self.selectedDate.year == self.currentDate.year):
                    fill = 'lightblue'
                else:
                    fill = 'lightgray'
                
                drawRect(x, y, daySize, daySize, fill=fill, border='black', borderWidth=1)
                drawLabel(str(dayCounter), x + daySize / 2, y -6+ daySize / 2, align='center')

                # Draw a circle if there is an event on that day
                date_str = self.selectedDate.replace(day=dayCounter).strftime('%Y-%m-%d')
                if date_str in eventList:
                    drawCircle(x + daySize / 2, y + 12 + daySize / 2,7, fill = 'red', border = 'black')
                
                # Store the rectangle and the date for each day so we can click on them later
                self.dayRects.append({
                    'rect': (x, y, daySize, daySize),
                    'date': self.selectedDate.replace(day=dayCounter)
                })
                dayCounter += 1
                # Break if we have drawn all the days in the month
                if dayCounter > daysInMonth:
                    drawRect(gridX,gridY,7*daySize,(row+2) * daySize, fill = None, border = 'black' )
                    break
    
    def drawWeeklyView(self, eventList, startDate):
        from datetime import datetime, timedelta
        
        self.dayRects = []

        start_date_obj = datetime.strptime(startDate, '%Y-%m-%d')

        days_to_sunday = (start_date_obj.weekday() + 1) % 7
        start_date_obj -= timedelta(days=days_to_sunday)
        end_date_obj = start_date_obj + timedelta(days=6)

        dateRangeLabel = f'{start_date_obj.strftime("%b %d, %Y")} - {end_date_obj.strftime("%b %d, %Y")}'
        gridX, gridY = 250, 170
        drawLabel(dateRangeLabel, gridX + 245, gridY - 60, size=18, align='center')

        days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        dayWidth = 70
        hourHeight = 25


        # Draw the day labels
        for i in range(len(days)):
            x = gridX + i * dayWidth
            current_date = start_date_obj + timedelta(days=i)
            drawLabel(days[i], x + dayWidth / 2, gridY - 30, size=16, align='center')
            drawLabel(current_date.strftime('%b %d'), x + dayWidth / 2, gridY -15, size=14, align='center')
            self.dayRects.append({
                'rect': (x, gridY, dayWidth, 24 * hourHeight),
                'date': current_date
            })
        # Draw the time slots for each hour of the day and the grid lines
        for i in range(24):
            y = gridY + i * hourHeight
            if i < 13:
                if i == 0:
                    label = 12
                else:
                    label = i
                drawLabel(f'{label} AM', gridX - 30, y - 12.5 + hourHeight / 2, size=12, align='center')
            else:
                drawLabel(f'{i - 12} PM', gridX - 30, y - 12.5 + hourHeight / 2, size=12, align='center')
            for j in range(len(days)):
                x = gridX + j * dayWidth
                drawRect(x, y, dayWidth, hourHeight, border='gray', borderWidth=1, fill=None)

        for date, events in eventList.items():
            event_date = datetime.strptime(date, '%Y-%m-%d')
            # Check if the event date is within the current week, if it is draw all events in the date
            if start_date_obj <= event_date <= end_date_obj:
                day_index = (event_date - start_date_obj).days
                
                # Draw each event as a rectangle on the calendar grid depending on the start and end times
                for event in events:
                    eventColor = event.get('fill', 'gray')
                    eventOpacity = 100 if event.get('flexible', 'No') == 'Yes' else 50

                    indexOfColonStart = event['start'].index(':')
                    indexOfColonEnd = event['end'].index(':')
                    
                    # Calculate the start and end times of the event in terms of y-coordinates
                    start_hour = int(event['start'][:indexOfColonStart])
                    start_minute = int(event['start'][indexOfColonStart+1:])
                    end_hour = int(event['end'][:indexOfColonEnd])
                    end_minute = int(event['end'][indexOfColonEnd+1:])

                    start_y = gridY + (start_hour + start_minute / 60) * hourHeight
                    end_y = gridY + (end_hour + end_minute / 60) * hourHeight
                    eventHeight = end_y - start_y

                    x = gridX + day_index * dayWidth
                    drawRect(x, start_y, dayWidth, eventHeight, fill=eventColor, opacity=eventOpacity, border='black')
                    drawLabel(event['name'], x + dayWidth / 2, start_y + eventHeight / 2, size=10, align='center')

        # Highlight current day by drawing a yellow rectangle
        current_date = datetime.now()
        if start_date_obj <= current_date <= end_date_obj:
            day_index = (current_date - start_date_obj).days
            x = gridX + day_index * dayWidth
            drawRect(x, gridY, dayWidth, 24 * hourHeight, fill='yellow', opacity=20)

        # Draw the current time line
        if start_date_obj <= current_date <= end_date_obj:
            day_index = (current_date - start_date_obj).days
            x = gridX + day_index * dayWidth
            y = gridY + current_date.hour * hourHeight + (current_date.minute / 60) * hourHeight
            drawLine(x, y, x + dayWidth, y, lineWidth=2, fill='red')
            drawCircle(x + dayWidth, y, 5, fill='red')


    # Draw the day view with events and time slots for the selected date 
    def drawDayView(self):
        gridX, gridY = 120, 100
        dayWidth = 200  
        hourHeight = 30  

        self.eventRects = []

        drawLabel(self.selectedDate.strftime('%A, %B %d, %Y'), gridX + dayWidth / 2, gridY - 20, size=20, align='center')

        # Draw the time slots for each hour of the day and the grid lines
        for hour in range(24):
            y = gridY + hour * hourHeight
            timeLabel = f'{hour % 12 or 12} {"AM" if hour < 12 else "PM"}'
            drawLabel(timeLabel, gridX - 30, y - 15 + hourHeight / 2, size=12, align='center')
            drawRect(gridX, y, dayWidth, hourHeight, border='gray', borderWidth=1, fill=None)

        dateStr = self.selectedDate.strftime('%Y-%m-%d')
        if dateStr in app.eventList:
            events = app.eventList[dateStr]

            # Draw each event as a rectangle on the calendar grid depending on the start and end times
            for event in events:
                eventColor = event.get('fill', 'gray')
                eventOpacity = 100 if event.get('flexible', 'No') == 'Yes' else 50
                
                indexOfColonStart = event['start'].index(':')
                indexOfColonEnd = event['end'].index(':')

                # Calculate the start and end times of the event in terms of y-coordinates
                start_hour = int(event['start'][:indexOfColonStart])
                start_minute = int(event['start'][indexOfColonStart+1:])
                end_hour = int(event['end'][:indexOfColonEnd])
                end_minute = int(event['end'][indexOfColonEnd+1:])

                start_y = gridY + (start_hour + start_minute / 60) * hourHeight
                end_y = gridY + (end_hour + end_minute / 60) * hourHeight
                eventHeight = end_y - start_y

                drawRect(gridX, start_y, dayWidth, eventHeight, fill=eventColor, border='black', borderWidth=1, opacity=eventOpacity)
                drawLabel(event['name'], gridX + dayWidth / 2, start_y + eventHeight / 2, size=12, align='center')
                self.eventRects.append({
                    'rect': (gridX, start_y, dayWidth, eventHeight),
                    'event': event
                })
        # Highlight current time by drawing a line and a circle indicating the current time
        current_date = datetime.datetime.now()
        if current_date.date() == self.selectedDate.date():
            y = gridY + current_date.hour * hourHeight + (current_date.minute / 60) * hourHeight
            drawLine(gridX, y, gridX + dayWidth + 10, y, lineWidth=2, fill='red')
            drawCircle(gridX + dayWidth + 10, y, 5, fill='red')

    # Move to the previous month, week, or day based on the current view
    def goToPrevious(self):
        if self.view == 'month':
            prevMonth = self.selectedDate.month - 1 if self.selectedDate.month > 1 else 12
            year = self.selectedDate.year - 1 if prevMonth == 12 else self.selectedDate.year
            self.selectedDate = self.selectedDate.replace(year=year, month=prevMonth)
        elif self.view == 'week':
            self.selectedDate -= datetime.timedelta(weeks=1)
        elif self.view == 'day':
            self.selectedDate -= datetime.timedelta(days=1)

    # Move to the next month, week, or day based on the current view
    def goToNext(self):
        if self.view == 'month':
            nextMonth = self.selectedDate.month + 1 if self.selectedDate.month < 12 else 1
            year = self.selectedDate.year + 1 if nextMonth == 1 else self.selectedDate.year
            self.selectedDate = self.selectedDate.replace(year=year, month=nextMonth)
        elif self.view == 'week':
            self.selectedDate += datetime.timedelta(weeks=1)
        elif self.view == 'day':
            self.selectedDate += datetime.timedelta(days=1)
