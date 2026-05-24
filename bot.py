import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = os.getenv("TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحباً بك! 🔥 صيفط ليا رابط أي فيديو وغادي نستخرجو ونصيفطو ليك واجد.")

async def download_and_send_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    status_message = await update.message.reply_text("جاري فحص الرابط واستخراج الفيديو... ⏳")
    
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': 'video.mp4',
        'quiet': True
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        await update.message.reply_video(video=open('video.mp4', 'rb'))
        await status_message.delete()
        
        if os.path.exists("video.mp4"):
            os.remove("video.mp4")
            
    except Exception as e:
        logging.error(f"Error: {e}")
        await status_message.edit_text("❌ عذراً، وقع مشكل أثناء تحميل الفيديو. تأكد من أن الرابط صحيح أو مدعوم.")
        if os.path.exists("video.mp4"):
            os.remove("video.mp4")

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_and_send_video))
    application.run_polling()

if __name__ == '__main__':
    main()
