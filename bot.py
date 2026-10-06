import discord
from discord.ext import commands
import os

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot Ready: {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    print(f"{message.author}: {message.content}")
    await bot.process_commands(message)

# يقرا التوكن من الموقع، واذا ما حصله يقراه من token.txt عندك
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    with open("token.txt", "r", encoding="utf-8") as f:
        TOKEN = f.read().strip()

bot.run(TOKEN)