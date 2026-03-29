import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message, BusinessMessagesDeleted, BusinessConnection
from aiogram.filters import Command

logging.basicConfig(level=logging.INFO)

TOKEN2 = os.getenv("TOKEN2")
ADMIN_ID = int("".join(filter(str.isdigit, os.getenv("ADMIN_ID", ""))))

bot = Bot(token=TOKEN2)
dp = Dispatcher()

cache = {}


def save_to_cache(message: Message):
    cid = message.chat.id
    if cid not in cache:
        cache[cid] = {}
    cache[cid][message.message_id] = message


async def forward_to_admin(msg: Message, prefix: str = ""):
    try:
        sender = ""
        if msg.from_user:
            sender = f"👤 {msg.from_user.full_name}"
            if msg.from_user.username:
                sender += f" (@{msg.from_user.username})"
            sender += f"\n🆔 {msg.from_user.id}"

        chat_info = ""
        if msg.chat:
            name = msg.chat.full_name or msg.chat.title or str(msg.chat.id)
            chat_info = f"💬 {name}"

        header = f"{prefix}\n{sender}\n{chat_info}".strip()
        await bot.send_message(ADMIN_ID, header)

        if msg.text:
            await bot.send_message(ADMIN_ID, f"✉️ {msg.text}")
        if msg.voice:
            await bot.send_voice(ADMIN_ID, msg.voice.file_id)
        if msg.video_note:
            await bot.send_video_note(ADMIN_ID, msg.video_note.file_id)
        if msg.photo:
            await bot.send_photo(ADMIN_ID, msg.photo[-1].file_id, caption=msg.caption)
        if msg.video:
            await bot.send_video(ADMIN_ID, msg.video.file_id, caption=msg.caption)
        if msg.audio:
            await bot.send_audio(ADMIN_ID, msg.audio.file_id, caption=msg.caption)
        if msg.document:
            await bot.send_document(ADMIN_ID, msg.document.file_id, caption=msg.caption)
        if msg.sticker:
            await bot.send_sticker(ADMIN_ID, msg.sticker.file_id)
        if msg.animation:
            await bot.send_animation(ADMIN_ID, msg.animation.file_id, caption=msg.caption)
    except Exception as e:
        logging.error(f"
