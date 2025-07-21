from telethon import TelegramClient, events
from datetime import datetime, timedelta
import asyncio

# 🔐 API-данные
api_id = 25562025
api_hash = 'e7c42bb295143247bf297a54cae8bafc'
bot_token = '7420577894:AAEubMz89jYYFmtN4ppbJpT68v6AGpSy5BM'

# 🚀 Инициализация клиента
client = TelegramClient("bot", api_id, api_hash).start(bot_token=bot_token)

# ⏱ Последнее время ответа
last_reply_times = {}

# 🧠 ID владельца бота (твой)
OWNER_ID = 1347186841  # Замени на свой user_id

# 📩 Текст автоответа
reply_text = (
    "👋 Йо! Если вы читаете это, значит я немного занят и не смог ответить сразу.\n"
    "Сейчас вам ответил мой 🤖 автоответчик. Спасибо за понимание!\n\n"
    "👋 Yo! Agar siz buni o‘qiyotgan bo‘lsangiz, demak men hozircha bandman va darhol javob bera olmadim.\n"
    "Sizga hozir 🤖 avtojavobchi javob berdi. Tushunganingiz uchun rahmat!\n\n"
    "👋 Yo! If you're reading this, it means I'm a bit busy and couldn’t reply right away.\n"
    "My 🤖 auto-reply bot answered you for now. Thanks for understanding!"
)

# 🔄 Обработка входящих сообщений
@client.on(events.NewMessage(incoming=True))
async def handler(event):
    # ❌ Пропускаем группы и каналы
    if event.is_group or event.is_channel:
        return

    user_id = event.sender_id

    # ❌ Не отвечаем себе
    if user_id == OWNER_ID:
        return

    # ❌ Не отвечаем, если ты онлайн
    me = await client.get_entity(OWNER_ID)
    status = me.status
    if hasattr(status, 'was_online'):
        # user is offline — отвечаем
        pass
    elif str(status) == "UserStatusOnline":
        return  # ❌ Ты онлайн — не отвечаем

    # ✅ Проверка времени последнего ответа
    now = datetime.now()
    last_time = last_reply_times.get(user_id)
    if not last_time or now - last_time > timedelta(hours=1):
        await client.send_message(user_id, reply_text)
        last_reply_times[user_id] = now

print("✅ Бот запущен")
client.run_until_disconnected()
