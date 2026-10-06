import discord, os, datetime
from discord.ext import commands
from flask import Flask
from threading import Thread

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="-", intents=intents, help_command=None, case_insensitive=True)

# --- تخزين التحذيرات في الذاكرة ---
warnings_db = {}

def parse_time(s):
    try:
        u, n = s[-1].lower(), int(s[:-1])
        if u == "s": return datetime.timedelta(seconds=n)
        if u == "m": return datetime.timedelta(minutes=n)
        if u == "h": return datetime.timedelta(hours=n)
        if u == "d": return datetime.timedelta(days=n)
    except: return None

async def send_log(guild, text):
    # يدور قناة اسمها logs او log
    ch = discord.utils.get(guild.text_channels, name="logs") or discord.utils.get(guild.text_channels, name="log")
    if ch:
        embed = discord.Embed(description=text, color=0x2b2d31, timestamp=datetime.datetime.now())
        await ch.send(embed=embed)

@bot.event
async def on_ready():
    print(f"✅ ONLINE: {bot.user}")

@bot.event
async def on_member_join(member):
    # ترحيب + اوتو رول
    ch = discord.utils.get(member.guild.text_channels, name="welcome") or discord.utils.get(member.guild.text_channels, name="general")
    if ch:
        await ch.send(f"👋 Welcome {member.mention} to **{member.guild.name}**!")

    # اوتو رول - يدور رتبة اسمها Member
    role = discord.utils.get(member.guild.roles, name="Member")
    if role:
        try: await member.add_roles(role)
        except: pass

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MemberNotFound):
        await ctx.send("❌ Member not found / العضو غير موجود")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ No permission / ما عندك صلاحية")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Usage / الاستخدام: `-{ctx.command} @member`")

# --- Moderation | الإدارة ---

@bot.command(name="kick")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason / بدون سبب"):
    if member.top_role >= ctx.guild.me.top_role: return await ctx.send("❌ My role lower / رتبتي اقل")
    await member.kick(reason=reason)
    await ctx.send(f"👢 Kicked / تم الطرد: {member.mention}")
    await send_log(ctx.guild, f"👢 **KICK** {member.mention} by {ctx.author.mention} | {reason}")

@bot.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason / بدون سبب"):
    if member.top_role >= ctx.guild.me.top_role: return await ctx.send("❌ My role lower / رتبتي اقل")
    await member.ban(reason=reason)
    await ctx.send(f"🔨 Banned / تم الباند: {member.mention}")
    await send_log(ctx.guild, f"🔨 **BAN** {member.mention} by {ctx.author.mention} | {reason}")

@bot.command(name="unban")
@commands.has_permissions(ban_members=True)
async def unban(ctx, user_id: int):
    user = await bot.fetch_user(user_id)
    await ctx.guild.unban(user)
    await ctx.send(f"✅ Unbanned / تم فك الباند: {user}")

@bot.command(name="mute")
@commands.has_permissions(moderate_members=True)
async def mute(ctx, member: discord.Member, time: str = "10m", *, reason="No reason"):
    dur = parse_time(time)
    if not dur: return await ctx.send("❌ Ex: `-mute @member 10m` (s/m/h/d)")
    await member.timeout(dur, reason=reason)
    await ctx.send(f"🔇 Muted / ميوت {member.mention} for {time}")
    await send_log(ctx.guild, f"🔇 **MUTE** {member.mention} for {time} by {ctx.author.mention}")

@bot.command(name="unmute")
@commands.has_permissions(moderate_members=True)
async def unmute(ctx, member: discord.Member):
    await member.timeout(None)
    await ctx.send(f"✅ Unmuted / فك الميوت {member.mention}")

@bot.command(name="clear")
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 10):
    await ctx.channel.purge(limit=amount+1)
    await ctx.send(f"🧹 Cleared / تم المسح {amount}", delete_after=3)

@bot.command(name="lock")
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 Locked / مقفل")

@bot.command(name="unlock")
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("🔓 Unlocked / مفتوح")

@bot.command(name="slowmode")
@commands.has_permissions(manage_channels=True)
async def slowmode(ctx, seconds: int = 0):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"⏱️ Slowmode / الوضع البطيء: {seconds}s")

# --- Warnings | التحذيرات ---

