import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="-", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("شغال!")

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="مركز المساعدة", description="-ping\n-help\nقريبا نضيف الالعاب", color=0x2ecc71)
    await ctx.send(embed=embed)

bot.run(os.environ["DISCORD_TOKEN"])
