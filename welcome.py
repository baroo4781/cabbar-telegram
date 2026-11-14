
from aiogram import Router
from aiogram.types import Message
from aiogram import F

from config import DEFAULT_WELCOME

router = Router()


@router.chat_member()
async def uye_degisti(event):
    eski = event.old_chat_member.status
    yeni = event.new_chat_member.status

    if eski in ("left", "kicked") and yeni in ("member", "administrator"):
        isim = event.new_chat_member.user.full_name

        mesaj = DEFAULT_WELCOME.format(isim=isim)

        await event.bot.send_message(
            event.chat.id,
            mesaj
        )

    elif eski in ("member", "administrator") and yeni in ("left", "kicked"):
        isim = event.old_chat_member.user.full_name

        await event.bot.send_message(
            event.chat.id,
            f"👋 {isim} gruptan ayrıldı."
        )


@router.message(F.new_chat_members)
async def yeni_uye(message: Message):
    for user in message.new_chat_members:
        await message.answer(
            DEFAULT_WELCOME.format(isim=user.full_name)
        )
