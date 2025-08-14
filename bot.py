import asyncio
import json
import logging
import os

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import WebAppInfo, ReplyKeyboardMarkup
from dotenv import load_dotenv

from db import init_db, insert_event

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEB_APP_URL = os.getenv("WEB_APP_URL")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(
                text="📅 Открыть календарь",
                web_app=WebAppInfo(url=WEB_APP_URL)
            )]
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите действие"
    )
    await message.answer(
        "Здравствуйте! Нажмите кнопку, чтобы открыть календарь.",
        reply_markup=kb
    )

@dp.message(F.web_app_data)
async def process_webapp_data(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)
        title = data.get("title", "Событие")
        start_ts = data["start"]
        end_ts = data.get("end")
        await insert_event(
            user_id=message.from_user.id,
            title=title,
            start_ts=start_ts,
            end_ts=end_ts
        )
        await message.answer(f"Событие сохранено!\n{title} — {start_ts}")
    except Exception as e:
        await message.answer(f"Не удалось обработать событие: {e}")

async def main():
    logging.basicConfig(level=logging.INFO)
    await init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
