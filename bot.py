import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from calendar_service import tambah_event

# Token Bot Telegram lu
TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Halo, Krim! Bot kalender dan tugas siap bantu lu. "
        "Gunakan format: /tambah <Judul> | <Waktu Mulai> | <Waktu Selesai>\n"
        "Contoh: /tambah Rapat | 2026-09-10T14:00:00 | 2026-09-10T15:00:00"
    )

async def tambah_jadwal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text.replace("/tambah", "").strip()
        parts = [p.strip() for p in text.split("|")]
        
        if len(parts) < 3:
            await update.message.reply_text("Format salah, Krim! Gunakan: /tambah Judul | Waktu Mulai | Waktu Selesai")
            return
            
        summary = parts[0]
        start_time = parts[1]
        end_time = parts[2]
        
        link = tambah_event(summary, start_time, end_time)
        await update.message.reply_text(f"Mantap Krim, jadwal *{summary}* berhasil ditambah!\nCek di sini: {link}", parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"Duh error, Krim: {e}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("tambah", tambah_jadwal))
    
    print("Bot Telegram siap...")
    app.run_polling()
