import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Scopes yang dibutuhin buat baca/tulis Google Calendar
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def main():
    creds = None
    # Token.json ini bakal nyimpen token login lu supaya gak perlu login ulang tiap bot nyala
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        
        # Simpen tokennya buat pemakaian berikutnya
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build("calendar", "v3", credentials=creds)

    # Ngetes ambil 10 daftar calendar/event lu
    print("Berhasil terhubung ke Google Calendar! Mengambil daftar calendar...")
    calendar_list = service.calendarList().list().execute()
    for calendar in calendar_list.get("items", []):
        print(f"- {calendar['summary']}")

if __name__ == "__main__":
    main()