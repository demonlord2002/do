import random
import asyncio
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient
from config import API_ID, API_HASH, BOT_TOKEN, MONGO_URI, DB_NAME, COLLECTION_NAME, OWNER_USER_ID, CHANNEL_LINK

# ==== MONGODB CONNECT ====
mongo_client = MongoClient(MONGO_URI)
db = mongo_client[DB_NAME]
scores_collection = db[COLLECTION_NAME]

# ==== MOVIE DATA ====
# --- Movie & Emoji data ---
movies = [
    ("🐯🔥", "Puli"),  # Tiger + Fire — symbolizing 'Puli' (Tiger)
    ("🕷️👨", "Spider-Man: No Way Home (Tamil Dub)"),
    ("🐯💪", "Singam"),
    ("👑🏰", "Ponniyin Selvan"),
    ("🚀🌕", "Tik Tik Tik"),
    ("🌊🐠", "Meen Kuzhambum Mann Paanaiyum"),
    ("🏹🔥", "Baahubali"),
    ("👻🏠", "Kanchana"),
    ("🛕🚜", "Thirupaachi"),  # Temple + Tractor — rural theme
    ("👩‍🍳🍲", "Saivam"),
    ("🐘🎯", "Kumki"),  # Elephant + Target — elephant featured in movie
    ("👨‍⚕️💊", "Mersal"),
    ("💣🕵️", "Vivegam"),
    ("🎭🎤", "Kaadhalan"),
    ("👮‍♂️🔥", "Theri"),  # Cop + Fire — main character is cop with fiery revenge
    ("🕰️🔄", "Maanaadu"),  # Clock + Repeat — time loop theme
    ("🛶🏝️", "Kaadhalum Kadanthu Pogum"),
    ("🎸🎤", "Rockstar (Tamil Dub)"),
    ("🚔🔫", "Kaakha Kaakha"),
    ("💃🕺", "Ok Kanmani"),
    ("🪖🔫", "Theeran Adhigaaram Ondru"),
    ("🦸‍♂️⚡", "Minnal Murali (Tamil Dub)"),
    ("🐆🔫", "Kaala"),
    ("🏍️💨", "Irumbu Thirai"),
    ("🎩🎩", "Gentleman"),
    ("🕰️🔄", "24"),
    ("👑🔥", "Sivaji"),  # Crown + Fire — fiery drama and leader
    ("👩‍👦❤️", "Pasanga"),
    ("👨‍🌾🌾", "Kadaikutty Singam"),
    ("👊🩸", "Asuran"),
    ("🎯🎯", "Thuppakki"),
    ("🚖🛣️", "Anegan"),
    ("🛶🐟", "Paruthiveeran"),
    ("🧟‍♂️🏃", "Miruthan"),
    ("🔪👩", "Psycho"),
    ("💼🏢", "Mankatha"),
    ("🕵️‍♂️🔍", "Detective"),
    ("👩‍❤️‍👨💔", "96"),
    ("💃💔", "Mayakkam Enna"),
    ("🏏🏆", "Chennai 600028"),
    ("🐒🎭", "Ko"),
    ("📚🎓", "Nanban"),
    ("🚚💨", "Vettai"),
    ("🪂🌪️", "Soorarai Pottru"),
    ("👩‍👩‍👦", "Thanga Meengal"),
    ("🕯️🌌", "Engeyum Eppodhum"),
    ("🎨👩", "Raja Rani"),
    ("🚀🪐", "Indru Netru Naalai"),
    ("🐍🩸", "Naan Avanillai"),
    ("🚤🏖️", "Billa"),
    ("🏞️🐘", "Aaranya Kaandam"),
    ("🛕🙏", "Kovil"),
    ("👮🔫", "Saamy"),
    ("💔🎼", "Vinnaithaandi Varuvaayaa"),
    ("🚂🏞️", "Pariyerum Perumal"),
    ("🎤🎧", "Sarvam Thaala Mayam"),
    ("🐎🏹", "Kaavalan"),
    ("👩‍🏫📚", "Kandukondain Kandukondain"),
    ("🍫🍭", "Chocklet"),
    ("🩸🏛️", "Raatchasan"),
    ("🏖️🌴", "Sura"),
    ("🐷🎯", "Oru Oorla Rendu Raja"),
    ("🎤🎸", "Petta"),
    ("🛣️🚙", "Kadhalar Dhinam"),
    ("🏛️⚖️", "Jai Bhim"),
    ("🏥🩺", "Doctor"),
    ("🌌🚀", "Enthiran"),
    ("🪖🇮🇳", "Indian"),
    ("🧑‍🚀🪐", "Manithan"),
    ("🎭🕴️", "Aalavandhan"),
    ("🌊🚤", "Anniyan"),
    ("💼🧠", "Ratsasan"),
    ("🧙‍♂️🔮", "Magadheera (Tamil Dub)"),
    ("🚘🛣️", "Saivam"),
    ("🦁👑", "The Lion King (Tamil Dub)"),
    ("🚓🔫", "Kaakha Kaakha 2"),  # Police car + Gun for sequel
    ("👨‍👩‍👧‍👦🔍", "Papanasam"),  # Family + Detective
    ("🚢🌊", "Kadhalan 2"),
    ("🐍💀", "Neelam"),
    ("🏹🗡️", "Vikram"),
    ("🚓🚨", "Beast"),
    ("🎓🔥", "Master"),  # Graduation cap + Fire for mass entertainer
    ("🎤🎧", "Bigil"),
    ("👓💼", "Don"),
    ("🕶️🔫", "Thunivu"),
    ("🌅🛕", "Varisu"),
    ("🏏🎯", "Kanaa")
]

