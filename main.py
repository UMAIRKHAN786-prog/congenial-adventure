from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import bot_utils
import config
from datetime import datetime

bot = Client("SHINxROAST", bot_token=config.BOT_TOKEN)

# ---------------- /start -----------------
@bot.on_message(filters.command("start"))
async def start(client, message):
    user = message.from_user.first_name
    intros = [
        f"✨ ᴏʏᴇ {user} 😏 aa gaya! Ready ho ek savage ride ke liye? {random.choice(bot_utils.fancy_symbols)}",
        f"🔥 Yo {user}! Bot aa gaya roast karne ke liye! {random.choice(bot_utils.fancy_symbols)}",
        f"🤣 {user}, bas tera wait khatam hua! Let's go! {random.choice(bot_utils.fancy_symbols)}"
    ]
    text = random.choice(intros)
    
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("TALK TO SHINCHAN 😎", callback_data="talk"),
         InlineKeyboardButton("GAMER 🎮", url="https://t.me/ENDLES_ERA")],
        [InlineKeyboardButton("FRIENDS 🧸", url="https://t.me/AQUA_REALM"),
         InlineKeyboardButton("GAMES 🎮", callback_data="games")]
    ])
    await message.reply_text(text, reply_markup=buttons)

# ----------- /talk & roast ----------
@bot.on_message(filters.private & filters.text)
async def savage_chat(client, message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    if bot_utils.has_credits(user_id):
        roast = bot_utils.generate_roast(message.text, user_name)
        bot_utils.deduct_credits(user_id)
        await message.reply_text(roast)
    else:
        await message.reply_text("😅 Oye, credits khatam ho gaye! /daily ya /pay try karo.")

# ----------- /daily ------------
@bot.on_message(filters.command("daily"))
async def daily(client, message):
    user_id = message.from_user.id
    # Daily credit logic using Supabase timestamp field
    user = bot_utils.supabase.table("users").select("*").eq("user_id", user_id).single().execute()
    now = datetime.utcnow()
    last_daily = user.data['last_daily'] if user.data and 'last_daily' in user.data else None
    if not last_daily or (now - last_daily).total_seconds() > 86400:
        bot_utils.supabase.table("users").update({"credits": user.data['credits']+1000, "last_daily": now}).eq("user_id", user_id).execute()
        await message.reply_text("🎁 Daily 1000 credits added!")
    else:
        await message.reply_text("⏳ Already claimed today, try after 24h.")

# ---------------- start bot ----------------
print("🔥 SHINxROAST Bot running...")
bot.run()
