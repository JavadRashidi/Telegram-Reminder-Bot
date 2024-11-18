from pyrogram import Client, filters
from pyrogram.types import *
from pyromod import listen
import logging
from dbt import Database
from datetime import datetime, timedelta
import asyncio

class ReminderBot:
    def __init__(self, bot):
        self.bot = bot
        self.user_states = {}

    ########## Reminder ##########
    async def reminder(self, message):
        chat_id = message.chat.id
        await self.bot.send_message(chat_id, "خوش آمدید! میخواهید یادآوری جدید اضافه کنید؟", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("بله", callback_data="add_task"), InlineKeyboardButton("خیر", callback_data="done")]
        ]))

    ########## All task ##########
    async def display_tasks(self, chat_id):
        dbt = Database()
        tasks = dbt.get_reminders(chat_id)
        task_list = "\n".join([f"{task[0]} در ساعت {task[1].strftime('%H:%M')}" for task in tasks])
        if task_list:
            await self.bot.send_message(chat_id, f"تسک های وارد شده شما:\n{task_list}\n\nپیام یادآوری به شما ارسال می شود.")
        else:
            await self.bot.send_message(chat_id, "یادآوری تنظیم نشده است.")
        dbt.close()

    ########## Add task(Yes) ##########
    async def add_task(self, callback_query):
        chat_id = callback_query.message.chat.id
        await callback_query.message.delete()
        await self.bot.send_message(chat_id, "لطفا تسک خود را وارد کنید.\nمثال: آب دادن به گلدانها")
        self.user_states[chat_id] = "waiting_for_task"

    ########## handle_task_text ##########
    async def handle_task_text(self, message):
        chat_id = message.chat.id
        if chat_id not in self.user_states:
            return

        if self.user_states[chat_id] == "waiting_for_task":
            task_text = message.text
            self.user_states[chat_id] = {"task": task_text, "state": "waiting_for_time"}
            await self.bot.send_message(chat_id, "لطفا زمان یادآوری را با فرمت دقیقه:ساعت وارد کنید.\nمثال: 11:25")

        elif self.user_states[chat_id].get("state") == "waiting_for_time":
            remind_time_str = message.text
            task_text = self.user_states[chat_id].get("task")

            try:
                remind_time = datetime.strptime(remind_time_str, '%H:%M')
                now = datetime.now()
                remind_time = now.replace(hour=remind_time.hour, minute=remind_time.minute, second=0, microsecond=0)
                if remind_time < now:
                    remind_time += timedelta(days=1)

                dbt = Database()
                dbt.add_reminder(chat_id, task_text, remind_time)
                dbt.close()

                await self.bot.send_message(chat_id, f"یادآوری '{task_text}' برای ساعت {remind_time_str} تنظیم شد. پیام یادآوری به شما ارسال می‌شود.")
            except ValueError:
                await self.bot.send_message(chat_id, "فرمت ورودی صحیح نمی‌باشد. دوباره سعی کنید.")

            del self.user_states[chat_id]

    ########## Done (No) ##########
    async def done(self, callback_query):
        chat_id = callback_query.message.chat.id
        await callback_query.message.edit_text("تمام شد! تسک ها در حال تنظیم می باشند.")
        await self.display_tasks(chat_id)

    ########## check_reminders ##########
    async def check_reminders(self):
        while True:
            dbt = Database()
            now = datetime.now()
            reminders = dbt.get_due_reminders()
            for reminder in reminders:
                id, chat_id, text, remind_time = reminder
                await self.bot.send_message(chat_id, f"یادآوری: {text}")
                dbt.delete_reminder(id)
            dbt.close()
            await asyncio.sleep(10)
