import discord
from discord.ext import commands
import random
import datetime

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ البوت شغال باسم {bot.user}")
    await bot.change_presence(activity=discord.Game(name="!help | SystemBot"))

# ========= عام =========
@bot.command()
async def ping(ctx):
    await ctx.send(f"🏓 البنق: {round(bot.latency*1000)}ms")

@bot.command()
async def هلا(ctx):
    await ctx.send(f"هلا والله {ctx.author.mention} 😍")

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="📜 أوامر SystemBot", color=0x00ff00)
    embed.add_field(name="🔹 عام", value="`!ping`, `!هلا`, `!avatar`, `!userinfo`, `!serverinfo`, `!say`", inline=False)
    embed.add_field(name="🔹 ادارة", value="`!clear`, `!kick`, `!ban`, `!unban`", inline=False)
    embed.add_field(name="🔹 ترفيه", value="`!نكتة`, `!ميم`, `!حب`, `!اقتباس`", inline=False)
    embed.add_field(name="🔹 اسلامي", value="`!اذكار`, `!قرآن`", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"صورة {member.name}")
    embed.set_image(url=member.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"معلومات {member.name}", color=0x3498db)
    embed.add_field(name="دخل السيرفر", value=member.joined_at.strftime("%Y-%m-%d"))
    embed.add_field(name="الحساب انشئ", value=member.created_at.strftime("%Y-%m-%d"))
    embed.set_thumbnail(url=member.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild
    embed = discord.Embed(title=guild.name, color=0x9b59b6)
    embed.add_field(name="الأعضاء", value=guild.member_count)
    embed.add_field(name="تاريخ الانشاء", value=guild.created_at.strftime("%Y-%m-%d"))
    embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
    await ctx.send(embed=embed)

@bot.command()
async def say(ctx, *, text):
    await ctx.message.delete()
    await ctx.send(text)

# ========= ادارة =========
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 5):
    await ctx.channel.purge(limit=amount+1)
    await ctx.send(f"✅ تم مسح {amount} رسائل", delete_after=3)

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="بدون سبب"):
    await member.kick(reason=reason)
    await ctx.send(f"👢 تم طرد {member.name}")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="بدون سبب"):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 تم حظر {member.name}")

# ========= ترفيه =========
@bot.command(name="نكتة")
async def نكتة(ctx):
    jokes = ["مرة واحد نام متأخر، حلم انه متأخر 😂", "واحد غبي سألوه ايش رأيك بالتعليم عن بعد؟ قال التعليم عن قرب ما فهمت عشان افهم عن بعد 😂"]
    await ctx.send(random.choice(jokes))

@bot.command()
async def ميم(ctx):
    await ctx.send("😂 ميم اليوم: البوت ما ينام وانت تنام!")

@bot.command()
async def حب(ctx, m1: discord.Member, m2: discord.Member):
    percent = random.randint(0,100)
    await ctx.send(f"❤️ نسبة الحب بين {m1.mention} و {m2.mention} هي {percent}%")

@bot.command()
async def اقتباس(ctx):
    quotes = ["لا تؤجل عمل اليوم الى الغد", "من جد وجد", "الابتسامة صدقة"]
    await ctx.send(f"💡 {random.choice(quotes)}")

# ========= اسلامي =========
@bot.command()
async def اذكار(ctx):
    await ctx.send("🤲 سبحان الله، الحمدلله، لا اله الا الله، الله اكبر")

@bot.command()
async def قرآن(ctx):
    await ctx.send("﴿ إِنَّ مَعَ الْعُسْرِ يُسْرًا ﴾")

# ========= ويب سيرفر عشان Render ما ينام =========
from flask import Flask
from threading import Thread

app = Flask('')
@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run).start()

import os
bot.run(os.getenv("TOKEN"))
