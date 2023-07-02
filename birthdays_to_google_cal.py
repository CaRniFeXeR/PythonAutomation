import datetime
import os
from googleapiclient.discovery import build
from google.oauth2 import service_account

def create_birthday_event(service, name, birthday, calendar_id='b81729c5752c067c0840fd866d5b3654ad496785defe488655ada8198e361597@group.calendar.google.com'):
    """
    Creates a birthday event in the specified calendar. The event will be created for the current year and will recur every year.
    The dateformat is DD.MM. (e.g. 01.01. for January 1st)
    """
    year = datetime.datetime.now().year
    birthdate = datetime.datetime.strptime(birthday, "%d.%m.")
    event_start = datetime.datetime(year, birthdate.month, birthdate.day)
    event_end = event_start + datetime.timedelta(days=1)
    event = {
        'summary': f"{name}'s B-Day",
        'start': {
            'date': event_start.strftime('%Y-%m-%d')
        },
        'end': {
            'date': event_end.strftime('%Y-%m-%d')
        },
        'recurrence': ['RRULE:FREQ=YEARLY']
    }
    event = service.events().insert(calendarId=calendar_id, body=event).execute()
    print(f"Event created: {event['summary']}")

def main():
    # Set up Google Calendar API credentials
    credentials = service_account.Credentials.from_service_account_file('./data/credentials.json', scopes=['https://www.googleapis.com/auth/calendar'])
    service = build('calendar', 'v3', credentials=credentials)

    # Read data from the text file
    file_path = './data/birthdays.txt'  # Replace with the path to your text file
    if not os.path.isfile(file_path):
        print(f"File '{file_path}' not found.")
        return

    with open(file_path, 'r') as file:
        for line in file:
            name, birthday = line.strip().split(" ")
            create_birthday_event(service, name, birthday)

if __name__ == '__main__':
    main()
