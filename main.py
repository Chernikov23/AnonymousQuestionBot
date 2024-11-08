from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
import os
import logging
from dotenv import load_dotenv
import asyncio 

load_dotenv()

bot_token = os.getenv('BOT_TOKEN')
dp = Dispatcher()
bot = Bot(token=bot_token, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Бот запущен и работает...")

admins = [1477027628, 1215724942]


@dp.message(CommandStart())
async def start_command(msg: Message):
    await msg.answer('Привет\! Я \- бот предложка постов в канале [MediaHUB](https://t.me/media_hubSPb)')


@dp.message(lambda message: message.text and not message.photo and not message.video)
async def handle_text_message(msg: Message):
    await forward_to_admins(msg, content_type="Текст")


@dp.message(lambda message: message.photo)
async def handle_photo(msg: Message):
    await forward_to_admins(msg, content_type="Фото", file_id=msg.photo[-1].file_id)


@dp.message(lambda message: message.video)
async def handle_video(msg: Message):
    await forward_to_admins(msg, content_type="Видео", file_id=msg.video.file_id)


@dp.message(lambda message: message.sticker)
async def handle_sticker(msg: Message):
    await forward_to_admins(msg, content_type="Стикер", file_id=msg.sticker.file_id)


@dp.message(lambda message: message.voice)
async def handle_voice(msg: Message):
    await forward_to_admins(msg, content_type="Голосовое сообщение", file_id=msg.voice.file_id)


@dp.message(lambda message: message.video_note)
async def handle_video_note(msg: Message):
    await forward_to_admins(msg, content_type="Видео-сообщение", file_id=msg.video_note.file_id)


async def forward_to_admins(msg: Message, content_type: str, file_id: str = None):
    name = msg.from_user.username or msg.from_user.first_name
    user_id = msg.from_user.id
    link = f"tg://user?id={user_id}"
    user_link = f"[{name}]({link})"
    caption_text = f"Новое сообщение от {user_link}:\n\nТип содержимого: {content_type}"
    
    if content_type == "Текст":
        caption_text += f"\n\n{msg.text}"
    elif msg.caption: 
        caption_text += f"\n\nПодпись: {msg.caption}"

    for admin_id in admins:
        if content_type == "Текст":
            await bot.send_message(chat_id=admin_id, text=caption_text, parse_mode=ParseMode.MARKDOWN_V2)
        elif content_type == "Фото":
            await bot.send_photo(chat_id=admin_id, photo=file_id, caption=caption_text, parse_mode=ParseMode.MARKDOWN_V2)
        elif content_type == "Видео":
            await bot.send_video(chat_id=admin_id, video=file_id, caption=caption_text, parse_mode=ParseMode.MARKDOWN_V2)
        elif content_type == "Стикер":
            await bot.send_sticker(chat_id=admin_id, sticker=file_id)
        elif content_type == "Голосовое сообщение":
            await bot.send_voice(chat_id=admin_id, voice=file_id, caption=caption_text)
        elif content_type == "Видео-сообщение":
            await bot.send_video_note(chat_id=admin_id, video_note=file_id)
    

    await msg.answer('Ваше сообщение отправлено на модерацию\.')

async def main() -> None:
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

