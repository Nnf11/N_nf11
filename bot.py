
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import yt_dlp
import requests
import os

# Token placeholder (Replace with your bot token)
TOKEN = "YOUR_BOT_TOKEN"

def start(update, context):
    update.message.reply_text("مرحبًا! أرسل لي رابط فيديو من YouTube, Instagram, Twitter, أو TikTok وسأقوم بتنزيله.")

def download_video(update, context):
    url = update.message.text

    if "youtube.com" in url or "youtu.be" in url or "tiktok.com" in url:
        update.message.reply_text("جاري تنزيل الفيديو، يرجى الانتظار...")
        ydl_opts = {'format': 'best', 'outtmpl': 'downloads/%(title)s.%(ext)s'}
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                video_title = ydl.prepare_filename(info)

                # Sending the video
                with open(video_title, 'rb') as video_file:
                    update.message.reply_video(video_file)

                # Removing video file after sending
                os.remove(video_title)
        except Exception as e:
            update.message.reply_text(f"حدث خطأ أثناء التنزيل: {e}")

    elif "instagram.com" in url or "twitter.com" in url:
        update.message.reply_text("جاري تنزيل الفيديو من إنستغرام أو تويتر...")
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                file_name = "downloads/video.mp4"
                with open(file_name, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        f.write(chunk)

                # Sending the video
                with open(file_name, 'rb') as video_file:
                    update.message.reply_video(video_file)

                # Removing video file after sending
                os.remove(file_name)
            else:
                update.message.reply_text("لم أتمكن من تنزيل الفيديو. يرجى التحقق من الرابط.")
        except Exception as e:
            update.message.reply_text(f"حدث خطأ أثناء التنزيل: {e}")

    else:
        update.message.reply_text("رابط غير مدعوم. يرجى إرسال رابط فيديو من YouTube, Instagram, Twitter, أو TikTok.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, download_video))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
