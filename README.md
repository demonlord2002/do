# 🎬 Guess the Emoji — Tamil Movie Bot 🇮🇳

**A fun, fast-paced Telegram game bot** where players guess Tamil movies based on emoji clues!  
Perfect for groups, families, and friends who love cinema. 🎭

---

## 🚀 Deploy Your Own Bot

Click the button below to deploy this bot to **Heroku** instantly:

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://www.heroku.com/deploy?template=https://github.com/demonlord2002/do)

---

## 🎯 Game Features

✅  **Tamil Movies Only** — specially curated movie list with emojis  
✅  **Multiple Choice** — 4 options per question (1 correct, 3 random)  
✅  **Score Tracking** — keeps track of each player’s points via MongoDB  
✅  **First Correct Wins** — once a player guesses correctly, the round ends  
✅  **No Spam** — each user can answer only once per round  
✅  **Group Friendly** — designed for Telegram groups

---

## 📜 How to Play

1. **Add the bot** to your Telegram group  
2. Type `/emoji` — the bot will send an emoji clue + answer buttons  
3. Tap the answer you think is correct  
4. First player to guess right wins 1 point  
5. Use `/myscore` to check your score

---

## 🔧 Commands

| Command         | Description                                   |
|-----------------|-----------------------------------------------|
| `/start`        | Start the bot / get instructions              |
| `/emoji`        | Send a new emoji movie question               |
| `/myscore`      | Show your current points                      |

---

## 🛠 Requirements

- Python 3.9+  
- MongoDB Atlas connection string  
- Telegram Bot API Token  
- Heroku account (for free hosting)

---

## ⚙ Environment Variables

These must be set in **Heroku Config Vars**:

| Variable         | Description |
|------------------|-------------|
| `API_ID`         | Your Telegram API ID from my.telegram.org |
| `API_HASH`       | Your Telegram API Hash from my.telegram.org |
| `BOT_TOKEN`      | Bot token from @BotFather |
| `MONGO_URI`      | MongoDB connection string |
| `DB_NAME`        | Database name (e.g., `emoji_game`) |
| `COLLECTION_NAME`| Collection name (e.g., `scores`) |
| `OWNER_LINK`     | Your Telegram profile link |
| `CHANNEL_LINK`   | Your updates channel link |

---

## 📂 Project Structure

