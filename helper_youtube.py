import os
from aiogram import Bot, types
from logging import disable
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import config
from pytube import YouTube
import datetime
from datetime import timedelta


bot = Bot(token=config.TOKEN) #Ваш токен
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def cmd_answer(message: types.Message):
      await message.answer('<b>👋 Привіт, я YouTube Помічник.</b> \n <b>📥 Ви зможете завантажити відео з YouTube.</b> \n <b>🔗 Надішліть посилання на відео.</b>', parse_mode='HTML')
      
@dp.message_handler(commands=['help'])
async def cmd_answer(message: types.Message):
    await message.answer("⁉️<b> Якщо у вас є проблеми.</b> \n✉️ <b>Напишіть мені</b> <a href='https://t.me/nikit0ns'>@nikitons</a><b>.</b>", disable_web_page_preview=True, parse_mode="HTML")
      

@dp.message_handler()
async def cmd_answer(message: types.Message):   
      if message.text.startswith('https://youtube.be/') or message.text.startswith('https://www.youtube.com/') or message.text.startswith('https://youtu.be/'):
            url = message.text
            yt = YouTube(url)
            title = yt.title
            author = yt.author
            channel = yt.channel_url
            resolution = yt.streams.get_highest_resolution().resolution
            file_size = yt.streams.get_highest_resolution().filesize
            length = yt.length
            date_published = yt.publish_date.strftime("%Y-%m-%d")
            views = yt.views
            picture = yt.thumbnail_url
 
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text="Завантажити", callback_data="download"))
            await message.answer_photo(f'{picture}', caption=f"📹 <b>{title}</b> <a href='{url}'>→</a> \n" #Title#
                                 f"👤 <b>{author}</b> <a href='{channel}'>→</a> \n" #Author Of Channel# 
                                 f"⚙️ <b>Розширення —</b> <code>{resolution}</code> \n" ##
                                 f"🗂 <b>Відео важить —</b> <code>{round(file_size * 0.000001, 2)}MB</code> \n" #File Size#
                                 f"⏳ <b>Тривалість —</b> <code>{str(datetime.timedelta(seconds=length))}</code> \n" #Length#
                                 f"🗓 <b>Дата публікації —</b> <code>{date_published}</code> \n" #Date Published#
                                 f"👁 <b>Перегляди —</b> <code>{views:,}</code> \n", parse_mode='HTML', reply_markup=keyboard) #Views#
      else:
            await message.answer(f"❗️<b>Це не схоже на посилання!</b>", parse_mode='HTML')
            
            

@dp.callback_query_handler(text="download")
async def button_download(call: types.CallbackQuery):
      url = call.message.html_text
      yt = YouTube(url)
      title = yt.title
      author = yt.author
      resolution = yt.streams.get_highest_resolution().resolution
      stream = yt.streams.filter(progressive=True, file_extension="mp4")
      stream.get_highest_resolution().download(f'{call.message.chat.id}', f'{call.message.chat.id}_{yt.title}')
      with open(f"{call.message.chat.id}/{call.message.chat.id}_{yt.title}", 'rb') as video:
            await bot.send_video(call.message.chat.id, video, caption=f"📹 <b>{title}</b> \n" #Title#
                                    f"👤 <b>{author}</b> \n\n" #Author Of Channel#
                                    f"⚙️ <b>Розширення —</b> <code>{resolution}</code> \n"
                                    f"📥 <b>Завантажено за допомогою @Helper_YouTube_Bot</b>", parse_mode='HTML')
            os.remove(f"{call.message.chat.id}/{call.message.chat.id}_{yt.title}")



if __name__ == '__main__':
      executor.start_polling(dp)      
      