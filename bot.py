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
    ("🐅🔔", "Puli"), ("🕷️🧑", "Spider-Man: No Way Home (Tamil Dub)"), ("🦁💪", "Singam"),
    ("👑🏰", "Ponniyin Selvan"), ("🚀🌕", "Tik Tik Tik"), ("🐟🍲", "Meen Kuzhambum Mann Paanaiyum"),
    ("🏹🔥", "Baahubali"), ("👻🏚️", "Kanchana"), ("🛕🛡️", "Thirupaachi"), ("👩‍👧‍👦🍲", "Saivam"),
    ("🐘🎯", "Kumki"), ("👨‍⚕️💊", "Mersal"), ("💣🕵️‍♂️", "Vivegam"), ("🎭🎶", "Kaadhalan"),
    ("👨‍🚒🔥", "Theri"), ("🕰️🔄", "Maanaadu"), ("🛶❤️🏝️", "Kaadhalum Kadanthu Pogum"),
    ("🎸🎤", "Rockstar (Tamil Dub)"), ("🚓🔫", "Kaakha Kaakha"), ("💃🕺", "Ok Kanmani"),
    ("🪖🔫", "Theeran Adhigaaram Ondru"), ("🦸‍♂️⚡", "Minnal Murali (Tamil Dub)"),
    ("🐆🔫", "Kaala"), ("🏍️💨", "Irumbu Thirai"), ("🎩🎩", "Gentleman"), ("🕰️⏳", "24"),
    ("🌋🔥", "Sivaji"), ("👩‍👦❤️", "Pasanga"), ("👨‍🌾🌾", "Kadaikutty Singam"),
    ("👊🩸", "Asuran"), ("🎯🚁", "Thuppakki"), ("🚕🛣️", "Anegan"), ("🛶🐟", "Paruthiveeran"),
    ("🧟‍♂️🏃", "Miruthan"), ("🔪👩", "Psycho"), ("💼🏢", "Mankatha"), ("🕵️‍♂️🔍", "Detective"),
    ("👩‍❤️‍👨💔", "96"), ("💃💔", "Mayakkam Enna"), ("🏏🏆", "Chennai 600028"),
    ("🐒🎭", "Ko"), ("📚🎓", "Nanban"), ("🚚💨", "Vettai"), ("🪂🌪️", "Soorarai Pottru"),
    ("👩‍👩‍👦", "Thanga Meengal"), ("🕯️🌌", "Engeyum Eppodhum"), ("🎨👩", "Raja Rani"),
    ("🚀🪐", "Indru Netru Naalai"), ("🐍🩸", "Naan Avanillai"), ("🚤🏖️", "Billa"),
    ("🏞️🐘", "Aaranya Kaandam"), ("🛕🙏", "Kovil"), ("👮‍♂️🔫", "Saamy"),
    ("💔🎼", "Vinnaithaandi Varuvaayaa"), ("🚂🏞️", "Pariyerum Perumal"),
    ("🎤🎧", "Sarvam Thaala Mayam"), ("🐎🏹", "Kaavalan"), ("👩‍🏫📚", "Kandukondain Kandukondain"),
    ("🍫🍭", "Chocklet"), ("🩸🏛️", "Raatchasan"), ("🏖️🌴", "Sura"), ("🐖🎯", "Oru Oorla Rendu Raja"),
    ("🎤🎸", "Petta"), ("🛣️🚙", "Kadhalar Dhinam"), ("🏛️⚖️", "Jai Bhim"), ("🏥🩺", "Doctor"),
    ("🌌🤖", "Enthiran"), ("🪖🇮🇳", "Indian"), ("🧑‍🚀🪐", "Manithan"), ("🎭🕴️", "Aalavandhan"),
    ("🌊🚤", "Anniyan"), ("💼🧠", "Ratsasan"), ("🧙‍♂️🔮", "Magadheera (Tamil Dub)"),
    ("🚗🛣️", "Saivam"), ("🦁👑", "The Lion King (Tamil Dub)"), ("🦜🌴", "Kaakha Kaakha 2"),
    ("🐦🎤", "Papanasam"), ("🚢🌊", "Kadhalan 2"), ("🐍💀", "Neelam"), ("🏹🗡️", "Vikram"),
    ("🚓🚨", "Beast"), ("🪆🎯", "Master"), ("🎤🎧", "Bigil"), ("👓💼", "Don"), ("🕶️🔫", "Thunivu"),
    ("🌅🛕", "Varisu"), ("🏏🎯", "Kanaa"),

    # Additional 100 movies with emojis:
    ("🎬🕵️", "Dhruva Natchathiram"),               # Film + Spy
    ("🦖🌴", "Jurassic Park (Tamil Dub)"),          # Dinosaur + Jungle
    ("🐦🦜", "Birds of Prey"),                       # Birds
    ("🕷️🕸️", "Spider-Man"),                        # Spider + Web
    ("🏹🧙‍♂️", "Archer & Wizard"),                   # Archer + Wizard (fictional)
    ("🚗💨", "Race Gurram"),                         # Car + Speed
    ("🛡️⚔️", "Veeram"),                             # Shield + Sword
    ("👨‍🚀🌌", "Interstellar"),                       # Astronaut + Space
    ("🎭💔", "7aum Arivu"),                          # Drama + Heartbreak (fictional)
    ("👊💥", "Panjaa"),                              # Punch + Explosion
    ("🧛‍♂️🦇", "Iraivi"),                            # Vampire + Bat (fictional)
    ("🛶🌊", "Neerparavai"),                          # Boat + Water
    ("🌾🚜", "Thondan"),                             # Crops + Tractor
    ("🎯🎯", "Singam 2"),                            # Target + Target
    ("🎭💃", "Kaatru Veliyidai"),                     # Drama + Dance
    ("🚗🔫", "Dhuruvangal Pathinaaru"),              # Car + Gun
    ("🕷️🏙️", "Spider-Man: Far From Home"),         # Spider + Cityscape
    ("💣💥", "Boomerang"),                           # Bomb + Explosion
    ("🎧🎤", "K.K."),                               # Headphones + Mic (fictional)
    ("👩‍🎤🎸", "Rock On"),                           # Singer + Guitar
    ("🕵️‍♂️💼", "Maya"),                            # Detective + Briefcase (fictional)
    ("👽🚀", "Alien"),                               # Alien + Rocket
    ("🌊🛶", "Naan Sigappu Manithan"),               # Wave + Boat
    ("⚔️🛡️", "Ponniyin Selvan 2"),                   # Sword + Shield
    ("💃🕺", "Remo"),                                # Dance + Dance
    ("🎩🕴️", "Gentleman Returns"),                   # Hat + Man walking
    ("🚓🚨", "Singam 3"),                            # Police + Siren
    ("👩‍🌾🌱", "Marudhamalai"),                      # Farmer + Plant
    ("🌪️🔥", "Anjaan"),                             # Tornado + Fire
    ("🚗🏁", "Vivegam 2"),                           # Car + Finish flag
    ("👑🗡️", "Kaaviya Thalaivan"),                   # Crown + Sword
    ("🏹🐅", "Rudhramadevi"),                        # Bow + Tiger (fictional)
    ("👩‍🔬🧪", "Yennai Arindhaal"),                   # Scientist + Test tube
    ("🕶️🔫", "Thuppakki Returns"),                   # Sunglasses + Gun
    ("🏞️🐘", "Aadai"),                               # Landscape + Elephant (fictional)
    ("👮‍♀️🚓", "Police"),                            # Female cop + Police car
    ("🏰⚔️", "Chola Empire"),                        # Castle + Sword (fictional)
    ("👨‍👩‍👧‍👦❤️", "Pichaikkaran"),                   # Family + Heart
    ("🦸‍♂️🛡️", "Hero"),                             # Superhero + Shield
    ("🎼🎤", "Kadhalum Kadandhu Pogum"),              # Music + Mic
    ("🧟‍♀️⚰️", "Zombie"),                            # Zombie + Coffin
    ("🚀👩‍🚀", "Apollo 18"),                         # Rocket + Astronaut
    ("💀🔪", "Ratsasan 2"),                          # Skull + Knife
    ("🎩🕵️‍♂️", "Sherlock"),                         # Hat + Detective
    ("🚁💥", "Airlift"),                             # Helicopter + Explosion
    ("🎓🏆", "Vishwaroopam"),                         # Graduation + Trophy
    ("🚤💨", "Thani Oruvan"),                         # Speedboat + Speed
    ("🛡️🗡️", "Rajinikanth"),                         # Shield + Sword (fictional)
    ("🎭💔", "Ok Bangaram"),                          # Drama + Broken heart
    ("🕷️🎯", "Spider-Man: No Way Home"),             # Spider + Target
    ("🏍️🔥", "Velaiyilla Pattathari"),               # Motorcycle + Fire
    ("🎤🕺", "Tamizhan"),                             # Mic + Dancing man
    ("💔🎬", "Mouna Guru"),                           # Broken heart + Film
    ("🐒🚨", "Ko 2"),                                # Monkey + Police siren
    ("🚀🌠", "24 (Telugu Dub)"),                      # Rocket + Shooting star
    ("🧟‍♂️🧠", "Miruthan 2"),                        # Zombie + Brain
    ("🎼🩸", "Ratsasan 3"),                           # Music + Blood
    ("🎩👨‍🎤", "Master 2"),                          # Hat + Singer
    ("🏍️🛣️", "Irumbu Thirai 2"),                      # Motorcycle + Road
    ("👩‍⚕️🚑", "Doctor 2"),                          # Doctor + Ambulance
    ("🎬🔥", "Petta 2"),                              # Film + Fire
    ("🦁🗡️", "Kaala 2"),                             # Lion + Sword
    ("🚂💥", "Enthiran 2"),                           # Train + Explosion
    ("🎭👑", "Ponniyin Selvan 3"),                     # Drama + Crown
    ("🧙‍♂️🪄", "Magadheera 2"),                       # Wizard + Magic wand


