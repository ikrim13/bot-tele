import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def get_calendar_service():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Kalau token invalid/expired dan gak bisa refresh, perlu re-auth
            raise Exception("Token Google Calendar tidak valid atau kadaluarsa.")
            
    service = build("calendar", "v3", credentials=creds)
    return service

def tambah_event(summary, start_time, end_time, description=""):
    """
    Fungsi buat nambahin jadwal baru ke Google Calendar.
    Format waktu: '2026-09-10T10:00:00+07:00'
    """
    service = get_calendar_service()
    
    event = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': start_time,
            'timeZone': 'Asia/Jakarta',
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'Asia/Jakarta',
        },
        # INI TAMBAHAN BUAT REMINDER OTOMATIS 30 MENIT SEBELUMNYA:
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': 30},
                {'method': 'email', 'minutes': 30},
            ],
        },
    }

    event_result = service.events().insert(calendarId='primary', body=event).execute()
    return event_result.get('htmlLink')
