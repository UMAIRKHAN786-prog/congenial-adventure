from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from transformers import pipeline
import random, asyncio

# --------------------------
# Bot Token
# --------------------------
BOT_TOKEN = "YOUR_BOT_TOKEN"  # BotFather se copy kar

bot = Client("SHINxROAST", bot_token=BOT_TOKEN)

# --------------------------
# AI Model Setup
# --------------------------
generator = pipeline("text-generation", model="gpt2-medium")

# --------------------------
# Fancy symbols & fonts
# --------------------------
fancy_symbols = ["✨", "🔥", "💫", "🪄", "😎", "🎮", "🧸"]

def generate_roast(prompt, user):
    result = generator(
        f"Reply in savage, funny, shin-style roast to user {user}: {prompt}",
        max_length=50,
        do_sample=True,
        temperature=0.9
    )
    return result[0]['generated_text']

# --------------------------
# /start command
# --------------------------
@bot.on_message(filters.command("start"))
async def start(client, message):
    user = message.from_user.first_name
    intros = [
        f"✨ ᴏʏᴇ {user} 😏 aa gaya! Ready ho ek savage ride ke liye? {random.choice(fancy_symbols)}",
        f"🔥 Yo {user}! Bot aa gaya roast karne ke liye! {random.choice(fancy_symbols)}",
        f"🤣 {user}, bas tera wait khatam hua! Let's go! {random.choice(fancy_symbols)}"
    ]
    text = random.choice(intros)

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("TALK TO SHINCHAN 😎", callback_data="talk"),
         InlineKeyboardButton("GAMER 🎮", url="https://t.me/ENDLES_ERA")],
        [InlineKeyboardButton("FRIENDS 🧸", url="https://t.me/AQUA_REALM"),
         InlineKeyboardButton("GAMES 🎮", callback_data="games")]
    ])
    await message.reply_text(text, reply_markup=buttons)

# --------------------------
# Button callbacks
# --------------------------
@bot.on_callback_query()
async def button_callback(client, query):
    user = query.from_user.first_name
    if query.data == "talk":
        await query.message.reply_text(f"😏 {user}, bata kya bolna hai?")
    elif query.data == "games":
        games = ["Chess ♟️", "Ludo 🎲", "TicTacToe ❌⭕", "Guess Number 🔢", "Snake 🐍"]
        game_buttons = InlineKeyboardMarkup(
            [[InlineKeyboardButton(game, callback_data=f"game_{game}")] for game in games]
        )
        await query.message.reply_text("Select your game 😎:", reply_markup=game_buttons)
    elif query.data.startswith("game_"):
        game_name = query.data.replace("game_", "")
        await query.message.reply_text(f"You chose: {game_name} 🎮 Let's play!")

# --------------------------
# /own sticker feature
# --------------------------
@bot.on_message(filters.command("own") & filters.reply)
async def own_sticker(client, message):
    if message.reply_to_message.sticker:
        await message.reply_text("ᴘʀᴏᴄᴇssɪɴɢ... 🪄")
        await asyncio.sleep(2.5)
        await message.reply_text("Your sticker is ready ✅")
    else:
        await message.reply_text("Reply to a sticker with /own!")

# --------------------------
# /music command
# --------------------------
@bot.on_message(filters.command("music"))
async def music(client, message):
    user = message.from_user.first_name
    trending_songs = ["Blinding Lights ✨", "Levitating 💫", "Stay 🔥", "Bad Habits 😎", "As It Was 💥"]
    random.shuffle(trending_songs)
    music_text = f":) HOPE U LIKE THIS, {user} 🎵\n\n" + "\n".join(trending_songs)
    await message.reply_text(music_text)

# --------------------------
# TALK TO SHINCHAN savage reply
# --------------------------
@bot.on_message(filters.private & filters.text)
async def savage_chat(client, message):
    user = message.from_user.first_name
    user_text = message.text
    roast = generate_roast(user_text, user)
    await message.reply_text(roast)

# --------------------------
# Start Bot
# --------------------------
print("🔥 SHINxROAST Bot running...")
bot.run()
