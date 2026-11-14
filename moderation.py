
from datetime import timedelta

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ChatPermissions
from aiogram.exceptions import TelegramBadRequest

from database import uyari_ekle, uyari_sayisi
from config import MAX_WARNINGS

router = Router()


async def hedef_kullanici(message: Message):
    if message.reply_to_message and message.reply_to_message.from_user:
        return message.reply_to_message.from_user

    return None


async def admin_mi(message: Message):
    if not message.from_user:
        return False

    member = await message.bot.get_chat_member(
        message.chat.id,
        message.from_user.id
    )

    return member.status in ("administrator", "creator")


@router.message(Command("ban"))
async def ban(message: Message):
    if message.chat.type == "private":
        return

    if not await admin_mi(message):
        await message.answer("⛔ Bu komut sadece yöneticiler içindir.")
        return

    hedef = await hedef_kullanici(message)

    if not hedef:
        await message.answer("Kullanıcıya yanıt vererek /ban yaz.")
        return

    try:
        await message.bot.ban_chat_member(
            message.chat.id,
            hedef.id
        )
        await message.answer(f"🔨 {hedef.full_name} gruptan yasaklandı.")
    except TelegramBadRequest:
        await message.answer("Bu kullanıcı yasaklanamadı. Bot izinlerini kontrol et.")


@router.message(Command("at"))
async def at(message: Message):
    if message.chat.type == "private":
        return

    if not await admin_mi(message):
        await message.answer("⛔ Bu komut sadece yöneticiler içindir.")
        return

    hedef = await hedef_kullanici(message)

    if not hedef:
        await message.answer("Kullanıcıya yanıt vererek /at yaz.")
        return

    try:
        await message.bot.ban_chat_member(
            message.chat.id,
            hedef.id
        )
        await message.bot.unban_chat_member(
            message.chat.id,
            hedef.id
        )
        await message.answer(f"👢 {hedef.full_name} gruptan çıkarıldı.")
    except TelegramBadRequest:
        await message.answer("Kullanıcı gruptan çıkarılamadı.")


@router.message(Command("sustur"))
async def sustur(message: Message):
    if message.chat.type == "private":
        return

    if not await admin_mi(message):
        await message.answer("⛔ Bu komut sadece yöneticiler içindir.")
        return

    hedef = await hedef_kullanici(message)

    if not hedef:
        await message.answer("Kullanıcıya yanıt vererek /sustur yaz.")
        return

    try:
        await message.bot.restrict_chat_member(
            message.chat.id,
            hedef.id,
            ChatPermissions(can_send_messages=False),
            until_date=timedelta(hours=1)
        )
        await message.answer(f"🔇 {hedef.full_name} 1 saat susturuldu.")
    except TelegramBadRequest:
        await message.answer("Kullanıcı susturulamadı.")


@router.message(Command("uyari"))
async def uyari(message: Message):
    if message.chat.type == "private":
        return

    if not await admin_mi(message):
        await message.answer("⛔ Bu komut sadece yöneticiler içindir.")
        return

    hedef = await hedef_kullanici(message)

    if not hedef:
        await message.answer("Kullanıcıya yanıt vererek /uyari yaz.")
        return

    sebep = message.text.partition(" ")[2].strip() or "Sebep belirtilmedi"

    await uyari_ekle(
        message.chat.id,
        hedef.id,
        sebep
    )

    sayi = await uyari_sayisi(
        message.chat.id,
        hedef.id
    )

    await message.answer(
        f"⚠️ {hedef.full_name} uyarıldı.\n"
        f"Uyarı sayısı: {sayi}/{MAX_WARNINGS}\n"
        f"Sebep: {sebep}"
    )


@router.message(Command("uyarilar"))
async def uyarilar(message: Message):
    if message.chat.type == "private":
        return

    hedef = await hedef_kullanici(message)

    if not hedef:
        hedef = message.from_user

    if not hedef:
        return

    sayi = await uyari_sayisi(
        message.chat.id,
        hedef.id
    )

    await message.answer(
        f"⚠️ {hedef.full_name} toplam {sayi} uyarıya sahip."
    )