emoji_meanings = {
    "🐯🔥": "Tiger + Fire: Represents 'Puli' symbolizing the fierce and bold nature.",
    "🕷️👨": "Spider + Man: Refers to 'Spider-Man', the superhero.",
    "🐯💪": "Tiger + Strong arm: Symbolizes 'Singam', meaning Lion, strength and bravery.",
    "👑🏰": "Crown + Castle: Indicates royalty and kingdom, 'Ponniyin Selvan'.",
    "🚀🌕": "Rocket + Moon: Refers to 'Tik Tik Tik', a space thriller.",
    "🌊🐠": "Water wave + Fish: Represents 'Meen Kuzhambum Mann Paanaiyum', fish and water.",
    "🏹🔥": "Bow and arrow + Fire: Symbolizes 'Baahubali', warrior and battle.",
    "👻🏠": "Ghost + House: Represents horror movie 'Kanchana'.",
    "🛕🚜": "Temple + Tractor: Points to rural backdrop in 'Thirupaachi'.",
    "👩‍🍳🍲": "Chef + Food: Refers to 'Saivam', family and food traditions.",
    "🐘🎯": "Elephant + Target: Symbolizes 'Kumki', involving an elephant.",
    "👨‍⚕️💊": "Doctor + Medicine: Points to 'Mersal', a doctor protagonist.",
    "💣🕵️": "Bomb + Detective: Refers to 'Vivegam', action and espionage.",
    "🎭🎤": "Drama mask + Microphone: Indicates 'Kaadhalan', romantic musical.",
    "👮‍♂️🔥": "Cop + Fire: Represents 'Theri', cop with fiery vengeance.",
    "🕰️🔄": "Clock + Repeat: Refers to 'Maanaadu', time loop thriller.",
    "🛶🏝️": "Boat + Island: Points to romantic travel in 'Kaadhalum Kadanthu Pogum'.",
    "🎸🎤": "Guitar + Microphone: Musical drama 'Rockstar'.",
    "🚔🔫": "Police car + Gun: 'Kaakha Kaakha', cop action.",
    "💃🕺": "Dancers: 'Ok Kanmani', romantic dance.",
    "🪖🔫": "Military helmet + Gun: 'Theeran Adhigaaram Ondru', police action.",
    "🦸‍♂️⚡": "Superhero + Lightning: 'Minnal Murali'.",
    "🐆🔫": "Leopard + Gun: 'Kaala', gangster movie.",
    "🏍️💨": "Motorcycle + Speed: 'Irumbu Thirai', fast action.",
    "🎩🎩": "Top hats: 'Gentleman', classy hero.",
    "🕰️🔄": "Clock + Repeat: '24', time thriller.",
    "👑🔥": "Crown + Fire: 'Sivaji', fiery drama.",
    "👩‍👦❤️": "Mother + Child + Heart: 'Pasanga', family drama.",
    "👨‍🌾🌾": "Farmer + Crop: 'Kadaikutty Singam', rural story.",
    "👊🩸": "Fist + Blood: 'Asuran', revenge drama.",
    "🎯🎯": "Targets: 'Thuppakki', precision thriller.",
    "🚖🛣️": "Taxi + Road: 'Anegan', journey romance.",
    "🛶🐟": "Boat + Fish: 'Paruthiveeran', rural drama.",
    "🧟‍♂️🏃": "Zombie + Running: 'Miruthan', zombie thriller.",
    "🔪👩": "Knife + Woman: 'Psycho', thriller.",
    "💼🏢": "Briefcase + Office: 'Mankatha', heist thriller.",
    "🕵️‍♂️🔍": "Detective + Magnifier: 'Detective', mystery.",
    "👩‍❤️‍👨💔": "Couple + Broken Heart: '96', romantic drama.",
    "💃💔": "Dancer + Broken Heart: 'Mayakkam Enna', love story.",
    "🏏🏆": "Cricket + Trophy: 'Chennai 600028', sports drama.",
    "🐒🎭": "Monkey + Drama Mask: 'Ko', political thriller.",
    "📚🎓": "Books + Graduation: 'Nanban', friendship and education.",
    "🚚💨": "Truck + Speed: 'Vettai', action thriller.",
    "🪂🌪️": "Parachute + Tornado: 'Soorarai Pottru', courage and storm.",
    "👩‍👩‍👦": "Family: 'Thanga Meengal', emotional drama.",
    "🕯️🌌": "Candle + Night sky: 'Engeyum Eppodhum', romantic drama.",
    "🎨👩": "Paint palette + Woman: 'Raja Rani', love story.",
    "🚀🪐": "Rocket + Planet: 'Indru Netru Naalai', sci-fi time travel.",
    "🐍🩸": "Snake + Blood: 'Naan Avanillai', thriller.",
    "🚤🏖️": "Speedboat + Beach: 'Billa', stylish action.",
    "🏞️🐘": "Landscape + Elephant: 'Aaranya Kaandam', gangster.",
    "🛕🙏": "Temple + Prayer: 'Kovil', devotional drama.",
    "👮🔫": "Police + Gun: 'Saamy', police action.",
    "💔🎼": "Broken Heart + Music: 'Vinnaithaandi Varuvaayaa', romantic musical.",
    "🚂🏞️": "Train + Landscape: 'Pariyerum Perumal', social drama.",
    "🎤🎧": "Mic + Headphones: 'Sarvam Thaala Mayam', music passion.",
    "🐎🏹": "Horse + Bow and Arrow: 'Kaavalan', action romance.",
    "👩‍🏫📚": "Teacher + Books: 'Kandukondain Kandukondain', education theme.",
    "🍫🍭": "Chocolate + Candy: 'Chocklet', romantic drama.",
    "🩸🏛️": "Blood + Court: 'Raatchasan', serial killer thriller.",
    "🏖️🌴": "Beach + Palm Tree: 'Sura', fishing village action.",
    "🐷🎯": "Pig + Target: 'Oru Oorla Rendu Raja', comedy-action.",
    "🎤🎸": "Mic + Guitar: 'Petta', mass entertainer.",
    "🛣️🚙": "Road + Car: 'Kadhalar Dhinam', romance.",
    "🏛️⚖️": "Court + Justice: 'Jai Bhim', courtroom drama.",
    "🏥🩺": "Hospital + Stethoscope: 'Doctor', action comedy.",
    "🌌🚀": "Galaxy + Rocket: 'Enthiran', sci-fi robot.",
    "🪖🇮🇳": "Soldier Helmet + India Flag: 'Indian', patriotic.",
    "🧑‍🚀🪐": "Astronaut + Planet: 'Manithan', social drama.",
    "🎭🕴️": "Drama Mask + Man Walking: 'Aalavandhan', psychological thriller.",
    "🌊🚤": "Water Wave + Speedboat: 'Anniyan', thriller.",
    "💼🧠": "Briefcase + Brain: 'Ratsasan', serial killer thriller.",
    "🧙‍♂️🔮": "Wizard + Crystal Ball: 'Magadheera', fantasy epic.",
    "🚘🛣️": "Car + Road: 'Saivam', family journey.",
    "🦁👑": "Lion + Crown: 'The Lion King', animated classic.",
    "🚓🔫": "Police Car + Gun: 'Kaakha Kaakha 2', sequel.",
    "👨‍👩‍👧‍👦🔍": "Family + Detective: 'Papanasam', family thriller.",
    "🚢🌊": "Ship + Water Wave: 'Kadhalan 2', romantic sequel.",
    "🐍💀": "Snake + Skull: 'Neelam', thriller/horror.",
    "🏹🗡️": "Bow + Sword: 'Vikram', action thriller.",
    "🚓🚨": "Police Car + Siren: 'Beast', action.",
    "🎓🔥": "Graduation Cap + Fire: 'Master', mass entertainer.",
    "🎤🎧": "Mic + Headphones: 'Bigil', sports/music drama.",
    "👓💼": "Glasses + Briefcase: 'Don', stylish action.",
    "🕶️🔫": "Sunglasses + Gun: 'Thunivu', heist thriller.",
    "🌅🛕": "Sunrise + Temple: 'Varisu', family drama.",
    "🏏🎯": "Cricket + Target: 'Kanaa', sports drama."
}
# ==== RUNTIME QUESTIONS ====
active_questions = {}
ended_games = set()
lock = asyncio.Lock()  # To prevent race conditions on active_questions

