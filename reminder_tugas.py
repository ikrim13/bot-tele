import os
import time
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from calendar_service import get_calendar_service
import requests

# Konfigurasi Bot Telegram lu & Chat ID lu
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = "8791729948"  

def kirim_pesan_telegram(pesan):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": pesan,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Gagal kirim pesan Telegram: {e}")

def cek_deadline_tugas():
    service = get_calendar_service()
    
    # Ambil waktu sekarang
    sekarang = datetime.utcnow()
    # Rentang waktu pengecekan (misal 3 hari ke depan)
    waktu_max = sekarang + timedelta(days=3)
    
    # Format ke RFC3339
    time_min = sekarang.isoformat() + 'Z'
    time_max = waktu_max.isoformat() + 'Z'
    
    print("Sedang mengecek deadline tugas di kalender...")
    
    events_result = service.events().list(
        calendarId='primary',
        timeMin=time_min,
        timeMax=time_max,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    events = events_result.get('items', [])

    if not events:
        print("Tidak ada tugas dalam waktu dekat.")
        return

    for event in events:
        summary = event.get('summary', 'Tanpa Judul')
        description = event.get('description', '')
        
        # CEK APA SUDAH SUBMIT: 
        # Kalau di kalender e-learning lu ada tulisan "[Submitted]" atau "Selesai",
        # bot bakal otomatis lewatin (gak ngingetin lagi).
        if "[submitted]" in summary.lower() or "[selesai]" in summary.lower() or "submitted" in description.lower():
            continue

        end_time_str = event['end'].get('dateTime') or event['end'].get('date')
        
        # Parsing waktu selesai (deadline)
        if 'T' not in end_time_str:
            continue # Lewati kalau bentuknya seharian penuh (bukan jam spesifik)
            
        deadline_time = datetime.fromisoformat(end_time_str.replace('Z', '+00:00')).replace(tzinfo=None)
        selisih = deadline_time - datetime.now()
        
        sisa_jam = selisih.total_seconds() / 3600
        
        # Logika Pengingat (2 Hari = ~48 jam, 1 Hari = ~24 jam, 2 Jam = ~2 jam)
        if 47.5 <= sisa_jam <= 48.5:
            kirim_pesan_telegram(f"⏰ *PENGINGAT TUGAS*\nTugas *{summary}* akan deadline dalam **2 hari** lagi!")
        elif 23.5 <= sisa_jam <= 24.5:
            kirim_pesan_telegram(f"⚠️ *PENGINGAT TUGAS*\nTugas *{summary}* deadline tinggal **1 hari** lagi! Jangan ditunda.")
        elif 1.8 <= sisa_jam <= 2.2:
            kirim_pesan_telegram(f"🚨 *WARNING DEADLINE DEKAT!*\nTugas *{summary}* tinggal **2 jam** lagi! Segera selesaikan!")

if __name__ == "__main__":
    print("Sistem pengingat tugas otomatis berjalan...")
    while True:
        try:
            cek_deadline_tugas()
        except Exception as e:
            print(f"Error saat cek deadline: {e}")
        
        # Program akan nge-check ulang setiap 30 menit sekali
        time.sleep(1800)
