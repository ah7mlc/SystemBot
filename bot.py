import discord
from discord.ext import commands
import random
from flask import Flask
from threading import Thread
import os

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"✅ شغال باسم {bot.user}")
    await bot.change_presence(activity=discord.Game(name="!help | SystemBot"))

# ======== HELP الجديد ========
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="📜 أوامر SystemBot", description="البادئة: `!`", color=0x2ecc71)
    embed.add_field(name="🔹 عام", value="`ping` - البنق\n`هلا` - ترحيب\n`avatar` - صورتك\n`userinfo` - معلوماتك\n`serverinfo` - معلومات السيرفر\n`say` - يكرر كلامك", inline=False)
    embed.add_field(name="🔹 ادارة", value="`clear 10` - مسح رسائل\n`kick @عضو` - طرد\n`ban @عضو` - حظر", inline=False)
    embed.add_field(name="🔹 ترفيه", value="`نكتة` - نكتة عشوائية\n`حب @شخص @شخص` - نسبة حب\n`اقتباس` - حكمة", inline=False)
    embed.add_field(name="🔹 اسلامي", value="`اذكار`\n`قرآن`", inline=False)
    embed.set_footer(text=f"طلب بواسطة {ctx.author.name}")
    await ctx.send(embed=embed)

@bot.command()
async def ping(ctx):
    await ctx.send(f"🏓 Pong! {round(bot.latency*1000)}ms - البوت شغال تمام")

@bot.command()
async def هلا(ctx):
    await ctx.send(f"هلا والله {ctx.author.mention} 😍🔥")

@bot.command()
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"صورة {member.name}", color=0x3498db)
    embed.set_image(url=member.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"معلومات {member.display}", color=0x3498db)
    embed.add_field(name="ID", value=member.id)
    embed.add_field(name="دخل السيرفر", value=member.joined_at.strftime("%Y-%m-%d"))
    embed.set_thumbnail(url=member.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command()
async def serverinfo(ctx):
    g = ctx.guild
    embed = discord.Embed(title=g.name, color=0x9b59b6)
    embed.add_field(name="الأعضاء", value=g.member_count)
    embed.add_field(name="المالك", value=g.owner)
    embed.set_thumbnail(url=g.icon.url if g.icon else None)
    await ctx.send(embed=embed)

@bot.command()
async def say(ctx, *, text):
    await ctx.message.delete()
    await ctx.send(text)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 5):
    await ctx.channel.purge(limit=amount+1)
    await ctx.send(f"✅ تم مسح {amount} رسائل", delete_after=2)

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="بدون سبب"):
    await member.kick(reason=reason)
    await ctx.send(f"👢 تم طرد {member}")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="بدون سبب"):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 تم حظر {member}")

@bot.command(name="نكتة")
async def nokta(ctx):
    jokes = ["مرة واحد نام متأخر حلم انه متأخر 😂", "واحد غبي سألوه وش رايك بالتعليم عن بعد؟ قال عن قرب ما فهمت عشان افهم عن بعد 😂"]
    await ctx.send(random.choice(jokes))

@bot.command()
async def حب(ctx, m1: discord.Member, m2: discord.Member):
    await ctx.send(f"❤️ نسبة الحب بين {m1.mention} و {m2.mention} هي {random.randint(0,100)}%")

@bot.command()
async def اقتباس(ctx):
    quotes = ["لا تؤجل عمل اليوم الى الغد", "من جد وجد ومن زرع حصد", "الابتسامة صدقة"]
    await ctx.send(f"💡 {random.choice(quotes)}")

@bot.command()
async def اذكار(ctx):
    await ctx.send("🤲 سبحان الله، الحمد لله، لا إله إلا الله، الله أكبر")

@bot.command()
async def قرآن(ctx):
    await ctx.send("﴿ إِنَّ مَعَ الْعُسْرِ يُسْرًا ﴾ ❤️")

# ======== عشان Render ========
app = Flask('')
@app.route('/')
def home(): return "Bot is Online!"

def run(): app.run(host='0.0.0.0', port=8080)
Thread(target=run).start()

bot.run(os.getenv("TOKEN"))
