# reminder_panel.py

from pyrogram import Client, filters
from pyrogram.types import *
from dbt import Database
from datetime import datetime, timedelta
user_states = {}

########## Reminder ##########
async def Reminder(client, message):
    chat_id = message.chat.id
    await bot.send_message(chat_id, "خوش آمدید! میخواهید یادآوری جدید اضافه کنید؟", reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("بله", callback_data="add_task"), InlineKeyboardButton("خیر", callback_data="done")]
    ]))
########## All task ##########
async def display_tasks(chat_id):
    dbt = Database()
    tasks = dbt.get_reminders(chat_id)
    task_list = "\n".join([f"{task[0]} در ساعت {task[1].strftime('%H:%M')}" for task in tasks])
    if task_list:
        await bot.send_message(chat_id, f"تسک های وارد شده شما:\n{task_list}\n\nپیام یادآوری به شما ارسال می شود.")
    else:
        await bot.send_message(chat_id, "یادآوری تنظیم نشده است.")
    dbt.close()

########## Add task(Yes) ##########
async def add_task(client, callback_query):
    chat_id = callback_query.message.chat.id
    await callback_query.message.delete()
    await bot.send_message(chat_id, "لطفا تسک خود را وارد کنید.\nمثال: آب دادن به گلدانها")
    user_states[chat_id] = "waiting_for_task"

########## Handle task text ##########
async def handle_task_text(client, message):
    chat_id = message.chat.id
    if chat_id not in user_states:
        return

    if user_states[chat_id] == "waiting_for_task":
        task_text = message.text
        user_states[chat_id] = {"task": task_text, "state": "waiting_for_time"}
        await bot.send_message(chat_id, "لطفا زمان یادآوری را با فرمت دقیقه:ساعت وارد کنید.\nمثال: 11:25")

    elif user_states[chat_id].get("state") == "waiting_for_time":
        remind_time_str = message.text
        task_text = user_states[chat_id].get("task")

        try:
            remind_time = datetime.strptime(remind_time_str, '%H:%M')
            now = datetime.now()
            remind_time = now.replace(hour=remind_time.hour, minute=remind_time.minute, second=0, microsecond=0)
            if remind_time < now:
                remind_time += timedelta(days=1)

            dbt = Database()
            dbt.add_reminder(chat_id, task_text, remind_time)
            dbt.close()

            await bot.send_message(chat_id, f"یادآوری '{task_text}' برای ساعت {remind_time_str} تنظیم شد. پیام یادآوری به شما ارسال می‌شود.")
        except ValueError:
            await bot.send_message(chat_id, "فرمت ورودی صحیح نمی‌باشد. دوباره سعی کنید.")
        
        del user_states[chat_id]

########## Add task(No) ##########
async def done(client, callback_query):
    chat_id = callback_query.message.chat.id
    await callback_query.message.edit_text("تمام شد! تسک ها در حال تنظیم می باشند.")
    await display_tasks(chat_id)
