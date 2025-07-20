import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import FSInputFile, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.executor import start_webhook
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_HOST = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}"
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.getenv("PORT", 8000))

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# === Asosiy menyu ===
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(
    KeyboardButton("📄 PDF fayl")
)

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await message.answer(
        "🇰🇷 Assalomu alaykum!\nPDF faylni olish uchun quyidagi tugmani bosing:",
        reply_markup=main_menu
    )

# === PDF yuborish ===
@dp.message_handler(lambda message: message.text == "📄 PDF fayl")
async def send_pdf(message: types.Message):
    try:
        file = FSInputFile("files/jaemi_korean3_vocab.pdf")
        await message.answer_document(file, caption="📘 재미있는 한국어 3 어휘 PDF")
    except Exception as e:
        await message.reply(f"❌ Xatolik: {e}")

# === Webhook ===
async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    print("✅ Webhook o‘rnatildi:", WEBHOOK_URL)

async def on_shutdown(dp):
    print("❌ Webhook o‘chirildi")

if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
