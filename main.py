
import asyncio
import os
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "🚀 CABBAR MANAGER'a hoş geldin!\n\n"
        "Bot başarıyla çalışıyor.\n"
        "Komutlar için /yardim yaz."
    )


@dp.message(Command("yardim"))
async def yardim(message: Message):
    await message.answer(
        "🤖 CABBAR MANAGER\n\n"
        "GENEL KOMUTLAR\n"
        "/start - Botu başlat\n"
        "/yardim - Yardım menüsü\n"
        "/ping - Bot gecikmesi\n"
        "/istatistik - Grup istatistikleri\n\n"
        "YÖNETİM\n"
        "/ban - Kullanıcıyı yasakla\n"
        "/at - Kullanıcıyı gruptan çıkar\n"
        "/sustur - Kullanıcıyı sustur\n"
        "/uyari - Kullanıcıya uyarı ver\n"
        "/uyarilar - Uyarıları göster\n"
        "/temizle - Mesajı temizle\n\n"
        "DİĞER\n"
        "/logkur - Log sistemini ayarla\n"
        "/hosgeldin - Karşılama mesajı\n"
        "/duyuru - Duyuru gönder\n"
        "/seviye - Seviyeni göster\n"
        "/liderlik - Liderlik tablosu"
    )


@dp.message(Command("ping"))
async def ping(message: Message):
    await message.answer("🏓 CABBAR MANAGER aktif!")


async def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN bulunamadı!")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
