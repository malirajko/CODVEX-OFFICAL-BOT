import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread

# ==========================================
# 1. FLASK SERVER ZA KEEP-ALIVE (UptimeRobot)
# ==========================================
app = Flask('')

@app.route('/')
def home():
    return "Glavni bot je ziv!"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

# ==========================================
# 2. INICIJALIZACIJA BOTA I GAŠENJE DEFAULT HELP-A
# ==========================================
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="t!", intents=intents)
bot.remove_command('help')  # Isključujemo fabrički help da bismo ubacili naš

# ==========================================
# 3. DOGAĐAJI (EVENTS) + CUSTOM STATUS
# ==========================================
@bot.event
async def on_ready():
    print(f'Glavni bot je spreman i online!')
    # Postavljanje traženog custom statusa
    await bot.change_presence(activity=discord.CustomActivity(name="Za Pomoc: t!help"))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error

# ==========================================
# 4. BOT KOMANDE
# ==========================================

# ➡️ KOMANDA: t!help
@bot.command(name="help")
async def main_help(ctx):
    opis_poruke = (
        "<:arrow_join6:1516798345568456714> Osnovni podaci servera:\n"
        "- __Server je napravljen 08/11/2025 sa zeljom da pomogne i poboljsa svim SAMP igracima dozivljaj same igrice.__\n\n"
        "<:arrow_join6:1516798345568456714> O cemu je nas server tacno?\n"
        "- __Next Level Community se zasniva iskljucivo o SAMP igrici, to znaci da ovde kacimo modpackove,modove i sve ostalo vezano za samp, "
        "Nasa zajednica je napravila kanal https://discord.com/channels/1404528302559068200/1448049898036658306 sa najcescim pitanjima vezano za modpackove, "
        "takodje pomoc administracije i drugih clanova oko crash-a,modpack-a i ostalo je 24/7 i uvek spremna.__\n\n"
        "<:arrow_join6:1516798345568456714> __Da li su modpackovi 100% original,bez virusa i slicno?\n"
        "Da, svaki modpack ili bilo sta drugo je cisto bez virusa i ostalo, takodje svaki modpack je detaljno radjen i 100% original.__\n\n"
        "<:arrow_join6:1516798345568456714> **__Vas Next Level Community__**"
    )
    
    embed = discord.Embed(
        title="<:arrow_join6:1516798345568456714>**__ Next Level Community Help Bot__**",
        description=opis_poruke,
        color=0x7ED321
    )
    await ctx.send(embed=embed)


# ➡️ KOMANDA: t!say (Slanje obične poruke preko bota)
@bot.command(name="say")
@commands.has_permissions(administrator=True)
async def say(ctx, kanal: discord.TextChannel, *, poruka: str):
    await ctx.message.delete()  # Briše tvoju komandu iz chata
    await kanal.send(poruka)


# ➡️ KOMANDA: t!esay (Slanje EMBED poruke preko bota sa zelenom bojom)
@bot.command(name="esay")
@commands.has_permissions(administrator=True)
async def esay(ctx, kanal: discord.TextChannel, *, poruka: str):
    await ctx.message.delete()  # Briše tvoju komandu iz chata
    
    # Pravimo embed sa istom zelenom bojom #7ED321
    embed = discord.Embed(
        description=poruka,
        color=0x7ED321
    )
    await kanal.send(embed=embed)


# Error handler za obe say komande ako zaboraviš parametre
@say.error
@esay.error
async def say_error_handler(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ **Greška!** Pravilan unos je:\n`t!say #kanal Tekst` za običnu poruku\n`t!esay #kanal Tekst` za Embed poruku", delete_after=7)

# ==========================================
# 5. POKRETANJE BOTA
# ==========================================
keep_alive()
token = os.environ.get("DISCORD_TOKEN")
bot.run(token)
