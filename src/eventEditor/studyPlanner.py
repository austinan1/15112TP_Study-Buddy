import random
import datetime

class StudySessionScheduler:
    def __init__(self, preferences):
        self.preferences = preferences

    def getPreferredTimeRanges(self):
        study_time = self.preferences['studyTime'].lower()
        if study_time == 'morning':
            return (7 * 60, 12 * 60)  # 7:00 AM to 12:00 PM
        elif study_time == 'midday':
            return (11 * 60, 16 * 60)  # 12:00 PM to 5:00 PM
        elif study_time == 'afternoon':
            return (14 * 60, 19 * 60)  # 5:00 PM to 10:00 PM
        elif study_time == 'evening':
            return (17 * 60, 22 * 60) # 5:00 PM to 10:00 PM
        else:
            return (7 * 60, 22 * 60)  # Full day

    def scheduleStudySessions(self, app, testDate, studySessions,fill, name = 'Study Session'):
        
        preferred_start, preferred_end = self.getPreferredTimeRanges()
        study_duration = int(self.preferences['studyDuration'])

        if preferred_end - preferred_start < study_duration:
            raise ValueError("Preferred time range is too small to fit the study duration.")
        # this is the date of the test and todays date
        test_date = datetime.datetime.strptime(testDate, "%Y-%m-%d").date()
        current_date = datetime.date.today()


        study_days_set = set()
        while len(study_days_set) < studySessions:
            # Randomly select a day between 1 to 20 days before the test date
            offset = random.randint(1, 20)  
            candidate_date = test_date - datetime.timedelta(days=offset)
            # Only consider the days that are on or after the current date
            if candidate_date >= current_date:
                study_days_set.add(candidate_date)

        study_days = sorted(study_days_set) 

        # Schedule study sessions on the selected days
        for day in study_days:
            day_str = day.strftime("%Y-%m-%d")
            if day_str not in app.eventList:
                app.eventList[day_str] = []

            start_time_found = False  ##uses chatgpt to get randomized times 
            random_start_minutes = list(range(preferred_start, preferred_end - study_duration + 1, 5))
            random.shuffle(random_start_minutes)  


            # Try to schedule a study session at each random start time
            for start_minutes in random_start_minutes:
                end_minutes = start_minutes + study_duration

                start_time = f"{start_minutes // 60:02}:{start_minutes % 60:02}"
                end_time = f"{end_minutes // 60:02}:{end_minutes % 60:02}"

                conflict = False
                for event in app.eventList[day_str]:
                    event_start = int(event['start'][:2]) * 60 + int(event['start'][3:])
                    event_end = int(event['end'][:2]) * 60 + int(event['end'][3:])
                    if not (end_minutes <= event_start or start_minutes >= event_end):
                        conflict = True
                        break
                # If there is no conflict, schedule the study session and move to the next day
                if not conflict:
                    app.eventList[day_str].append({
                        'name': name,
                        'start': start_time,
                        'end': end_time,
                        'type': 'Study Sessions',
                        'flexible': 'Yes',
                        'fill': fill
                    })
                    start_time_found = True
                    break

            if not start_time_found:
                print(f"Could not schedule a study session on {day_str} due to conflicts.")
