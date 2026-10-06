import discord, os, datetime
from discord.ext import commands
from flask import Flask
from threading import Thread

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="-", intents=intents, help_command=None, case_insensitive=True)

warnings_db = {}

def parse_time(s):
    try:
        u,n=s[-1].lower(),int(s[:-1])
        if u=="s": return datetime.timedelta(seconds=n)
        if u=="m": return datetime.timedelta(minutes=n)
        if u=="h": return datetime.timedelta(hours=n)
        if u=="d": return datetime.timedelta(days=n)
    except: return None

@bot.event
async def on_ready():
    print(f"✅ ONLINE: {bot.user}")

@bot.command(name="help")
async def help_cmd(ctx):
    embed = discord.Embed(title="🛡️ Bot Commands | أوامر البوت", description="Prefix: `-`", color=0x2b2d31)
    embed.add_field(name="-kick @member [reason]", value="طرد عضو / Kick", inline=False)
    embed.add_field(name="-ban @member [reason]", value="باند عضو / Ban", inline=False)
    embed.add_field(name="-unban ID", value="فك الباند / Unban", inline=False)
    embed.add_field(name="-mute @member 10m", value="ميوت / Mute", inline=False)
    embed.add_field(name="-unmute @member", value="فك الميوت / Unmute", inline=False)
    embed.add_field(name="-warn / -warnings / -clearwarn @member", value="نظام التحذيرات / Warn system", inline=False)
    embed.add_field(name="-clear [num] / -lock / -unlock / -slowmode", value="ادارة الشات / Chat manage", inline=False)
    embed.add_field(name="-info / -avatar @member", value="معلومات العضو / Member info", inline=False)
    embed.set_footer(text=f"Requested by {ctx.author}")
    await ctx.send(embed=embed)

# باقي اوامرك نفسها (اختصرتهم عشان لا يتكرر)
@bot.command(name="kick")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason"): await member.kick(reason=reason); await ctx.send(f"Kicked {member.mention}")
@bot.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason"): await member.ban(reason=reason); await ctx.send(f"Banned {member.mention}")
@bot.command(name="unban")
@commands.has_permissions(ban_members=True)
async def unban(ctx, user_id: int): user=await bot.fetch_user(user_id); await ctx.guild.unban(user); await ctx.send(f"Unbanned {user}")
@bot.command(name="mute")
@commands.has_permissions(moderate_members=True)
async def mute(ctx, member: discord.Member, time: str="10m", *, reason="No reason"): await member.timeout(parse_time(time), reason=reason); await ctx.send(f"Muted {member.mention} {time}")
@bot.command(name="unmute")
@commands.has_permissions(moderate_members=True)
async def unmute(ctx, member: discord.Member): await member.timeout(None); await ctx.send(f"Unmuted {member.mention}")
@bot.command(name="clear")
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int=10): await ctx.channel.purge(limit=amount+1); await ctx.send(f"Cleared {amount}", delete_after=2)
@bot.command(name="lock")
@commands.has_permissions(manage_channels=True)
async def lock(ctx): await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False); await ctx.send("🔒 Locked")
@bot.command(name="unlock")
@commands.has_permissions(manage_channels=True)
async def unlock(ctx): await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True); await ctx.send("🔓 Unlocked")

app = Flask('')
@app.route('/')
def home(): return "OK"
Thread(target=lambda: app.run(host='0.0.0.0',port=8080)).start()
bot.run(os.getenv("DISCORD_TOKEN") or os.getenv("TOKEN"))
