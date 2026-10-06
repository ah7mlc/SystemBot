import discord
from discord.ext import commands
import os, datetime
from flask import Flask
from threading import Thread

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

def parse_time(s):
    try:
        u, n = s[-1], int(s[:-1])
        if u == "s": return datetime.timedelta(seconds=n)
        if u == "m": return datetime.timedelta(minutes=n)
        if u == "h": return datetime.timedelta(hours=n)
        if u == "d": return datetime.timedelta(days=n)
    except: return None

@bot.event
async def on_ready():
    print(f"✅ {bot.user} Online")

# k = kick / طرد
@bot.command(name="k")
@commands.has_permissions(kick_members=True)
async def k(ctx, member: discord.Member, *, reason="بدون سبب"):
    await member.kick(reason=reason)
    await ctx.send(f"👢 تم طرد {member.mention} | {reason}")

# b = ban / باند
@bot.command(name="b")
@commands.has_permissions(ban_members=True)
async def b(ctx, member: discord.Member, *, reason="بدون سبب"):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 تم باند {member} | {reason}")

# ub = unban
@bot.command(name="ub")
@commands.has_permissions(ban_members=True)
async def ub(ctx, user_id: int):
    user = await bot.fetch_user(user_id)
    await ctx.guild.unban(user)
    await ctx.send(f"✅ فك باند {user}")

# m = mute / t = timeout نفس الشي
@bot.command(name="m")
@commands.has_permissions(moderate_members=True)
async def m(ctx, member: discord.Member, time: str = "10m", *, reason="بدون سبب"):
    dur = parse_time(time)
    if not dur: return await ctx.send("❌ اكتب الوقت صح: `!m @عضو 10m` او `10s` `1h` `1d`")
    await member.timeout(dur, reason=reason)
    await ctx.send(f"🔇 {member.mention} ميوت لمدة {time} | {reason}")

@bot.command(name="t")
@commands.has_permissions(moderate_members=True)
async def t(ctx, member: discord.Member, time: str, *, reason="بدون سبب"):
    dur = parse_time(time)
    if not dur: return await ctx.send("❌ مثال: `!t @عضو 30m سبام`")
    await member.timeout(dur, reason=reason)
    await ctx.send(f"⏰ {member.mention} تايم {time} | {reason}")

# um = فك الميوت
@bot.command(name="um")
@commands.has_permissions(moderate_members=True)
async def um(ctx, member: discord.Member):
    await member.timeout(None)
    await ctx.send(f"✅ تم فك {member.mention}")

# c = مسح
@bot.command(name="c")
@commands.has_permissions(manage_messages=True)
async def c(ctx, amount: int = 5):
    await ctx.channel.purge(limit=amount+1)
    await ctx.send(f"🧹 مسح {amount}", delete_after=2)

@bot.command(name="help")
async def help_cmd(ctx):
    e = discord.Embed(title="⚙️ SystemBot - اختصارات", color=0x00ff88)
    e.add_field(name="الاوامر", value="`!k @عضو` طرد\n`!b @عضو` باند\n`!ub ID` فك باند\n`!m @عضو 10m` ميوت\n`!t @عضو 1h` تايم\n`!um @عضو` فك ميوت\n`!c 10` مسح", inline=False)
    await ctx.send(embed=e)

app = Flask('')
@app.route('/')
def home(): return "OK"
Thread(target=lambda: app.run(host='0.0.0.0',port=8080)).start()
bot.run(os.getenv("TOKEN"))
