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
bot.remove_command('help')  # Force gašenje fabričkog help-a

# ==========================================
# 3. DOGAĐAJI (EVENTS) + CUSTOM STATUS
# ==========================================
@bot.event
async def on_ready():
    print(f'Glavni bot je spreman i online!')
    
    # OVDE JE TVOJ CUSTOM STATUS (Promeni tekst po zelji)
    await bot.change_presence(activity=discord.CustomActivity(name="Za Pomoc: t!help"))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error

# ==========================================
# 4. NOVA PRILAGOĐENA HELP KOMANDA U EMBEDU
# ==========================================
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

# ==========================================
# 5. POKRETANJE BOTA
# ==========================================
keep_alive()
token = os.environ.get("DISCORD_TOKEN")
bot.run(token)
