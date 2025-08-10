# config.py
import os

# ==== BOT CONFIG ====
API_ID = int(os.getenv("API_ID", "12345"))
API_HASH = os.getenv("API_HASH", "your_api_hash")
BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token")

# ==== MONGODB CONFIG ====
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://username:password@cluster0.mongodb.net/?retryWrites=true&w=majority")
DB_NAME = os.getenv("DB_NAME", "emoji_game")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "scores")

# ==== LINKS ====
OWNER_LINK = os.getenv("OWNER_LINK", "https://t.me/YourUsername")
CHANNEL_LINK = os.getenv("CHANNEL_LINK", "https://t.me/YourChannel")
