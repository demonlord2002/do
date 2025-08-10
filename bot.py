import random
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient

# ==== BOT CONFIG ====
API_ID = 12345  # your api_id
API_HASH = "your_api_hash"
BOT_TOKEN = "your_bot_token"

# ==== MONGODB CONFIG ====
MONGO_URI = "mongodb+srv://username:password@cluster0.mongodb.net/?retryWrites=true&w=majority"
DB_NAME = "emoji_game"
COLLECTION_NAME = "scores"

# Connect to MongoDB
mongo_client = MongoClient(MONGO_URI)
db = mongo_client[DB_NAME]
scores_collection = db[COLLECTION_NAME]

# ==== MOVIE DATA ====
movies = [
    ("🐍🔔", "Puli"), ("🕷️👨", "Spider-Man: No Way Home (Tamil Dub)"), ("🐯💪", "Singam"),
    ("👑🏰", "Ponniyin Selvan"), ("🚀🌕", "Tik Tik Tik"), ("🌊🐠", "Meen Kuzhambum Mann Paanaiyum"),
    ("🏹🔥", "Baahubali"), ("👻🏠", "Kanchana"), ("🛕🦅", "Thirupaachi"), ("👩‍🍳🍲", "Saivam"),
    ("🐅🎯", "Kumki"), ("👨‍⚕️💊", "Mersal"), ("💣🕵️", "Vivegam"), ("🎭🎤", "Kaadhalan"),
    ("👨‍🚒🔥", "Theri"), ("🪂🎯", "Maanaadu"), ("🛶🏝️", "Kaadhalum Kadanthu Pogum"),
    ("🎸🎤", "Rockstar (Tamil Dub)"), ("🚔🔫", "Kaakha Kaakha"), ("💃🕺", "Ok Kanmani"),
    ("🪖🔫", "Theeran Adhigaaram Ondru"), ("🦸‍♂️⚡", "Minnal Murali (Tamil Dub)"),
    ("🐆🔫", "Kaala"), ("🏍️💨", "Irumbu Thirai"), ("🎩🎩", "Gentleman"), ("🕰️🔄", "24"),
    ("🌋🔥", "Sivaji"), ("👩‍👦❤️", "Pasanga"), ("👨‍🌾🌾", "Kadaikutty Singam"),
    ("👊🩸", "Asuran"), ("🎯🎯", "Thuppakki"), ("🚖🛣️", "Anegan"), ("🛶🐟", "Paruthiveeran"),
    ("🧟‍♂️🏃", "Miruthan"), ("🔪👩", "Psycho"), ("💼🏢", "Mankatha"), ("🕵️‍♂️🔍", "Detective"),
    ("👩‍❤️‍👨💔", "96"), ("💃💔", "Mayakkam Enna"), ("🏏🏆", "Chennai 600028"),
    ("🐒🎭", "Ko"), ("📚🎓", "Nanban"), ("🚚💨", "Vettai"), ("🪂🌪️", "Soorarai Pottru"),
    ("👩‍👩‍👦", "Thanga Meengal"), ("🕯️🌌", "Engeyum Eppodhum"), ("🎨👩", "Raja Rani"),
    ("🚀🪐", "Indru Netru Naalai"), ("🐍🩸", "Naan Avanillai"), ("🚤🏖️", "Billa"),
    ("🏞️🐘", "Aaranya Kaandam"), ("🛕🙏", "Kovil"), ("👮🔫", "Saamy"), ("💔🎼", "Vinnaithaandi Varuvaayaa"),
    ("🚂🏞️", "Pariyerum Perumal"), ("🎤🎧", "Sarvam Thaala Mayam"), ("🐎🏹", "Kaavalan"),
    ("👩‍🏫📚", "Kandukondain Kandukondain"), ("🍫🍭", "Chocklet"), ("🩸🏛️", "Raatchasan"),
    ("🏖️🌴", "Sura"), ("🐷🎯", "Oru Oorla Rendu Raja"), ("🎤🎸", "Petta"), ("🛣️🚙", "Kadhalar Dhinam"),
    ("🏛️⚖️", "Jai Bhim"), ("🏥🩺", "Doctor"), ("🌌🚀", "Enthiran"), ("🪖🇮🇳", "Indian"),
    ("🧑‍🚀🪐", "Manithan"), ("🎭🕴️", "Aalavandhan"), ("🌊🚤", "Anniyan"), ("💼🧠", "Ratsasan"),
    ("🧙‍♂️🔮", "Magadheera (Tamil Dub)"), ("🚘🛣️", "Saivam"), ("🦁👑", "The Lion King (Tamil Dub)"),
    ("🦜🌴", "Kaakha Kaakha 2"), ("🐦🎤", "Papanasam"), ("🚢🌊", "Kadhalan 2"), ("🐍💀", "Neelam"),
    ("🏹🗡️", "Vikram"), ("🚓🚨", "Beast"), ("🪆🎯", "Master"), ("🎤🎧", "Bigil"),
    ("👓💼", "Don"), ("🕶️🔫", "Thunivu"), ("🌅🛕", "Varisu"), ("🏏🎯", "Kanaa")
]

