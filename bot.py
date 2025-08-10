import random
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient
from config import API_ID, API_HASH, BOT_TOKEN, MONGO_URI, DB_NAME, COLLECTION_NAME, OWNER_LINK, CHANNEL_LINK

# ==== MONGODB CONNECT ====
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

# ==== EMOJI MEANINGS ====
emoji_meanings = {
    "🐍🔔": "🐍 (Snake) + 🔔 (Bell): Represents 'Puli' which means Tiger; here snake and bell symbolize danger and alertness, hinting at the fierce nature of the movie.",
    "🕷️👨": "🕷️ (Spider) + 👨 (Man): Refers to 'Spider-Man', the superhero with spider-like powers.",
    "🐯💪": "🐯 (Tiger) + 💪 (Strong arm): Symbolizes 'Singam', meaning Lion, representing strength and bravery.",
    "👑🏰": "👑 (Crown) + 🏰 (Castle): Indicates royalty and kingdom, pointing to the historic epic 'Ponniyin Selvan'.",
    "🚀🌕": "🚀 (Rocket) + 🌕 (Moon): Refers to 'Tik Tik Tik', a space-themed thriller.",
    "🌊🐠": "🌊 (Water wave) + 🐠 (Fish): Related to 'Meen Kuzhambum Mann Paanaiyum', which is about fish and water elements.",
    "🏹🔥": "🏹 (Bow and arrow) + 🔥 (Fire): Symbolizes 'Baahubali', a warrior with bow and fire representing battle and power.",
    "👻🏠": "👻 (Ghost) + 🏠 (House): Represents the horror movie 'Kanchana' set in a haunted house.",
    "🛕🦅": "🛕 (Temple) + 🦅 (Eagle): Related to 'Thirupaachi', a movie with rural and temple backdrop and vigilance.",
    "👩‍🍳🍲": "👩‍🍳 (Chef) + 🍲 (Food): Refers to 'Saivam', which emphasizes family and food traditions.",
    "🐅🎯": "🐅 (Tiger) + 🎯 (Target): Symbolizes 'Kumki', a movie involving an elephant used to control wild animals (tiger representing wildlife).",
    "👨‍⚕️💊": "👨‍⚕️ (Doctor) + 💊 (Medicine): Points to 'Mersal', where the lead character is a doctor.",
    "💣🕵️": "💣 (Bomb) + 🕵️ (Detective): Refers to 'Vivegam', an action-thriller involving espionage and explosions.",
    "🎭🎤": "🎭 (Drama mask) + 🎤 (Microphone): Indicates 'Kaadhalan', a romantic and musical drama.",
    "👨‍🚒🔥": "👨‍🚒 (Firefighter) + 🔥 (Fire): Represents 'Theri', an action movie with fiery vengeance.",
    "🪂🎯": "🪂 (Parachute) + 🎯 (Target): Refers to 'Maanaadu', a political thriller involving tactical operations.",
    "🛶🏝️": "🛶 (Boat) + 🏝️ (Island): Points to 'Kaadhalum Kadanthu Pogum', a romantic movie with travel themes.",
    "🎸🎤": "🎸 (Guitar) + 🎤 (Microphone): Refers to 'Rockstar', a musical drama.",
    "🚔🔫": "🚔 (Police car) + 🔫 (Gun): Symbolizes 'Kaakha Kaakha', a cop action thriller.",
    "💃🕺": "💃 (Dancer) + 🕺 (Dancer): Represents 'Ok Kanmani', a romantic dance-filled movie.",
    "🪖🔫": "🪖 (Military helmet) + 🔫 (Gun): Points to 'Theeran Adhigaaram Ondru', a police action movie.",
    "🦸‍♂️⚡": "🦸‍♂️ (Superhero) + ⚡ (Lightning): Represents 'Minnal Murali', a superhero film.",
    "🐆🔫": "🐆 (Leopard) + 🔫 (Gun): Refers to 'Kaala', a gangster movie symbolized by the fierce leopard.",
    "🏍️💨": "🏍️ (Motorcycle) + 💨 (Speed): Points to 'Irumbu Thirai', a fast-paced action thriller.",
    "🎩🎩": "🎩 (Top hats): Symbolizes 'Gentleman', representing a classy hero.",
    "🕰️🔄": "🕰️ (Clock) + 🔄 (Repeat): Represents '24', a thriller revolving around time.",
    "🌋🔥": "🌋 (Volcano) + 🔥 (Fire): Symbolizes 'Sivaji', a fiery and explosive drama.",
    "👩‍👦❤️": "👩‍👦 (Mother and child) + ❤️ (Love): Points to 'Pasanga', a family drama focusing on children.",
    "👨‍🌾🌾": "👨‍🌾 (Farmer) + 🌾 (Crop): Represents 'Kadaikutty Singam', a rural farmer-based story.",
    "👊🩸": "👊 (Fist) + 🩸 (Blood): Symbolizes 'Asuran', a violent revenge drama.",
    "🎯🎯": "🎯 (Targets): Refers to 'Thuppakki', a thriller involving precision attacks.",
    "🚖🛣️": "🚖 (Taxi) + 🛣️ (Road): Points to 'Anegan', a romantic movie involving journeys.",
    "🛶🐟": "🛶 (Boat) + 🐟 (Fish): Represents 'Paruthiveeran', a rural action-drama.",
    "🧟‍♂️🏃": "🧟‍♂️ (Zombie) + 🏃 (Running): Refers to 'Miruthan', a zombie apocalypse movie.",
    "🔪👩": "🔪 (Knife) + 👩 (Woman): Points to 'Psycho', a thriller with a female lead and murder mystery.",
    "💼🏢": "💼 (Briefcase) + 🏢 (Office): Refers to 'Mankatha', a heist thriller.",
    "🕵️‍♂️🔍": "🕵️‍♂️ (Detective) + 🔍 (Magnifying glass): Symbolizes 'Detective', a mystery thriller.",
    "👩‍❤️‍👨💔": "👩‍❤️‍👨 (Couple) + 💔 (Broken heart): Points to '96', a romantic drama about lost love.",
    "💃💔": "💃 (Dancer) + 💔 (Broken heart): Refers to 'Mayakkam Enna', a love story with emotional turmoil.",
    "🏏🏆": "🏏 (Cricket) + 🏆 (Trophy): Symbolizes 'Chennai 600028', a sports drama.",
    "🐒🎭": "🐒 (Monkey) + 🎭 (Drama mask): Refers to 'Ko', a political thriller with twists.",
    "📚🎓": "📚 (Books) + 🎓 (Graduation cap): Points to 'Nanban', a story about friendship and education.",
    "🚚💨": "🚚 (Truck) + 💨 (Speed): Represents 'Vettai', an action thriller.",
    "🪂🌪️": "🪂 (Parachute) + 🌪️ (Tornado): Refers to 'Soorarai Pottru', about courage and stormy challenges.",
    "👩‍👩‍👦": "👩‍👩‍👦 (Family): Represents 'Thanga Meengal', a family emotional drama.",
    "🕯️🌌": "🕯️ (Candle) + 🌌 (Night sky): Symbolizes 'Engeyum Eppodhum', a romantic drama.",
    "🎨👩": "🎨 (Paint palette) + 👩 (Woman): Refers to 'Raja Rani', a love story with artistic elements.",
    "🚀🪐": "🚀 (Rocket) + 🪐 (Planet): Points to 'Indru Netru Naalai', a sci-fi time travel movie.",
    "🐍🩸": "🐍 (Snake) + 🩸 (Blood): Refers to 'Naan Avanillai', a thriller with betrayal and danger.",
    "🚤🏖️": "🚤 (Speedboat) + 🏖️ (Beach): Symbolizes 'Billa', an action thriller with style.",
    "🏞️🐘": "🏞️ (Landscape) + 🐘 (Elephant): Points to 'Aaranya Kaandam', a gangster movie set in urban wilds.",
    "🛕🙏": "🛕 (Temple) + 🙏 (Prayer): Represents 'Kovil', a devotional drama.",
    "👮🔫": "👮 (Police) + 🔫 (Gun): Refers to 'Saamy', a police action movie.",
    "💔🎼": "💔 (Broken heart) + 🎼 (Music): Symbolizes 'Vinnaithaandi Varuvaayaa', a romantic musical.",
    "🚂🏞️": "🚂 (Train) + 🏞️ (Scenery): Points to 'Pariyerum Perumal', a social drama.",
    "🎤🎧": "🎤 (Mic) + 🎧 (Headphones): Refers to 'Sarvam Thaala Mayam', about music and passion.",
    "🐎🏹": "🐎 (Horse) + 🏹 (Bow and arrow): Represents 'Kaavalan', a romantic action movie.",
    "👩‍🏫📚": "👩‍🏫 (Teacher) + 📚 (Books): Symbolizes 'Kandukondain Kandukondain', a romantic drama with education themes.",
    "🍫🍭": "🍫 (Chocolate) + 🍭 (Candy): Refers to 'Chocklet', a romantic drama.",
    "🩸🏛️": "🩸 (Blood) + 🏛️ (Court): Points to 'Raatchasan', a thriller about a serial killer and investigation.",
    "🏖️🌴": "🏖️ (Beach) + 🌴 (Palm tree): Represents 'Sura', a fishing village action movie.",
    "🐷🎯": "🐷 (Pig) + 🎯 (Target): Refers to 'Oru Oorla Rendu Raja', a comedy-action movie.",
    "🎤🎸": "🎤 (Mic) + 🎸 (Guitar): Symbolizes 'Petta', a mass entertainer with style and music.",
    "🛣️🚙": "🛣️ (Road) + 🚙 (Car): Points to 'Kadhalar Dhinam', a romantic movie.",
    "🏛️⚖️": "🏛️ (Court) + ⚖️ (Justice scale): Represents 'Jai Bhim', a courtroom drama about justice.",
    "🏥🩺": "🏥 (Hospital) + 🩺 (Stethoscope): Refers to 'Doctor', an action comedy with a doctor hero.",
    "🌌🚀": "🌌 (Galaxy) + 🚀 (Rocket): Symbolizes 'Enthiran', a sci-fi robot movie.",
    "🪖🇮🇳": "🪖 (Soldier helmet) + 🇮🇳 (India flag): Points to 'Indian', a patriotic action movie.",
    "🧑‍🚀🪐": "🧑‍🚀 (Astronaut) + 🪐 (Planet): Represents 'Manithan', a social drama.",
    "🎭🕴️": "🎭 (Drama mask) + 🕴️ (Man walking): Refers to 'Aalavandhan', a psychological thriller.",
    "🌊🚤": "🌊 (Water wave) + 🚤 (Speedboat): Points to 'Anniyan', a thriller with multiple personalities.",
    "💼🧠": "💼 (Briefcase) + 🧠 (Brain): Symbolizes 'Ratsasan', a serial killer thriller.",
    "🧙‍♂️🔮": "🧙‍♂️ (Wizard) + 🔮 (Crystal ball): Refers to 'Magadheera', a reincarnation fantasy epic.",
    "🚘🛣️": "🚘 (Car) + 🛣️ (Road): Represents 'Saivam', a family drama about journeys.",
    "🦁👑": "🦁 (Lion) + 👑 (Crown): Refers to 'The Lion King', a classic animated movie (Tamil dub).",
    "🦜🌴": "🦜 (Parrot) + 🌴 (Palm tree): Points to 'Kaakha Kaakha 2', a sequel to the cop movie.",
    "🐦🎤": "🐦 (Bird) + 🎤 (Mic): Refers to 'Papanasam', a thriller about a family man.",
    "🚢🌊": "🚢 (Ship) + 🌊 (Water wave): Represents 'Kadhalan 2', a romantic movie sequel.",
    "🐍💀": "🐍 (Snake) + 💀 (Skull): Points to 'Neelam', a thriller/horror movie.",
    "🏹🗡️": "🏹 (Bow and arrow) + 🗡️ (Sword): Symbolizes 'Vikram', an action thriller.",
    "🚓🚨": "🚓 (Police car) + 🚨 (Siren): Refers to 'Beast', an action movie.",
    "🪆🎯": "🪆 (Russian doll) + 🎯 (Target): Points to 'Master', a mass entertainer.",
    "🎤🎧": "🎤 (Mic) + 🎧 (Headphones): Symbolizes 'Bigil', a sports and music drama.",
    "👓💼": "👓 (Glasses) + 💼 (Briefcase): Refers to 'Don', a stylish action movie.",
    "🕶️🔫": "🕶️ (Sunglasses) + 🔫 (Gun): Points to 'Thunivu', a heist action thriller.",
    "🌅🛕": "🌅 (Sunrise) + 🛕 (Temple): Represents 'Varisu', a family drama.",
    "🏏🎯": "🏏 (Cricket) + 🎯 (Target): Refers to 'Kanaa', a sports drama about cricket."
}


