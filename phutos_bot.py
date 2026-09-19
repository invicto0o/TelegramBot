import os
import telebot
import yt_dlp

# حط التوكن حقك هنا اللي طلعته من BotFather
TOKEN = "8932107945:AAGfl0QWHOHv27bGj_zTqr7Z9I7AoAATW34"
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك يا كابتن يزن! أرسل لي أي رابط من تيك توك، إنستقرام، يوتيوب أو سناب وأبشر بالتحميل.")


@bot.message_handler(func=lambda message: True)
def download_media(message):
    url = message.text
    if not url.startswith("http"):
        bot.reply_to(message, "الرجاء إرسال رابط صحيح يا كابتن.")
        return

    processing_msg = bot.reply_to(message, "جاري المعالجة والتحميل... ⏳")

    output_template = 'downloaded_video.%(ext)s'

    ydl_opts = {
        'outtmpl': output_template,
        'format': 'best',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        # إرسال الفيديو للمستخدم
        with open(filename, 'rb') as video:
            bot.send_video(message.chat.id, video, caption="تم التحميل بواسطة بوتك الخاص 🚀")

        # حذف الملف من الجهاز بعد الإرسال لتنظيف المساحة
        os.remove(filename)
        bot.delete_message(message.chat.id, processing_msg.message_id)

    except Exception as e:
        bot.edit_message_text(chat_id=message.chat.id, message_id=processing_msg.message_id,
                              text=f"عذراً يا كابتن، صار خطأ أثناء التحميل: {str(e)}")


# تشغيل البوت
print("البوت شغال الآن...")
bot.infinity_polling()