# ==== runtime question tracking ====
active_questions = {}

# ==== BOT INSTANCE ====
bot = Client("emoji_movie_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ==== MONGODB FUNCTIONS ====
def get_score(user_id: int) -> int:
    user = scores_collection.find_one({"user_id": user_id})
    return user["score"] if user and "score" in user else 0

def update_score(user_id: int, name: str):
    scores_collection.update_one(
        {"user_id": user_id},
        {"$inc": {"score": 1}, "$set": {"name": name}},
        upsert=True
    )

# ==== COMMANDS ====
@bot.on_message(filters.command("start"))
async def start(_, message):
    OWNER_LINK = "https://t.me/YourUsername"
    CHANNEL_LINK = "https://t.me/YourChannel"

    start_buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("👑 Owner", url=OWNER_LINK)],
            [InlineKeyboardButton("📢 Update", url=CHANNEL_LINK)],
            [InlineKeyboardButton("ℹ Help", callback_data="help_info")]
        ]
    )

    await message.reply(
        "🎬 வணக்கம்! 'Guess the Emoji - Tamil Movie Game' க்கு வரவேற்கிறோம்!\n\n"
        "குழுவில் /emoji டைப் செய்து விளையாடுங்கள்!\n\n"
        "🏆 உங்கள் புள்ளிகளை பார்க்க: /myscore\n\n"
        "கீழே உள்ள பட்டன்களை பயன்படுத்தவும் ⬇",
        reply_markup=start_buttons
    )

@bot.on_callback_query(filters.regex(r"^help_info$"))
async def help_info(_, query):
    help_text = (
        "ℹ **விளையாடும் வழிமுறை:**\n\n"
        "1️⃣ குழுவில் `/emoji` type செய்யவும்.\n"
        "2️⃣ Bot ஒரு emoji clue & 4 தேர்வுகள் தரும்.\n"
        "3️⃣ சரியான பதிலை click செய்யவும்.\n"
        "4️⃣ முதலில் சரியான பதில் சொல்வவருக்கு புள்ளிகள் கிடைக்கும்.\n\n"
        "🏆 `/myscore` – உங்கள் புள்ளிகள் பார்க்க\n"
        "📌 ஒவ்வொரு கேள்விக்கும் ஒரே முயற்சி மட்டுமே அனுமதி.\n"
        "🎯 சுறுசுறுப்பாக பதிலளிக்கவும்!"
    )
    await query.answer()
    await query.message.reply(help_text)

@bot.on_message(filters.command("myscore"))
async def my_score(_, message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    points = get_score(user_id)
    await message.reply(f"🏆 {name}, உங்கள் புள்ளிகள்: {points}")

@bot.on_message(filters.command("emoji") & filters.group)
async def send_emoji_question(_, message):
    movie = random.choice(movies)
    correct = movie[1]
    wrong_choices = random.sample([m[1] for m in movies if m[1] != correct], 3)
    options = wrong_choices + [correct]
    random.shuffle(options)
    correct_index = options.index(correct)

    qid = str(random.randint(100000, 999999))
    active_questions[qid] = {
        "options": options,
        "correct_index": correct_index,
        "answered": set(),
        "closed": False
    }

    buttons = [
        [InlineKeyboardButton(opt, callback_data=f"ans|{qid}|{i}")]
        for i, opt in enumerate(options)
    ]

    sent = await message.reply(
        f"🔍 இந்த Emoji எந்த தமிழ் படம்?\n\n{movie[0]}",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

    active_questions[qid]["msg_id"] = sent.message_id
    active_questions[qid]["chat_id"] = sent.chat.id

@bot.on_callback_query(filters.regex(r"^ans\|"))
async def check_answer(_, query):
    try:
        _, qid, idx_str = query.data.split("|")
        idx = int(idx_str)
    except Exception:
        await query.answer("Invalid data.", show_alert=True)
        return

    qdata = active_questions.get(qid)
    user_id = query.from_user.id
    user_name = query.from_user.first_name

    if not qdata:
        await query.answer("This question expired or bot restarted. Use /emoji to start a new one.", show_alert=True)
        return

    if qdata.get("closed", False):
        await query.answer("This question has already been answered.", show_alert=True)
        active_questions.pop(qid, None)
        return

    if user_id in qdata["answered"]:
        await query.answer("நீங்கள் ஏற்கனவே பதில் சொன்னீர்கள் — மறுபடியும் முயற்சி செய்ய முடியாது.", show_alert=True)
        return

    qdata["answered"].add(user_id)

    if idx == qdata["correct_index"]:
        update_score(user_id, user_name)
        points = get_score(user_id)
        await query.answer(f"✅ சரி! {user_name}க்கு {points} புள்ளிகள்", show_alert=True)
        correct_text = qdata["options"][qdata["correct_index"]]
        await query.message.edit_text(f"🏆 {user_name} சரியாக கண்டுபிடித்தார்!\nசரியான பதில்: {correct_text}")
        qdata["closed"] = True
        active_questions.pop(qid, None)
    else:
        await query.answer("❌ தவறு! நன்றி - மீண்டும் முயற்சி செய்ய முடியாது.", show_alert=True)

bot.run()
