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
    embed = discord.Embed(title="📜 مركز المساعدة - System Bot", color=0x2ecc71)
    embed.add_field(name="🛡️ الادارة", value="`ban` `kick` `clear`\n`lock` `unlock`", inline=True)
    embed.add_field(name="🎮 الالعاب", value="`xo @منشن` `rps`\n`8ball` `bola`", inline=True)
    embed.add_field(name="⚙️ عام", value="`ping` `help` `avatar`", inline=True)
    embed.set_footer(text="Prefix: - | System Bot")
    await ctx.send(embed=embed)

@bot.command()
async def bola(ctx):
    await ctx.send("لعبة bola قريبا!")

bot.run(os.environ["DISCORD_TOKEN"])
