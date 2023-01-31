import os
import telebot
from pytube import YouTube
from config import *
from visualizator import *


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'{WELCOME} {message.from_user.first_name}\n{SEND_LINK}')

@bot.message_handler()
def send_video_user(message):
    if message.text[:23] in FULL_LINK_YOUTUBE or message.text[:16] in LINK_YOUTUBE:
        start_msg = bot.send_message(chat_id=message.chat.id, text=START_DOWNLOAD)
        yt = YouTube(url=message.text)
        video = yt.streams.filter(only_audio=True).first()
        video.download(output_path='music', filename=f'{yt.title}.mp3')

        send_audio_msg = bot.send_message(message.chat.id, SEND_AUDIO)
        audio = open(f'music/{yt.title}.mp3', 'rb')
        bot.send_audio(message.chat.id, audio, caption=f'<b>{yt.title}\n@Deyssey</b>', parse_mode='html')

        bot.delete_message(message.chat.id, message.message_id)
        bot.delete_message(chat_id=message.chat.id, message_id=start_msg.message_id)
        bot.delete_message(chat_id=message.chat.id, message_id=send_audio_msg.message_id)

        path = f'music/{yt.title}.mp3'
        os.remove(path=path)
    else:
        bot.send_message(chat_id=message.chat.id, text=SEND_LINK_PLEASE)

if __name__ == '__main__':
    print('[INFO]:Telegram Bot connection!')
    bot.polling(none_stop=True)
