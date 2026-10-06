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
    print(f"✅ ONLINE: {bot.user}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MemberNotFound):
        await ctx.send("❌ Member not found. Mention correctly: `!ban @member`")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You don't have permission")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Missing argument: `!{ctx.command} @member`")

@bot.command(name="kick")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason"):
    if member.top_role >= ctx.guild.me.top_role:
        return await ctx.send("❌ My role is lower than this member. Move my role up!")
    await member.kick(reason=reason)
    await ctx.send(f"👢 Kicked {member.mention} | Reason: {reason}")

@bot.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason"):
    if member.top_role >= ctx.guild.me.top_role:
        return await ctx.send("❌ My role is lower than this member.")
    await member.ban(reason=reason)
    await ctx.send(f"🔨 Banned {member.mention} | Reason: {reason}")

@bot.command(name="unban")
@commands.has_permissions(ban_members=True)
async def unban(ctx, user_id: int):
    user = await bot.fetch_user(user_id)
    await ctx.guild.unban(user)
    await ctx.send(f"✅ Unbanned {user} | ID: {user_id}")

@bot.command(name="mute")
@commands.has_permissions(moderate_members=True)
async def mute(ctx, member: discord.Member, time: str = "10m", *, reason="No reason"):
    dur = parse_time(time)
    if not dur: return await ctx.send("❌ Example: `!mute @member 10m` - Use s/m/h/d")
    await member.timeout(dur, reason=reason)
    await ctx.send(f"🔇 Muted {member.mention} for {time} | Reason: {reason}")

@bot.command(name="unmute")
@commands.has_permissions(moderate_members=True)
async def unmute(ctx, member: discord.Member):
    await member.timeout(None)
    await ctx.send(f"✅ Unmuted {member.mention}")

@bot.command(name="clear")
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 10):
    await ctx.channel.purge(limit=amount+1)
    await ctx.send(f"🧹 Cleared {amount} messages", delete_after=3)

@bot.command(name="lock")
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 Channel locked")

@bot.command(name="unlock")
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("🔓 Channel unlocked")

@bot.command(name="info")
async def info(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"{member.name} Info", color=0x2b2d31)
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="Mention", value=member.mention, inline=True)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Joined", value=discord.utils.format_dt(member.joined_at, style="R"), inline=True)
    embed.add_field(name="Top Role", value=member.top_role.mention, inline=True)
    await ctx.send(embed=embed)

@bot.command(name="help")
async def help_cmd(ctx):
    embed = discord.Embed(title="🛡️ Moderation Bot - Commands", color=0x2b2d31, description="Prefix: `!`")
    embed.add_field(name="👢!kick @member [reason]", value="Kick a member", inline=False)
    embed.add_field(name="🔨!ban @member [reason]", value="Ban a member", inline=False)
    embed.add_field(name="✅!unban ID", value="Unban by User ID. Ex: `!unban 123456789`", inline=False)
    embed.add_field(name="🔇!mute @member [time] [reason]", value="Timeout. Ex: `!mute @member 10m spam` (s/m/h/d)", inline=False)
    embed.add_field(name="🔊!unmute @member", value="Remove timeout", inline=False)
    embed.add_field(name="🧹!clear [amount]", value="Clear messages. Ex: `!clear 20`", inline=False)
    embed.add_field(name="🔒!lock /!unlock", value="Lock / Unlock channel", inline=False)
    embed.add_field(name="ℹ️!info [@member]", value="Show member info", inline=False)
    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
    await ctx.send(embed=embed)

app = Flask('')
@app.route('/')
def home(): return "Bot is Online"
Thread(target=lambda: app.run(host='0.0.0.0',port=8080)).start()

bot.run(os.getenv("DISCORD_TOKEN") or os.getenv("TOKEN"))
