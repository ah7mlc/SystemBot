from flask import Flask
import threading
import discord
from discord.ext import commands
import os

app = Flask('')
@app.route('/')
def home(): return "Bot is Alive!"
threading.Thread(target=lambda: app.run(host='0.0.0.0', port=10000)).start()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot Ready: {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot: return
    print(f"{message.author}: {message.content}")
    await bot.process_commands(message)

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    with open("token.txt", "r", encoding="utf-8") as f:
        TOKEN = f.read().strip()
bot.run(TOKEN)
