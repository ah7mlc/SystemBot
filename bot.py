from flask import Flask
import threading
import discord
from discord.ext import commands
import os

app = Flask(__name__)
@app.route('/')
def home(): 
    return "Bot is Alive!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_web).start()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot Ready: {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong! 🏓 البوت شغال تمام")

@bot.command()
async def هلا(ctx):
    await ctx.send(f"هلا والله {ctx.author.mention} 👋")

@bot.event
async def on_message(message):
    if message.author.bot: 
        return
    await bot.process_commands(message)

# هذا السطر هو المهم - يقرأ من أي اسم
TOKEN = os.getenv("DISCORD_TOKEN") or os.getenv("TOKEN")

if not TOKEN:
    print("ERROR: ما لقيت التوكن! تأكد انك حاط DISCORD_TOKEN في Render")
else:
    bot.run(TOKEN)
