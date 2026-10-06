import discord
from discord.ext import commands
import random
from flask import Flask
from threading import Thread

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="-", intents=intents, help_command=None)

active_guess = {}
active_fakk = {}

# === HELP ===
class HelpSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="الادارة", emoji="🛡️"),
            discord.SelectOption(label="الالعاب", emoji="🎮"),
            discord.SelectOption(label="الكل", emoji="📜")
        ]
        super().__init__(placeholder="اختر قسم", options=options)
    async def callback(self, interaction):
        v = self.values[0]
        if v == "الادارة":
            txt = "`-ban` `-kick` `-clear` `-mute` `-lock`"
        elif v == "الالعاب":
            txt = "`-xo @شخص` `-خمن` `-روليت` `-rps` `-فكك` `-سؤال` `-عجلة`"
        else:
            txt = "`-help` وكل الاوامر"
        embed = discord.Embed(title=v, description=txt, color=0x2ecc71)
        await interaction.response.edit_message(embed=embed)

class HelpView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
        self.add_item(HelpSelect())

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="مركز المساعدة", description="اختر من القائمة", color=0x2ecc71)
    await ctx.send(embed=embed, view=HelpView())

# === العاب ===
@bot.command(aliases=["خمن"])
async def guess(ctx):
    active_guess[ctx.channel.id] = random.randint(1,100)
    await ctx.send(f"{ctx.author.mention} خمنت رقم 1-100")

@bot.command(aliases=["روليت"])
async def roulette(ctx):
    m = random.choice([x for x in ctx.guild.members if not x.bot])
    await ctx.send(f"🔫 الطلقة على {m.mention}")

@bot.command()
async def rps(ctx, c=None):
    await ctx.send(f"انت {c} | انا {random.choice(['حجر','ورقة','مقص'])}")

@bot.command(aliases=["فكك"])
async def fakk(ctx):
    w = random.choice(["سحابة","ديسكورد","بوت"])
    active_fakk[ctx.channel.id] = w
    await ctx.send(f"فكك: {''.join(random.sample(w,len(w)))}")

@bot.command(aliases=["سؤال"])
async def سوال(ctx):
    await ctx.send(random.choice(["عاصمة عمان؟","كم رجل للاخطبوط؟"]))

@bot.command(aliases=["عجلة"])
async def ajala(ctx):
    await ctx.send(f"ربحت {random.choice(['100','200','حظ اوفر'])}")

@bot.command(aliases=["xo"])
async def xogame(ctx, member: discord.Member=None):
    if not member: return await ctx.send("-xo @شخص")
    view = discord.ui.View()
    # لعبة xo المبسطة
    await ctx.send(f"XO: {ctx.author.mention} vs {member.mention} - قريبا الازرار الكاملة")

@bot.event
async def on_message(msg):
    if msg.channel.id in active_guess:
        try:
            if int(msg.content) == active_guess[msg.channel.id]:
                await msg.channel.send("صح! 🎉")
                del active_guess[msg.channel.id]
        except: pass
    await bot.process_commands(msg)

app = Flask("")
@app.route("/")
def home(): return "alive"
Thread(target=lambda: app.run(host="0.0.0.0", port=8080)).start()

bot.run("TOKEN_HERE")
