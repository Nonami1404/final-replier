from telethon import TelegramClient, events, Button
from datetime import datetime, timedelta
import asyncio
import os

# API данные
api_id = 25562025
api_hash = 'e7c42bb295143247bf297a54cae8bafc'
bot_token = '7420577894:AAEubMz89jYYFmtN4ppbJpT68v6AGpSy5BM'

# Создаём клиент
client = TelegramClient("bot", api_id, api_hash).start(bot_token=bot_token)

# Храним время последнего ответа
last_reply_times = {}

# Ответы на языках
messages = {
    "ru": "👋 Привет! Это автоответчик. Я скоро отвечу на твоё сообщение. Спасибо за ожидание!",
    "uz": "👋 Salom! Bu avtojavob. Men sizga tez orada javob beraman. Kutganingiz uchun rahmat!",
    "en": "👋 Hello! This is an auto-reply. I’ll get back to you soon. Thanks for waiting!"
}

# Обработка новых сообщений
@client.on(events.NewMessage(incoming=True))
async def handler(event):
    # Только личные чаты
    if event.is_group or event.is_channel:
        return

    print(f"💬 Получено сообщение от: {event.sender_id}")

    user_id = event.sender_id
    now = datetime.now()
    last_time = last_reply_times.get(user_id)

    # Отвечаем, если не отвечали больше часа
    if not last_time or now - last_time > timedelta(hours=1):
        await client.send_message(
            user_id,
            "👋 Выберите язык ответа:",
            buttons=[
                [Button.inline("🇷🇺 Русский", b"lang_ru")],
                [Button.inline("🇺🇿 O'zbek", b"lang_uz")],
                [Button.inline("🇬🇧 English", b"lang_en")]
            ]
        )
        last_reply_times[user_id] = now

# Обработка выбора языка
@client.on(events.CallbackQuery)
async def callback(event):
    lang = event.data.decode().split("_")[-1]
    if lang in messages:
        await client.send_message(event.sender_id, messages[lang])
        await event.answer("Отправлено ✅", alert=False)

print("✅ Бот запущен")
client.run_until_disconnected()