@bot.command(name="warn")
@commands.has_permissions(moderate_members=True)
async def warn(ctx, member: discord.Member, *, reason="No reason"):
    uid = str(member.id)
    if uid not in warnings_db: warnings_db[uid] = []
    warnings_db[uid].append({"reason": reason, "by": str(ctx.author), "time": str(datetime.datetime.now())})
    count = len(warnings_db[uid])
    await ctx.send(f"⚠️ Warned / تحذير {member.mention} | Warns: {count}/3 | Reason: {reason}")
    await send_log(ctx.guild, f"⚠️ **WARN** {member.mention} ({count}/3) by {ctx.author.mention} | {reason}")
    if count >= 3:
        await member.timeout(datetime.timedelta(hours=1), reason="3 Warns")
        await ctx.send(f"🔇 Auto Mute 1h for {member.mention} - Reached 3 warns / وصل 3 تحذيرات")

@bot.command(name="warnings")
async def warnings(ctx, member: discord.Member):
    uid = str(member.id)
    warns = warnings_db.get(uid, [])
    if not warns: return await ctx.send("✅ No warnings / لا يوجد تحذيرات")
    msg = "\n".join([f"{i+1}. {w['reason']} - by {w['by']}" for i,w in enumerate(warns)])
    await ctx.send(f"**Warnings for {member}:**\n{msg}")

@bot.command(name="clearwarn", aliases=["clearwarns"])
@commands.has_permissions(manage_messages=True)
async def clearwarn(ctx, member: discord.Member):
    warnings_db.pop(str(member.id), None)
    await ctx.send(f"✅ Cleared warns / تم مسح التحذيرات: {member.mention}")

# --- Info | معلومات ---

@bot.command(name="info")
async def info(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"{member.name}", color=0x2b2d31)
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Joined / دخل", value=discord.utils.format_dt(member.joined_at, style="R"), inline=True)
    embed.add_field(name="Top Role / اعلى رتبة", value=member.top_role.mention, inline=True)
    await ctx.send(embed=embed)

@bot.command(name="avatar", aliases=["av"])
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"{member.name} Avatar", color=0x2b2d31)
    embed.set_image(url=member.display_avatar.url)
    await ctx.send(embed=embed)

# --- HELP BILINGUAL ---

@bot.command(name="help")
async def help_cmd(ctx):
    embed = discord.Embed(title="🛡️ Bot Commands | أوامر البوت", description="Prefix: `-`", color=0x2b2d31)
    embed.add_field(name="-kick @member [reason]", value="Kick member | طرد عضو", inline=False)
    embed.add_field(name="-ban @member [reason]", value="Ban member | باند عضو", inline=False)
    embed.add_field(name="-unban ID", value="Unban by ID | فك الباند بالايدي", inline=False)
    embed.add_field(name="-mute @member [time] [reason]", value="Mute/Timeout | ميوت مثال: `-mute @m 10m`", inline=False)
    embed.add_field(name="-unmute @member", value="Remove mute | فك الميوت", inline=False)
    embed.add_field(name="-warn @member [reason]", value="Add warning | اضافة تحذير", inline=False)
    embed.add_field(name="-warnings @member", value="Show warnings | عرض التحذيرات", inline=False)
    embed.add_field(name="-clearwarn @member", value="Clear warnings | مسح التحذيرات", inline=False)
    embed.add_field(name="-clear [number]", value="Clear chat | مسح الشات", inline=False)
    embed.add_field(name="-lock / -unlock", value="Lock/Unlock channel | قفل/فتح القناة", inline=False)
    embed.add_field(name="-slowmode [seconds]", value="Slowmode | الوضع البطيء", inline=False)
    embed.add_field(name="-info [@member] / -avatar [@member]", value="Info & Avatar | معلومات وصورة العضو", inline=False)
    embed.add_field(name="Auto Features | الميزات التلقائية", value="✅ Welcome in #welcome | ترحيب\n✅ Auto Role: Member | رتبة تلقائية\n✅ Logs in #logs | سجل العقوبات", inline=False)
    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
    await ctx.send(embed=embed)

app = Flask('')
@app.route('/')
def home(): return "OK"
Thread(target=lambda: app.run(host='0.0.0.0',port=8080)).start()
bot.run(os.getenv("DISCORD_TOKEN") or os.getenv("TOKEN"))
