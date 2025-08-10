# config.py
import os

# ==== BOT CONFIG ====
API_ID = int(os.getenv("API_ID", "23559126"))
API_HASH = os.getenv("API_HASH", "58347a441c011b1b9ee3367ea936dcc4")
BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token")

# ==== MONGODB CONFIG ====
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://drdoom2003p:drdoom2003p@cluster0.fnhjrtn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DB_NAME = os.getenv("DB_NAME", "emoji_game")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "scores")

# ==== LINKS ====
OWNER_LINK = os.getenv("OWNER_LINK", "https://t.me/SunsetOfMe")
CHANNEL_LINK = os.getenv("CHANNEL_LINK", "https://t.me/Cursed_Intelligence")
