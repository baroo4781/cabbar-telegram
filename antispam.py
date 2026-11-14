
import time
from collections import defaultdict, deque

from aiogram import Router
from aiogram.types import Message
from aiogram import F

from moderation import admin_mi

router = Router()

mesajlar = defaultdict(deque)

MESAJ_LIMITI = 5
SURE = 8


@router.message(F.text)
async def anti_spam(message: Message):
    if message.chat.type == "private" or not message.from_user:
        return

    if await admin_mi(message):
        return

    anahtar = (message.chat.id, message.from_user.id)
    simdi = time.monotonic()

    kuyruk = mesajlar[anahtar]

    while kuyruk and simdi - kuyruk[0] > SURE:
        kuyruk.popleft()

    kuyruk.append(simdi)

    if len(kuyruk) > MESAJ_LIMITI:
        try:
            await message.delete()
            await message.answer(
                f"⚠️ {message.from_user.full_name}, lütfen spam yapma."
            )
        except Exception:
            pass

        kuyruk.clear()