# ==== RUNTIME QUESTIONS ====
active_questions = {}
ended_games = set()

# ==== BOT INSTANCE ====
bot = Client("emoji_movie_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ==== SCORE FUNCTIONS ====
def get_score(user_id: int) -> int:
    user = scores_collection.find_one({"user_id": user_id})
    return user["score"] if user and "score" in user else 0

def update_score(user_id: int, name: str):
    scores_collection.update_one(
        {"user_id": user_id},
        {"$inc": {"score": 1}, "$set": {"name": name}},
        upsert=True
    )

# ==== COMMAND HANDLERS ====
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
async def help_info(_, query):
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

@bot.on_message(filters.command("myscore"))
async def my_score(_, message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    points = get_score(user_id)
    await message.reply(f"🏆 {name}, உங்கள் புள்ளிகள்: {points}")

@bot.on_message(filters.command("emoji") & filters.group)
async def send_emoji_question(_, message):
    chat_id = message.chat.id
    if chat_id in ended_games:
        await message.reply("🛑 விளையாட்டு நிறுத்தப்பட்டுள்ளது. மீண்டும் தொடங்க முடியாது.")
        return

    movie = random.choice(movies)
    correct = movie[1]

    # Show the full emoji clue (not partial)
    emoji_clue = movie[0]

    # Wrong choices with same first letter if possible
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

@bot.on_message(filters.command("skip") & filters.group)
async def skip_question(_, message):
    chat_id = message.chat.id
    for qid, qdata in list(active_questions.items()):
        if qdata.get("chat_id") == chat_id:
            correct_text = qdata["options"][qdata["correct_index"]]
            emoji_clue = qdata.get("emoji_clue", "")
            explanation = emoji_meanings.get(emoji_clue, "Sorry, no explanation available for this emoji clue.")
            await message.reply(f"⏭ கேள்வி தவிர்க்கப்பட்டது!\nசரியான பதில்: {correct_text}\n\n📖 விளக்கம்:\n{explanation}")
            active_questions.pop(qid, None)
            return
    await message.reply("⏭ தற்போது எதுவும் கேள்வி இல்லை.")

@bot.on_message(filters.command("end") & filters.group)
async def end_game(_, message):
    chat_id = message.chat.id
    ended_games.add(chat_id)
    for qid, qdata in list(active_questions.items()):
        if qdata.get("chat_id") == chat_id:
            active_questions.pop(qid, None)
    await message.reply("🛑 விளையாட்டு நிறுத்தப்பட்டது!.")

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
        await query.message.edit_text(
            f"🏆 {user_name} சரியாக கண்டுபிடித்தார்!\nசரியான பதில்: {correct_text}\n\n📖 விளக்கம்:\n{explanation}"
        )
        qdata["closed"] = True
        active_questions.pop(qid, None)
    else:
        await query.answer("❌ தவறு!", show_alert=True)

bot.run()
