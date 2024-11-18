from pyrogram import Client
from pyrogram.types import *

Admin = 540350821
# تابع مربوط به پشتیبانی
async def Support(client, message):
    chat_id = message.chat.id
    message_support = await client.ask(chat_id, "پیام خود را به ربات ارسال کنید")
    await client.send_message(chat_id, "پیام با موفقیت به مدیریت ارسال شد ")

    try:
        await client.send_message(Admin, f"شما یک پیام جدید دارید:\nآیدی عددی:{message_support.from_user.id}\n\n{message_support.text}")
    except Exception as ee:
        print(ee)

# تابع مربوط به زیر مجموعه گیری
async def Link(client, message):
    chat_id = message.chat.id
    user = message.chat.first_name
    await client.send_message(chat_id, f"""
   لینک از طرف {user}

    https://telegram.me/reminderme2024_bot?start={chat_id}
""")

# تابع مربوط به وی ای پی
async def VIP(client, message):
    chat_id = message.chat.id
    await client.send_message(chat_id, "پیام خود را وارد کنید ")

# تابع مربوط به درباره ربات
async def About_bot(client, message):
    chat_id = message.chat.id
    await client.send_message(chat_id, """
سلام به ربات یادآور خوش آمدید 😍
با این ربات راحت کارهای روزانتون رو مدیریت کنید ✅

بخش رایگان ربات🆓 :
1-استفاده محدود به مدت دوهفته

2-محدودیت استفاده در روز به تعداد 5 پیام 

3-با دعوت 3 نفر از دوستان خود به ربات میتوانید به مدت دوهفته از ربات به طور رابگان استفاده کنید 

4-نمایش تبلیغات 

💎بخش VIP ربات 💎:
1-استفاده نامحدود از ربات 

2-عدم محدودیت در روز

4-نیاز به دعوت ندارد 

5-عدم نمایش تبلیغات

""")

