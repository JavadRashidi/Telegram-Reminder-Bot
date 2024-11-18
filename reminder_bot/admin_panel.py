# admin_panel.py

from pyrogram import Client, filters
from pyrogram.types import *
from dbt import Database

# شناسه ادمین
Admin = 540350821
user_states = {}

# پنل ادمین
@Client.on_message(filters.private & filters.user(Admin))
async def Panel_admin(client, message):
    chat_id = message.chat.id
    text = message.text
    dbt = Database()
    mark2 = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton("تعداد کاربران")],
        [KeyboardButton("پیام همگانی"), KeyboardButton("پیام تکی")],
        [KeyboardButton("بلاک کردن"), KeyboardButton("آزاد کردن")]
    ], resize_keyboard=True)

    if text == "/start":
        await client.send_message(chat_id, "سلام ادمین عزیز", reply_markup=mark2)
    elif text == "تعداد کاربران":
        users = dbt.all_user()
        await message.reply(f"تعداد کاربران ربات {len(users)}")
    elif text == "پیام همگانی":
        update = await client.ask(chat_id, "پیام خود را ارسال کنید")
        users = dbt.all_user()
        succ = err = 0

        for pv in users:
            try:
                await client.send_message(pv, update.text)
                succ += 1
            except:
                err += 1

        await message.reply(f"""
تعداد کاربران ربات: {len(users)}
ارسال شده‌ها: {succ}
ارسال نشده‌ها: {err}""")
    elif text == "پیام تکی":
        user_id = await client.ask(chat_id, "آیدی شخص مورد نظر را وارد کنید")
        message_text = await client.ask(chat_id, "پیام خود را ارسال کنید ")
        try:
            await client.send_message(int(user_id.text), message_text.text)
            await message.reply("پیام با موفقیت ارسال شد")
        except Exception as e:
            await message.reply(f"پیام ارسال نشده: {e}\nمطمئن شوید کاربر از قبل ربات را استارت کرده است")
    elif text == "بلاک کردن":
        update_id = await client.ask(chat_id, "آیدی فرد مورد نظر را ارسال کنید")
        if dbt.add_block(update_id.text):
            await message.reply("کاربر با موفقیت بلاک شد")
            await client.send_message(update_id.text, "شما توسط ادمین بلاک شدید")
        else:
            await message.reply("کاربر بلاک نشد")
    elif text == "آزاد کردن":
        update_id = await client.ask(chat_id, "آیدی فرد مورد نظر را ارسال کنید")
        if dbt.remove_block(update_id.text):
            await message.reply("کاربر با موفقیت آزاد شد")
            await client.send_message(update_id.text, "شما توسط ادمین آنبلاک شدید")
        else:
            await message.reply("کاربر آزاد نشد")
