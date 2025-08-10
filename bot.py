import random
import logging
from typing import Dict, Any
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from config import API_ID, API_HASH, BOT_TOKEN, MONGO_URI, DB_NAME, COLLECTION_NAME, OWNER_LINK, CHANNEL_LINK

# --- Setup logging ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- MongoDB Connection ---
try:
    mongo_client = MongoClient(MONGO_URI)
    db = mongo_client[DB_NAME]
    scores_collection = db[COLLECTION_NAME]
    logger.info("MongoDB connected successfully.")
except PyMongoError as e:
    logger.error(f"MongoDB connection failed: {e}")
    scores_collection = None

# --- Movie & Emoji data ---
movies = [
    # (Emoji, Movie name)
    ("🐅🔔", "Puli"), ("🕷️🧑", "Spider-Man: No Way Home (Tamil Dub)"), ("🦁💪", "Singam"),
    # ... your full movie list here, truncated for brevity
]

emoji_meanings = {
    # Use exact keys matching your emoji in movies for correct lookup
    "🐅🔔": "🐅 (Tiger) + 🔔 (Bell): Represents 'Puli' — 'Puli' means tiger, bell here suggests alertness.",
    "🕷️🧑": "🕷️ (Spider) + 🧑 (Man): Refers to 'Spider-Man', the superhero with spider-like powers.",
    # ... your full emoji_meanings here, truncated for brevity
}

# --- Runtime data ---
active_questions: Dict[str, Dict[str, Any]] = {}
ended_games = set()

# --- Pyrogram bot instance ---
bot = Client("emoji_movie_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- Score functions ---
def get_score(user_id: int) -> int:
    if not scores_collection:
        return 0
    user = scores_collection.find_one({"user_id": user_id})
    return user.get("score", 0) if user else 0

def update_score(user_id: int, name: str) -> None:
    if not scores_collection:
        return
    try:
        scores_collection.update_one(
            {"user_id": user_id},
            {"$inc": {"score": 1}, "$set": {"name": name}},
            upsert=True
        )
    except PyMongoError as e:
        logger.error(f"Failed to update score for {user_id}: {e}")

# --- Commands ---

BOT_NAME = "˹🌙 ᴀᴢʜᴀɢɪʏᴀ ✘ ᴍᴏᴊɪ˼"
fancy_bot_name = f"{BOT_NAME}"

@bot.on_message(filters.command("start"))
async def start(_, message):
    start_buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🌸 Owner", url=OWNER_LINK),
                InlineKeyboardButton("📢 Updates", url=CHANNEL_LINK)
            ],
            [
                InlineKeyboardButton("💖 Help", callback_data="help_info")
            ]
        ]
    )
    mention_md = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
    start_text = (
        f"{fancy_bot_name}\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"💗 வணக்கம் {mention_md} 🌟💕\n"
        "🎬 **Tamil Emoji Movie Game**-க்கு உங்களை வரவேற்கிறோம்! 🥳✨\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "💡 குழுவில் **/emoji** என டைப் செய்து விளையாட துவங்குங்கள்!\n"
        "🏆 உங்கள் புள்ளிகளை பார்க்க: **/myscore**\n"
        "⏭ கேள்வியை தவிர்க்க: **/skip**\n"
        "🛑 விளையாட்டை நிறுத்த: **/end**\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "💡 கீழே உள்ள பட்டன்களை பயன்படுத்தவும் ⬇"
    )
    await message.reply(
        start_text,
        reply_markup=start_buttons,
        parse_mode=ParseMode.MARKDOWN
    )

@bot.on_callback_query(filters.regex(r"^help_info$"))
async def help_info(_, query: CallbackQuery):
    help_text = (
        "ℹ **விளையாடும் வழிமுறை:**\n\n"
        "1️⃣ குழுவில் `/emoji` type செய்யவும்.\n"
        "2️⃣ Bot ஒரு emoji clue & 4 தேர்வுகள் தரும்.\n"
        "3️⃣ சரியான பதிலை click செய்யவும்.\n"
        "4️⃣ முதலில் சரியான பதில் சொல்வவருக்கு புள்ளிகள் கிடைக்கும்.\n\n"
        "🏆 `/myscore` – உங்கள் புள்ளிகள் பார்க்க\n"
        "⏭ `/skip` – தற்போதைய கேள்வி தவிர்க்க\n"
        "🛑 `/end` – விளையாட்டு நிறுத்த\n"
        "📌 ஒவ்வொரு கேள்விக்கும் ஒரே முயற்சி மட்டுமே."
    )
    await query.answer()
    await query.message.reply(help_text)

@bot.on_message(filters.command("help"))
async def help_command(_, message):
    await message.reply(
        "👋 Welcome to Tamil Emoji Movie Game!\n\n"
        "Use these commands:\n"
        "/emoji - Start a new emoji question\n"
        "/myscore - Show your current score\n"
        "/skip - Skip current question\n"
        "/end - End the game in this group\n"
        "Tap the buttons or use commands as shown."
    )