# ==== BOT INSTANCE ====
bot = Client("emoji_movie_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ==== SCORE FUNCTIONS ====
def get_score(user_id: int) -> int:
    try:
        user = scores_collection.find_one({"user_id": user_id})
        return user["score"] if user and "score" in user else 0
    except Exception as e:
        print(f"MongoDB get_score error: {e}")
        return 0

def update_score(user_id: int, name: str):
    try:
        scores_collection.update_one(
            {"user_id": user_id},
            {"$inc": {"score": 1}, "$set": {"name": name}},
            upsert=True
        )
    except Exception as e:
        print(f"MongoDB update_score error: {e}")

# ==== COMMAND HANDLERS ====
BOT_NAME = "˹🌙 ᴀᴢʜᴀɢɪʏᴀ ✘ ᴍᴏᴊɪ˼"
fancy_bot_name = f"{BOT_NAME}"

@bot.on_message(filters.command("start"))
async def start(_, message):
    start_buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🌸 Owner", url="https://t.me/TheAnonymous_II"),
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

    # Optional: Check if a question is already active for this chat to avoid flooding
    async with lock:
        for qid, qdata in active_questions.items():
            if qdata.get("chat_id") == chat_id and not qdata.get("closed", False):
                await message.reply("❗ ஏற்கனவே ஒரு கேள்வி உள்ளது. தயவு செய்து பதில் சொல்லுங்கள் அல்லது /skip செய்யுங்கள்.")
                return

        movie = random.choice(movies)
        correct = movie[1]
        emoji_clue = movie[0]

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
    async with lock:
        active_questions[qid]["msg_id"] = sent.message_id

@bot.on_message(filters.command("skip") & filters.group)
async def skip_question(_, message):
    chat_id = message.chat.id
    async with lock:
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
    async with lock:
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

    async with lock:
        qdata = active_questions.get(qid)
        if not qdata:
            await query.answer("இந்த கேள்வி காலாவதியாகிவிட்டது.", show_alert=True)
            return

        user_id = query.from_user.id
        user_name = query.from_user.first_name

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

            # Edit message with answer
            try:
                await query.message.edit_text(
                    f"🏆 {user_name} சரியாக கண்டுபிடித்தார்!\nசரியான பதில்: {correct_text}\n\n📖 விளக்கம்:\n{explanation}"
                )
            except Exception as e:
                print(f"Failed to edit message: {e}")

            qdata["closed"] = True
            # Remove question after short delay to allow others to see result
            active_questions.pop(qid, None)
        else:
            await query.answer("❌ தவறு!", show_alert=True)

bot.run()
