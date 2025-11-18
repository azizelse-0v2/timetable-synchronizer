from pdfr import Grade, extract_pdf_info, output_info

from datetime import datetime, timezone, timedelta,date
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]

start_times = [
    "08:30:00",
    "09:20:00",
    "10:10:00",
    "11:25:00",
    "12:15:00",
    "14:00:00",
    "14:50:00",
    "15:40:00",
]

end_times = [
    "09:15:00",
    "10:05:00",
    "10:55:00",
    "12:10:00",
    "13:00:00",
    "14:45:00",
    "15:35:00",
    "16:25:00",
]

"""
#template for event
# event = {
#   'summary': 'Google I/O 2015',
#   'location': '800 Howard St., San Francisco, CA 94103',
#   'description': 'A chance to hear more about Google\'s developer products.',
#   'start': {
#     'dateTime': '2015-05-28T09:00:00-07:00',
#     'timeZone': 'America/Los_Angeles',
#   },
#   'end': {
#     'dateTime': '2015-05-28T17:00:00-07:00',
#     'timeZone': 'America/Los_Angeles',
#   },
#   'recurrence': [
#     'RRULE:FREQ=DAILY;COUNT=2'
#   ],
#   'attendees': [
#     {'email': 'lpage@example.com'},
#     {'email': 'sbrin@example.com'},
#   ],
#   'reminders': {
#     'useDefault': False,
#     'overrides': [
#       {'method': 'email', 'minutes': 24 * 60},
#       {'method': 'popup', 'minutes': 10},
#     ],
#   },
# }

# event = service.events().insert(calendarId='primary', body=event).execute()
# print 'Event created: %s' % (event.get('htmlLink'))
"""

def main():
    grade = Grade.get()
    info = extract_pdf_info("timetable.pdf", grade=grade)
    events = []
    week_events = []
    # output_info(info)

    for day_index in range(len(info)):
        day = info[day_index]
        real_index=0
        for lesson in day:# lesson["lesson_info"], lesson["double_lesson"]
            day_date = (date(2025,11,17) + timedelta(days=day_index)).isoformat()#safe date generation
            event = {
                "summary": lesson["lesson_info"][1],
                "location": "Presidential School in Tashkent",
                "description": f"Rooms: {lesson['lesson_info'][0]}\nTeachers: {lesson['lesson_info'][2]}",
                "start": {
                    "dateTime": f"{day_date}T{start_times[real_index]}+05:00",
                    "timeZone": "Asia/Tashkent",
                },
                "end": {
                    "dateTime": f"{day_date}T{end_times[real_index+(1 if lesson["double_lesson"] else 0)]}+05:00",
                    "timeZone": "Asia/Tashkent",
                },
                "recurrence": ["RRULE:FREQ=WEEKLY"],
            }
            real_index+=1+lesson["double_lesson"]
            week_events.append(event)
        events.append(week_events)


    #validating user token
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)
        # now = datetime.now(tz=timezone.utc).isoformat()
        # for day_events in events:
        #     for event in day_events:
        #       event = service.events().insert(calendarId="primary", body=event).execute()
        #       print(f"Event created: {event.get('htmlLink')}")
        for event in week_events:
            event = service.events().insert(calendarId="primary", body=event).execute()
            # print(event)
            # print("--------------------")
            print(f"Event created: {event.get('htmlLink')}")

    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    main()