@bot.on_message(filters.command("myscore"))
async def my_score(_, message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    points = get_score(user_id)
    await message.reply(f"🏆 {name}, உங்கள் புள்ளிகள்: {points}")

@bot.on_message(filters.command("emoji") & filters.chat_type.groups)
async def send_emoji_question(_, message):
    chat_id = message.chat.id
    if chat_id in ended_games:
        await message.reply("🛑 விளையாட்டு நிறுத்தப்பட்டுள்ளது. மீண்டும் தொடங்க முடியாது.")
        return

    movie = random.choice(movies)
    correct = movie[1]
    emoji_clue = movie[0]

    # Find wrong choices with same first letter if possible
    same_first_letter_movies = [m[1] for m in movies if m[1] != correct and m[1][0].lower() == correct[0].lower()]
    if len(same_first_letter_movies) < 3:
        wrong_choices = random.sample([m[1] for m in movies if m[1] != correct], 3)
    else:
        wrong_choices = random.sample(same_first_letter_movies, 3)

    options = wrong_choices + [correct]
    random.shuffle(options)
    correct_index = options.index(correct)

    qid = str(random.randint(100000, 999999))
    active_questions[qid] = {
        "options": options,
        "correct_index": correct_index,
        "answered": set(),
        "closed": False,
        "chat_id": chat_id,
        "emoji_clue": emoji_clue,
        "correct_answer": correct
    }

    buttons = [
        [InlineKeyboardButton(opt, callback_data=f"ans|{qid}|{i}")]
        for i, opt in enumerate(options)
    ]

    sent = await message.reply(
        f"🔍 இந்த Emoji எந்த தமிழ் படம்?\n\n{emoji_clue}",
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    active_questions[qid]["msg_id"] = sent.message_id

@bot.on_message(filters.command("skip") & filters.chat_type.groups)
async def skip_question(_, message):
    chat_id = message.chat.id
    found = False
    for qid, qdata in list(active_questions.items()):
        if qdata.get("chat_id") == chat_id:
            correct_text = qdata["options"][qdata["correct_index"]]
            emoji_clue = qdata.get("emoji_clue", "")
            explanation = emoji_meanings.get(emoji_clue, "மன்னிக்கவும், இந்த Emoji விளக்கம் கிடைக்கவில்லை.")
            await message.reply(
                f"⏭ கேள்வி தவிர்க்கப்பட்டது!\n"
                f"சரியான பதில்: {correct_text}\n\n"
                f"📖 விளக்கம்:\n{explanation}"
            )
            active_questions.pop(qid, None)
            found = True
            break
    if not found:
        await message.reply("⏭ தற்போது எதுவும் கேள்வி இல்லை.")

@bot.on_message(filters.command("end") & filters.chat_type.groups)
async def end_game(_, message):
    chat_id = message.chat.id
    if chat_id in ended_games:
        await message.reply("🛑 விளையாட்டு ஏற்கனவே நிறுத்தப்பட்டுள்ளது.")
        return
    ended_games.add(chat_id)
    # Remove all active questions for this chat
    to_remove = [qid for qid, qdata in active_questions.items() if qdata.get("chat_id") == chat_id]
    for qid in to_remove:
        active_questions.pop(qid, None)
    await message.reply("🛑 விளையாட்டு நிறுத்தப்பட்டது!")

@bot.on_callback_query(filters.regex(r"^ans\|"))
async def check_answer(_, query: CallbackQuery):
    try:
        _, qid, idx_str = query.data.split("|")
        idx = int(idx_str)
    except Exception as e:
        logger.error(f"Callback parse error: {e}")
        await query.answer("Invalid data.", show_alert=True)
        return

    qdata = active_questions.get(qid)
    user_id = query.from_user.id
    user_name = query.from_user.first_name

    if not qdata:
        await query.answer("இந்த கேள்வி காலாவதியாகிவிட்டது.", show_alert=True)
        return

    if qdata.get("closed", False):
        await query.answer("இந்த கேள்விக்கு பதில் சொல்லப்பட்டுவிட்டது.", show_alert=True)
        return

    if user_id in qdata.get("answered", set()):
        await query.answer("நீங்கள் ஏற்கனவே பதில் சொன்னீர்கள்.", show_alert=True)
        return

    qdata["answered"].add(user_id)

    if idx == qdata["correct_index"]:
        update_score(user_id, user_name)
        points = get_score(user_id)
        await query.answer(f"✅ சரி! {user_name}க்கு {points} புள்ளிகள்", show_alert=True)
        correct_text = qdata["options"][qdata["correct_index"]]
        explanation = emoji_meanings.get(qdata.get("emoji_clue", ""), "விளக்கம் கிடைக்கவில்லை.")
        try:
            await query.message.edit_text(
                f"🏆 {user_name} சரியாக கண்டுபிடித்தார்!\n"
                f"சரியான பதில்: {correct_text}\n\n"
                f"📖 விளக்கம்:\n{explanation}"
            )
        except Exception as e:
            logger.error(f"Failed to edit message: {e}")

        qdata["closed"] = True
        active_questions.pop(qid, None)
    else:
        await query.answer("❌ தவறு!", show_alert=True)

# Optional admin restart command to clear ended games
@bot.on_message(filters.command("restart") & filters.user(OWNER_LINK.split("tg://user?id=")[-1]))
async def restart_game(_, message):
    ended_games.clear()
    active_questions.clear()
    await message.reply("♻️ விளையாட்டு மீண்டும் துவங்கியது!")

# --- Run bot ---
if __name__ == "__main__":
    logger.info("Bot started...")
    bot.run()
