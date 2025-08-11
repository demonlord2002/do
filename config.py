# config.py
import os

# ==== BOT CONFIG ====
API_ID = int(os.getenv("API_ID", "23559126"))
API_HASH = os.getenv("API_HASH", "58347a441c011b1b9ee3367ea936dcc4")
BOT_TOKEN = os.getenv("BOT_TOKEN", "7607268654:AAGup94GSmRa3U_SQ604_2XgKOovWsueYsM")

# ==== MONGODB CONFIG ====
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://drdoom2003p:drdoom2003p@cluster0.fnhjrtn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DB_NAME = os.getenv("DB_NAME", "emoji_game")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "scores")

# ==== LINKS ====
OWNER_USER_ID = 8370703281
CHANNEL_LINK = os.getenv("CHANNEL_LINK", "https://t.me/FallenAngelsNetwork")
