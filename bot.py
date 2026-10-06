import discord, os, datetime
from discord.ext import commands
from flask import Flask
from threading import Thread

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None, case_insensitive=True)

def parse_time(s):
    try:
        u, n = s[-1].lower(), int(s[:-1])
        if u == "s": return datetime.timedelta(seconds=n)
        if u == "m": return datetime.timedelta(minutes=n)
        if u == "h": return datetime.timedelta(hours=n)
        if u == "d": return datetime.timedelta(days=n)
    except: return None

@bot.event
async def on_ready():
    print(f"✅ {bot.user}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MemberNotFound):
        await ctx.send("❌ ما لقيت العضو! سوي منشن صح: `!k @العضو` اضغط @ واختاره من القائمة")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ ما عندك صلاحية")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ الاستخدام: `!{ctx.command} @عضو`")
    else:
        await ctx.send(f"❌ خطأ: {error}")
        print(error)

@bot.command(name="k")
@commands.has_permissions(kick_members=True)
async def k_cmd(ctx, member: discord.Member, *, reason="بدون سبب"):
    if member == ctx.author: return await ctx.send("❌ ما تقدر تطرد نفسك")
    if member.top_role >= ctx.guild.me.top_role: return await ctx.send("❌ رتبة البوت اقل من العضو! ارفع رتبة البوت فوق")
    await member.kick(reason=reason)
    await ctx.send(f"👢 تم طرد {member.mention}")

@bot.command(name="b")
@commands.has_permissions(ban_members=True)
async def b_cmd(ctx, member: discord.Member, *, reason="بدون سبب"):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 باند {member.mention}")

@bot.command(name="m")
@commands.has_permissions(moderate_members=True)
async def m_cmd(ctx, member: discord.Member, time: str = "10m", *, reason="بدون"):
    dur = parse_time(time)
    if not dur: return await ctx.send("❌ الوقت: `!m @عضو 10m`")
    await member.timeout(dur, reason=reason)
    await ctx.send(f"🔇 ميوت {member.mention} {time}")

@bot.command(name="t")
@commands.has_permissions(moderate_members=True)
async def t_cmd(ctx, member: discord.Member, time: str, *, reason="بدون"):
    dur = parse_time(time)
    await member.timeout(dur, reason=reason)
    await ctx.send(f"⏰ تايم {member.mention} {time}")

@bot.command(name="um")
@commands.has_permissions(moderate_members=True)
async def um_cmd(ctx, member: discord.Member):
    await member.timeout(None)
    await ctx.send(f"✅ فك {member.mention}")

@bot.command(name="help")
async def help_cmd(ctx):
    await ctx.send("`!k @عضو` طرد\n`!b @عضو` باند\n`!m @عضو 10m` ميوت\n`!t @عضو 1h` تايم")

app = Flask('')
@app.route('/')
def home(): return "OK"
Thread(target=lambda: app.run(host='0.0.0.0',port=8080)).start()
bot.run(os.getenv("DISCORD_TOKEN") or os.getenv("TOKEN"))
