import logging
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile, ReplyKeyboardMarkup, KeyboardButton
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import setup_application
from aiohttp import web
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_HOST = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}"
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.getenv("PORT", 8000))

# Logging
logging.basicConfig(level=logging.INFO)

# Create bot and dispatcher
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# === Asosiy menyu ===
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(KeyboardButton("📄 PDF fayl"))

@dp.message(F.text == "/start")
async def start_handler(message: Message):
    await message.answer(
        "🇰🇷 Assalomu alaykum!\nPDF faylni olish uchun quyidagi tugmani bosing:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="📄 PDF fayl")]
            ],
            resize_keyboard=True
        )
    )

@dp.message(F.text == "📄 PDF fayl")
async def send_pdf(message: Message):
    try:
        file = FSInputFile("files/jaemi_korean3_vocab.pdf")
        await message.answer_document(file, caption="📘 재미있는 한국어 3 어휘 PDF")
    except Exception as e:
        await message.answer(f"❌ Xatolik: {e}")

# === Webhook endpoint ===
async def on_startup(app):
    await bot.set_webhook(WEBHOOK_URL)
    logging.info(f"✅ Webhook o‘rnatildi: {WEBHOOK_URL}")

async def on_shutdown(app):
    logging.info("❌ Webhook o‘chirildi")

def create_app():
    app = web.Application()
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    app.router.add_post(WEBHOOK_PATH, dp.webhook_handler(bot))
    setup_application(app, dp, bot=bot)
    return app

if __name__ == "__main__":
    app = create_app()
    web.run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT)
