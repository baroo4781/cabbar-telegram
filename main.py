
import asyncio
import os
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, ChatMemberUpdated
from dotenv import load_dotenv

from database import veritabani_kur, xp_ekle
from config import (
    BOT_NAME,
    BOT_VERSION,
    XP_PER_MESSAGE,
    XP_COOLDOWN,
    DEFAULT_WELCOME
)

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

if not TOKEN:
    raise RuntimeError("BOT_TOKEN Railway Variables bölümünde bulunamadı!")

bot = Bot(token=TOKEN)
dp = Dispatcher()

xp_son_mesaj = {}


@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        f"🚀 {BOT_NAME} v{BOT_VERSION}\n\n"
        "Bot başarıyla çalışıyor!\n"
        "Komutlar için /yardim yaz."
    )


@dp.message(Command("yardim"))
async def yardim(message: Message):
    await message.answer(
        "🤖 CABBAR MANAGER\n\n"
        "GENEL\n"
        "/start - Botu başlat\n"
        "/yardim - Yardım menüsü\n"
        "/ping - Bot durumu\n"
        "/istatistik - İstatistikler\n\n"
        "YÖNETİM\n"
        "/ban - Kullanıcıyı yasakla\n"
        "/at - Kullanıcıyı gruptan çıkar\n"
        "/sustur - Kullanıcıyı sustur\n"
        "/uyari - Uyarı ver\n"
        "/uyarilar - Uyarıları göster\n"
        "/temizle - Mesajları temizle\n\n"
        "SİSTEMLER\n"
        "/logkur - Log ayarla\n"
        "/hosgeldin - Karşılama ayarla\n"
        "/duyuru - Duyuru gönder\n"
        "/seviye - Seviyeni göster\n"
        "/liderlik - Liderlik tablosu"
    )


@dp.message(Command("ping"))
async def ping(message: Message):
    await message.answer("🏓 CABBAR MANAGER aktif!")


@dp.message(Command("istatistik"))
async def istatistik(message: Message):
    await message.answer(
        f"📊 {BOT_NAME}\n"
        f"Sürüm: {BOT_VERSION}\n"
        "Durum: Aktif"
    )


@dp.message(Command("seviye"))
async def seviye(message: Message):
    if not message.from_user or message.chat.type == "private":
        await message.answer("Bu komut gruplarda kullanılabilir.")
        return

    xp, level = await xp_ekle(
        message.chat.id,
        message.from_user.id,
        0
    )

    await message.answer(
        f"⭐ {message.from_user.full_name}\n"
        f"Seviye: {level}\n"
        f"XP: {xp}"
    )


@dp.message(F.text)
async def mesaj_sistemi(message: Message):
    if message.chat.type == "private" or not message.from_user:
        return

    user_id = message.from_user.id
    chat_id = message.chat.id
    anahtar = (chat_id, user_id)

    simdi = asyncio.get_running_loop().time()
    onceki = xp_son_mesaj.get(anahtar, 0)

    if simdi - onceki >= XP_COOLDOWN:
        xp_son_mesaj[anahtar] = simdi
        eski_xp, eski_seviye = await xp_ekle(
            chat_id,
            user_id,
            XP_PER_MESSAGE
        )

        if int((eski_xp / 100) ** 0.5) > eski_seviye:
            await message.answer(
                f"🎉 Tebrikler {message.from_user.full_name}!\n"
                f"Yeni seviyen: {int((eski_xp / 100) ** 0.5)}"
            )


async def main():
    await veritabani_kur()
    logging.info("%s başlatılıyor...", BOT_NAME)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
