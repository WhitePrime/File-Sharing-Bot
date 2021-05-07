import asyncio
import base64
from pyrogram import Client, filters, __version__
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait

from bot import Bot
from config import CHANNEL_ID, ADMINS, START_MSG, OWNER_ID



@Bot.on_message(filters.command('start') & filters.private)
async def start_command(client: Client, message: Message):
    text = message.text
    if len(text)>7:
        try:
            base64_string = text.split(" ", 1)[1]
        except:
            return
        base64_bytes = base64_string.encode("ascii")
        string_bytes = base64.b64decode(base64_bytes) 
        string = string_bytes.decode("ascii") 
        argument = string.split("-")
        if len(argument) == 3:
            try:
                start = int(argument[1])
                end = int(argument[2])
            except:
                return
            if start <= end:
                ids = range(start,end+1)
            else:
                ids = []
                i = start
                while True:
                    ids.append(i)
                    i -= 1
                    if i < end:
                        break
        elif len(argument) == 2:
            try:
                ids = [int(argument[1])]
            except:
                return
        try:
            msgs = await client.get_messages(
                chat_id=CHANNEL_ID,
                message_ids=ids
            )
        except:
            await message.reply_text("Something went wrong..!")
            return
        for msg in msgs:
            try:
                await msg.copy(chat_id=message.from_user.id)
                await asyncio.sleep(0.5)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await msg.copy(chat_id=message.from_user.id)
            except:
                pass
        return
    else:
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("😊 Информация", callback_data = "about"),
                    InlineKeyboardButton("🔒 Закрыть", callback_data = "close")
                ]
            ]
        )
        await message.reply_text(
            text = START_MSG.format(firstname = message.chat.first_name),
            reply_markup = reply_markup,
            disable_web_page_preview = True,
            quote = True
        )
        return



@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    if data == "about":
        await query.message.edit_text(
            text = f"<b>○ Создатель : <a href='tg://user?id={OWNER_ID}'>White Prime</a>\n○ Канал №1 : @ITHard\n○ Канал №2 : @ITHardNews",
            disable_web_page_preview = True,
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🔒 Закрыть", callback_data = "close")
                    ]
                ]
            )
        )
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass


@Bot.on_message(filters.private & filters.user(ADMINS) & ~filters.command(['start','batch']))
async def channel_post(client: Client, message: Message):
    reply_text = await message.reply_text("Подождите...!", quote = True)
    try:
        post_message = await message.copy(chat_id = CHANNEL_ID, disable_notification=True)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        post_message = await message.copy(chat_id = CHANNEL_ID, disable_notification=True)
    except:
        await reply_text.edit_text("Что-то не так..!")
        return
    string = f"get-{post_message.message_id}"
    string_bytes = string.encode("ascii")
    base64_bytes = base64.b64encode(string_bytes)
    base64_string = base64_bytes.decode("ascii")
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Ссылка", url=f'https://telegram.me/share/url?url={link}')]])
    await reply_text.edit(f"<b>Ссылка на загрузку</b>\n\n{link}", reply_markup=reply_markup, disable_web_page_preview = True)


@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('batch'))
async def batch(client: Client, message: Message):
    while True:
        try:
            first_message = await client.ask(text = "Перешлите это сообщение в канал (или заметки)..", chat_id = message.from_user.id, filters=filters.forwarded, timeout=30)
        except:
            return
        if first_message.forward_from_chat:
            if first_message.forward_from_chat.id == CHANNEL_ID:
                f_msg_id = first_message.forward_from_message_id
                break
        await first_message.reply_text("Переадресация только с назначенного канала...", quote = True)
        continue
    while True:
        try:
            second_message = await client.ask(text = "Перешлите последнее сообщение из канала (или заметок)..", chat_id = message.from_user.id, filters=filters.forwarded, timeout=30)
        except:
            return
        if second_message.forward_from_chat:
            if second_message.forward_from_chat.id == CHANNEL_ID:
                s_msg_id = second_message.forward_from_message_id
                break
        await second_message.reply_text("Доступно только подписчикам...", quote = True)
        continue
    string = f"get-{f_msg_id}-{s_msg_id}"
    string_bytes = string.encode("ascii")
    base64_bytes = base64.b64encode(string_bytes)
    base64_string = base64_bytes.decode("ascii")
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Ссылка", url=f'https://telegram.me/share/url?url={link}')]])
    await second_message.reply_text(f"<b>Ссылка на скачивание</b>\n\n{link}", quote=True, reply_markup=reply_markup)
