from config import TOKEN, LINK_YOUTUBE, FULL_LINK_YOUTUBE
from aiogram import *
from pytube import YouTube
from visualizator import *
import os


bot = Bot(TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_bot(message: types.Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id, text=f"{WELCOME} {message.from_user.first_name}!")
    await bot.send_message(chat_id, text=SEND_LINK)

@dp.message_handler(commands=["help"])
async def help_bot(message: types.Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id, text=HELP_BOT)


@dp.message_handler()
async def text_message(message: types.Message):
    chat_id = message.chat.id
    url = message.text

    if url[0:16] in FULL_LINK_YOUTUBE or url[0:16] in LINK_YOUTUBE:
        await bot.send_message(chat_id, text=START_DOWNLOAD)
        await downloads(url, message, bot)
        await bot.delete_message(chat_id, message_id=message.message_id)
    else:
        await bot.send_message(chat_id, text=SEND_LINK_PLEASE)
        await bot.delete_message(chat_id, message_id=message.message_id)

        
async def downloads(url, message, bot):
    yt = YouTube(url)
    stream = yt.streams.filter(progressive=True, file_extension='mp4')
    stream.get_highest_resolution().download(f'{message.chat.id}', f"{yt.title}")

    with open(f"{message.chat.id}/{yt.title}", 'rb') as video:
        await bot.send_audio(message.chat.id, video, caption='@Deyssey')
        os.remove(f"{message.chat.id}/{yt.title}")


if __name__ == '__main__':
    executor.start_polling(dp)