# ==== EMOJI MEANINGS ====
emojis_meaning = {
    "🐅🔔": "🐅 (Tiger) + 🔔 (Bell): Represents 'Puli' — 'Puli' means tiger, bell here suggests alertness.",
    "🕷️👨": "🕷️ (Spider) + 👨 (Man): Refers to 'Spider-Man', the superhero with spider-like powers.",
    "🐯💪": "🐯 (Tiger) + 💪 (Strong arm): Symbolizes 'Singam' (Lion), representing strength and bravery.",
    "👑🏰": "👑 (Crown) + 🏰 (Castle): Indicates royalty and kingdom, pointing to 'Ponniyin Selvan'.",
    "🚀🌕": "🚀 (Rocket) + 🌕 (Moon): Refers to 'Tik Tik Tik', a space-themed thriller.",
    "🌊🐠": "🌊 (Water wave) + 🐠 (Fish): Related to 'Meen Kuzhambum Mann Paanaiyum', involving fish and water.",
    "🏹🔥": "🏹 (Bow and arrow) + 🔥 (Fire): Symbolizes 'Baahubali', a warrior film.",
    "👻🏠": "👻 (Ghost) + 🏠 (House): Represents 'Kanchana', a horror movie set in a haunted house.",
    "🛕🦅": "🛕 (Temple) + 🦅 (Eagle): Represents 'Thirupaachi', a movie with rural temple backdrop and vigilance.",
    "👩‍🍳🍲": "👩‍🍳 (Chef) + 🍲 (Food): Refers to 'Saivam', emphasizing family and food traditions.",
    "🐅🎯": "🐅 (Tiger) + 🎯 (Target): Symbolizes 'Kumki', a movie about wild animals and mahouts.",
    "👨‍⚕️💊": "👨‍⚕️ (Doctor) + 💊 (Medicine): Points to 'Mersal', featuring a doctor protagonist.",
    "💣🕵️": "💣 (Bomb) + 🕵️ (Detective): Refers to 'Vivegam', an espionage action thriller.",
    "🎭🎤": "🎭 (Drama mask) + 🎤 (Microphone): Indicates 'Kaadhalan', a romantic musical drama.",
    "👨‍🚒🔥": "👨‍🚒 (Firefighter) + 🔥 (Fire): Represents 'Theri', an action movie with fiery vengeance.",
    "🕰️🔄": "🕰️ (Clock) + 🔄 (Repeat): Represents 'Maanaadu', a time loop political thriller.",
    "🛶🏝️": "🛶 (Boat) + 🏝️ (Island): Points to 'Kaadhalum Kadanthu Pogum', a romantic travel story.",
    "🎸🎤": "🎸 (Guitar) + 🎤 (Microphone): Refers to 'Rockstar', a musical drama.",
    "🚔🔫": "🚔 (Police car) + 🔫 (Gun): Symbolizes 'Kaakha Kaakha', a cop action thriller.",
    "💃🕺": "💃 (Woman dancing) + 🕺 (Man dancing): Represents 'Ok Kanmani', a romantic dance-filled movie.",
    "🪖🔫": "🪖 (Military helmet) + 🔫 (Gun): Points to 'Theeran Adhigaaram Ondru', a police action movie.",
    "🦸‍♂️⚡": "🦸‍♂️ (Superhero) + ⚡ (Lightning): Represents 'Minnal Murali', a superhero film.",
    "🐆🔫": "🐆 (Leopard) + 🔫 (Gun): Refers to 'Kaala', a gangster film symbolized by the fierce leopard.",
    "🏍️💨": "🏍️ (Motorcycle) + 💨 (Speed): Points to 'Irumbu Thirai', a fast-paced action thriller.",
    "🎩🎩": "🎩 (Two top hats): Symbolizes 'Gentleman', representing a classy hero.",
    "🕰️⏳": "🕰️ (Clock) + ⏳ (Hourglass): Represents '24', a thriller revolving around time.",
    "🌋🔥": "🌋 (Volcano) + 🔥 (Fire): Symbolizes 'Sivaji', a fiery and explosive drama.",
    "👩‍👦❤️": "👩‍👦 (Mother and child) + ❤️ (Love): Points to 'Pasanga', a family drama focusing on children.",
    "👨‍🌾🌾": "👨‍🌾 (Farmer) + 🌾 (Crop): Represents 'Kadaikutty Singam', a rural farmer-based story.",
    "👊🩸": "👊 (Fist) + 🩸 (Blood): Symbolizes 'Asuran', a violent revenge drama.",
    "🎯🚁": "🎯 (Target) + 🚁 (Helicopter): Refers to 'Thuppakki', a thriller involving precision attacks.",
    "🚕🛣️": "🚕 (Taxi) + 🛣️ (Road): Points to 'Anegan', a romantic movie involving journeys.",
    "🛶🐟": "🛶 (Boat) + 🐟 (Fish): Represents 'Paruthiveeran', a rural action drama.",
    "🧟‍♂️🏃": "🧟‍♂️ (Zombie) + 🏃 (Running): Refers to 'Miruthan', a zombie apocalypse movie.",
    "🔪👩": "🔪 (Knife) + 👩 (Woman): Points to 'Psycho', a thriller with a female lead.",
    "💼🏢": "💼 (Briefcase) + 🏢 (Office building): Refers to 'Mankatha', a heist thriller.",
    "🕵️‍♂️🔍": "🕵️‍♂️ (Detective) + 🔍 (Magnifying glass): Symbolizes 'Detective', a mystery thriller.",
    "👩‍❤️‍👨💔": "👩‍❤️‍👨 (Couple) + 💔 (Broken heart): Points to '96', a romantic drama about lost love.",
    "💃💔": "💃 (Dancer) + 💔 (Broken heart): Refers to 'Mayakkam Enna', a love story with emotional turmoil.",
    "🏏🏆": "🏏 (Cricket) + 🏆 (Trophy): Symbolizes 'Chennai 600028', a sports drama.",
    "🐒🎭": "🐒 (Monkey) + 🎭 (Drama mask): Refers to 'Ko', a political thriller with twists.",
    "📚🎓": "📚 (Books) + 🎓 (Graduation cap): Points to 'Nanban', a story about friendship and education.",
    "🚚💨": "🚚 (Truck) + 💨 (Speed): Represents 'Vettai', an action thriller.",
    "🪂🌪️": "🪂 (Parachute) + 🌪️ (Tornado): Refers to 'Soorarai Pottru', about courage against odds.",
    "👩‍👩‍👦": "👩‍👩‍👦 (Family): Represents 'Thanga Meengal', a family emotional drama.",
    "🕯️🌌": "🕯️ (Candle) + 🌌 (Night sky): Symbolizes 'Engeyum Eppodhum', a romantic drama.",
    "🎨👩": "🎨 (Paint palette) + 👩 (Woman): Refers to 'Raja Rani', a love story with artistic elements.",
    "🚀🪐": "🚀 (Rocket) + 🪐 (Planet): Points to 'Indru Netru Naalai', a sci-fi time travel movie.",
    "🐍🩸": "🐍 (Snake) + 🩸 (Blood): Refers to 'Naan Avanillai', a thriller with deception.",
    "🚤🏖️": "🚤 (Speedboat) + 🏖️ (Beach): Symbolizes 'Billa', a stylish action thriller.",
    "🏞️🐘": "🏞️ (Landscape) + 🐘 (Elephant): Points to 'Aaranya Kaandam', a gangster movie.",
    "🛕🙏": "🛕 (Temple) + 🙏 (Prayer): Represents 'Kovil', a devotional drama.",
    "👮‍♂️🔫": "👮‍♂️ (Police officer) + 🔫 (Gun): Refers to 'Saamy', a police action movie.",
    "💔🎼": "💔 (Broken heart) + 🎼 (Music): Symbolizes 'Vinnaithaandi Varuvaayaa', a romantic musical.",
    "🚂🏞️": "🚂 (Train) + 🏞️ (Nature): Points to 'Pariyerum Perumal', a social drama.",
    "🎤🎧": "🎤 (Microphone) + 🎧 (Headphones): Refers to 'Sarvam Thaala Mayam', about music.",
    "🐎🏹": "🐎 (Horse) + 🏹 (Bow and arrow): Represents 'Kaavalan', a romantic action movie.",
    "👩‍🏫📚": "👩‍🏫 (Teacher) + 📚 (Books): Symbolizes 'Kandukondain Kandukondain', a romantic drama.",
    "🍫🍭": "🍫 (Chocolate) + 🍭 (Candy): Refers to 'Chocklet', a romantic movie.",
    "🩸🏛️": "🩸 (Blood) + 🏛️ (Court): Points to 'Raatchasan', a serial killer thriller.",
    "🏖️🌴": "🏖️ (Beach) + 🌴 (Palm tree): Represents 'Sura', a fishing village action movie.",
    "🐷🎯": "🐷 (Pig) + 🎯 (Target): Refers to 'Oru Oorla Rendu Raja', a comedy action movie.",
    "🎤🎸": "🎤 (Microphone) + 🎸 (Guitar): Symbolizes 'Petta', a mass entertainer with music.",
    "🛣️🚙": "🛣️ (Road) + 🚙 (Car): Points to 'Kadhalar Dhinam', a romantic movie.",
    "🏛️⚖️": "🏛️ (Court) + ⚖️ (Justice): Represents 'Jai Bhim', a courtroom drama.",
    "🏥🩺": "🏥 (Hospital) + 🩺 (Stethoscope): Refers to 'Doctor', an action comedy.",
    "🌌🤖": "🌌 (Galaxy) + 🤖 (Robot): Symbolizes 'Enthiran', a sci-fi robot movie.",
    "🪖🇮🇳": "🪖 (Soldier helmet) + 🇮🇳 (India flag): Points to 'Indian', a patriotic action movie.",
    "🧑‍🚀🪐": "🧑‍🚀 (Astronaut) + 🪐 (Planet): Represents 'Manithan', a social drama.",
    "🎭🕴️": "🎭 (Drama mask) + 🕴️ (Man walking): Refers to 'Aalavandhan', a psychological thriller.",
    "🌊🚤": "🌊 (Water wave) + 🚤 (Speedboat): Points to 'Anniyan', a thriller with multiple personalities.",
    "💼🧠": "💼 (Briefcase) + 🧠 (Brain): Symbolizes 'Ratsasan', a serial killer thriller.",
    "🧙‍♂️🔮": "🧙‍♂️ (Wizard) + 🔮 (Crystal ball): Refers to 'Magadheera (Tamil Dub)', a reincarnation fantasy.",
    "🚗🛣️": "🚗 (Car) + 🛣️ (Road): Represents 'Saivam', a family drama.",
    "🦁👑": "🦁 (Lion) + 👑 (Crown): Refers to 'The Lion King (Tamil Dub)', classic animation.",
    "🦜🌴": "🦜 (Parrot) + 🌴 (Palm tree): Points to 'Kaakha Kaakha 2', cop action sequel.",
    "🐦🎤": "🐦 (Bird) + 🎤 (Mic): Refers to 'Papanasam', a thriller about family.",
    "🚢🌊": "🚢 (Ship) + 🌊 (Water wave): Represents 'Kadhalan 2', a romantic sequel.",
    "🐍💀": "🐍 (Snake) + 💀 (Skull): Points to 'Neelam', thriller/horror movie.",
    "🏹🗡️": "🏹 (Bow) + 🗡️ (Sword): Symbolizes 'Vikram', action thriller.",
    "🚓🚨": "🚓 (Police car) + 🚨 (Siren): Refers to 'Beast', action movie.",
    "🪆🎯": "🪆 (Matryoshka doll) + 🎯 (Target): Points to 'Master', mass entertainer.",
    "🎤🎧": "🎤 (Mic) + 🎧 (Headphones): Symbolizes 'Bigil', sports drama.",
    "👓💼": "👓 (Glasses) + 💼 (Briefcase): Refers to 'Don', stylish action.",
    "🕶️🔫": "🕶️ (Sunglasses) + 🔫 (Gun): Points to 'Thunivu', heist thriller.",
    "🌅🛕": "🌅 (Sunrise) + 🛕 (Temple): Represents 'Varisu', family drama.",
    "🏏🎯": "🏏 (Cricket) + 🎯 (Target): Refers to 'Kanaa', cricket sports drama."
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
