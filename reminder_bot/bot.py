from pyrogram import Client, filters
from pyrogram.types import *
from pyromod import listen
import logging
from dbt import Database
from datetime import datetime, timedelta
import asyncio
from admin_panel import Panel_admin
from handlers import Support, Link, VIP, About_bot
from config import API_ID, API_HASH, BOT_TOKEN, ADMIN_ID

bot = Client(
    'reminder',
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

#Admin ={540350821,5610875596}
Admin = ADMIN_ID
user_states = {}

########## Panel Admin ##########
@bot.on_message(filters.private & filters.user(Admin))
async def admin_panel(client, message):
    await Panel_admin(client, message)

########## Start ##########
@bot.on_message(filters.command("start"))
async def Start(client, message):
    chat_id = message.chat.id
    users = message.chat.first_name
    mark = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton("یادآوری 📆"),
        ],
        [
            KeyboardButton("👈🏻 زیر مجموعه گیری 👉🏻"),
            KeyboardButton("VIP"),
            KeyboardButton("درباره ربات 🤖")
        ],
        [
            KeyboardButton("پشتیبانی 📞")
        ]
    ], resize_keyboard=True)
    await bot.send_message(chat_id, f"سلام {users} به ربات یاد آور خوش آمدید🌹", reply_markup=mark)

########## Reminder ##########
@bot.on_message(filters.regex("یادآوری 📆"))
async def Reminder(client, message):
    chat_id = message.chat.id
    await bot.send_message(
        chat_id,
        "🎉 *به بخش یادآوری خوش آمدید!* 🎉\n\n"
        "💡 اینجا می‌توانید *تسک‌ها و زمان‌های یادآوری* خود را تنظیم کنید.\n\n"
        "📋 *می‌خواهید یادآوری جدیدی اضافه کنید؟*\n"
        "👇 یکی از گزینه‌های زیر را انتخاب کنید:",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("➕ بله، اضافه کن! ✅", callback_data="add_task"),
                InlineKeyboardButton("❌ خیر، تمام شد.", callback_data="done")
            ]
        ]),
        
    )
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
@bot.on_callback_query(filters.regex("add_task"))
async def add_task(client, callback_query):
    chat_id = callback_query.message.chat.id
    await callback_query.message.delete()
    await bot.send_message(
        chat_id,
        "✍️ *لطفاً نام تسک خود را وارد کنید!*\n\n"
        "📖 *مثال:* `آب دادن به گلدان‌ها 🪴`",
        
    )
    user_states[chat_id] = "waiting_for_task"

########## handle ##########
@bot.on_message(filters.text & filters.create(lambda _, __, message: message.chat.id in user_states))
async def handle_task_text(client, message):
    chat_id = message.chat.id
    if chat_id not in user_states:
        return

    if user_states[chat_id] == "waiting_for_task":
        task_text = message.text
        user_states[chat_id] = {"task": task_text, "state": "waiting_for_time"}
        await bot.send_message(
            chat_id,
            "⏳ *لطفاً زمان یادآوری را وارد کنید!*\n\n"
            "📌 *فرمت‌های قابل قبول:*\n"
            "`HH:MM` ⏰ یا `HH:MM AM/PM` 🕰️\n\n"
            "📖 *مثال‌ها:*\n"
            "✅ `14:30` (24 ساعته)\n"
            "✅ `02:30 PM` (12 ساعته)\n\n"
            "🎯 *منتظریم که زمان را وارد کنید!*",
           
        )

    elif user_states[chat_id].get("state") == "waiting_for_time":
        remind_time_str = message.text
        task_text = user_states[chat_id].get("task")

        try:
            # تبدیل زمان وارد شده به datetime
            now = datetime.now()
            if "AM" in remind_time_str.upper() or "PM" in remind_time_str.upper():
                remind_time = datetime.strptime(remind_time_str.upper(), "%I:%M %p")
            else:
                remind_time = datetime.strptime(remind_time_str, "%H:%M")

            remind_time = now.replace(hour=remind_time.hour, minute=remind_time.minute, second=0, microsecond=0)
            if remind_time < now:
                remind_time += timedelta(days=1)

            # ذخیره تسک در دیتابیس
            dbt = Database()
            dbt.add_reminder(chat_id, task_text, remind_time)
            dbt.close()

            await bot.send_message(
                chat_id,
                f"✅ *یادآوری ثبت شد!*\n\n"
                f"📝 *یاداوری:* `{task_text}`\n"
                f"⏰ *زمان:* `{remind_time.strftime('%H:%M')}`\n\n"
                "📬 *پیام یادآوری به شما ارسال خواهد شد!*",
                
            )
        except ValueError:
            await bot.send_message(
                chat_id,
                "⚠️ *فرمت ورودی صحیح نمی‌باشد.*\n"
                "🔄 لطفاً دوباره زمان را وارد کنید!",
                
            )
        
        del user_states[chat_id]

########## Add task(No) ##########
@bot.on_callback_query(filters.regex("done"))
async def done(client, callback_query):
    chat_id = callback_query.message.chat.id
    await callback_query.message.edit_text(
        "🎉 *تمام شد!*\n\n"
        "📝 *یادآوری شما در حال تنظیم می‌باشند.*\n\n"
        "🕒 *زمان‌بندی‌های شما به‌زودی نمایش داده می‌شوند.*",
        
    )
    await display_tasks(chat_id)

########## check_reminders ##########
async def check_reminders():
    while True:
        dbt = Database()
        now = datetime.now()
        reminders = dbt.get_due_reminders()

        # چاپ برای بررسی و اشکال‌زدایی
        print(f"Checking reminders at {now.strftime('%Y-%m-%d %H:%M:%S')}")
        
        for reminder in reminders:
            id, chat_id, text, remind_time = reminder
            if remind_time <= now:  # اگر زمان یادآوری به گذشته رسیده باشد
                await bot.send_message(chat_id, f"یادآوری: {text}")
                dbt.delete_reminder(id)
        
        dbt.close()
        await asyncio.sleep(10)

########## Main ##########
@bot.on_message(filters.text & ~filters.command("start") & ~filters.regex("یادآوری 📆"))
async def Main(client, message):
    chat_id = message.chat.id
    text = message.text
    user_id = message.from_user.id
    
    dbt = Database()
    dbt.add_user(user_id)  # اضافه کردن کاربر به دیتابیس

    # بررسی بلاک بودن کاربر
    if dbt.check_block(user_id):
        await bot.send_message(chat_id, "🚫 شما از استفاده از این ربات مسدود شده‌اید.")
        return

    # دستورات دیگر
    if text == "/start":
        await Start(client, message)
    elif text[0:7] == "/start ":
        user_chat_friend = text.replace("/start ", "")
        dbt = Database()
        if dbt.update_user(user_id, user_chat_friend):
            await bot.send_message(user_chat_friend, "یک نفر با لینک شما به ربات دعوت شد")
        else:
            await bot.send_message(user_chat_friend, "قبلاً با لینک شما اد شده است")
        await Start(client, message)
    elif text == "یادآوری 📆" or text == "/reminder":
        await Reminder(client, message)
    elif text == "👈🏻 زیر مجموعه گیری 👉🏻" or text == "/link":
        await Link(client, message)
    elif text == "VIP" or text == "/vip":
        await VIP(client, message)
    elif text == "درباره ربات 🤖" or text == "/about":
        await About_bot(client, message)
    elif text == "پشتیبانی 📞" or text == "/support":
        await Support(client, message)

    dbt.close()

if __name__ == "__main__":
    bot.start()
    loop = asyncio.get_event_loop()
    loop.create_task(check_reminders())
    loop.run_forever()
