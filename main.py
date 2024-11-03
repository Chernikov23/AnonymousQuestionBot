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
bot = Bot(token=bot_token, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Бот запущен и работает...")


admins = [1477027628, 1215724942]

@dp.message(CommandStart())
async def start_command(msg: Message):
    await msg.answer('Йоу! Мы команда [MEDIA HUB](https://t.me/media_hubSPb).\nНапиши нам идеи постов, мемы или обратную связь.')

@dp.message()
async def handle_message(msg: Message):
    if msg.from_user.username:
        name = f"@{msg.from_user.username}"
    else:
        name = msg.from_user.first_name

    id = msg.from_user.id
    link = f"tg://user?id={id}"
    user_link = f"[{name}]({link})"
    message_text = f"Новое сообщение от {user_link}:\n\n{msg.text}"
    for admin_id in admins:
        await bot.send_message(chat_id=admin_id, text=message_text, parse_mode=ParseMode.MARKDOWN)
    await msg.answer('Если контент пройдёт модерацию, то ты увидишь его в канале MEDIA HUB!)


async def main() -> None:
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
