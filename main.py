
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
# 2. INICIJALIZACIJA BOTA I UKLJUČIVANJE INTENTS-A
# ==========================================
# Promenjeno u intents.all() da bi bot mogao da vidi nove članove (guild_members)
intents = discord.Intents.all()

bot = commands.Bot(command_prefix="t!", intents=intents)
bot.remove_command('help')  # Isključujemo fabrički help da bismo ubacili naš

# ==========================================
# CONFIG: ID-EVI KANALA (Zameni sa svojim ID-evima)
# ==========================================
WELCOME_CHANNEL_ID = 1515699310501560420    # ID kanala gde stiže dobrodošlica
PRAVILA_CHANNEL_ID = 1404528872103350292    # ID kanala za pravila
BAZAAR_CHANNEL_ID =  1527277236938604554     # ID kanala za pijacu/bazaar
PRIJAVE_CHANNEL_ID = 1523627320852873348    # ID kanala za staff prijave

# ==========================================
# 3. DOGAĐAJI (EVENTS) + CUSTOM STATUS
# ==========================================
@bot.event
async def on_ready():
    print(f'Glavni bot je spreman i online!')
    await bot.change_presence(activity=discord.CustomActivity(name="Za Pomoc: t!help"))

# NOVI DOGAĐAJ: Automatska dobrodošlica kada neko uđe na server
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1515699310501560420)
    if channel is None:
        return

    # Uzimamo ukupan broj članova na serveru
    member_count = member.guild.memberCount

    # Pravimo tekst za dobrodošlicu sa tvojim razmakom i formatom
    opis_poruke = (
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"👋 × **Ćao, {member.mention}!** Dobrodošao u našu zvaničnu zajednicu! Drago nam je što si postao deo **NEXT LEVEL** priče. Pre nego što kreneš sa blejom, baci pogled na par ključnih stvari:\n\n"
        f"📜 × **PRAVILA SERVERA:** Da ne bi dolazilo do nesporazuma i kazni, obavezno pročitaj pravila u kanalu <#{1515699310501560420}>.\n\n"
        f"🛒 × **SAMP BAZAAR:** Ako igraš SAMP, u kanalu <#{1527277236938604554}> možeš pratiti najnovije oglase, kupovati i prodavati imovinu ili pokrenuti aukciju preko našeg bota!\n\n"
        f"👑 × **STAFF PRIJAVE:** Želiš da pomogneš zajednici i postaneš deo naše administracije? Konkuriši i otvori prijavu u kanalu <#{1523627320852873348}>.\n\n"
        f"✨ × **BUDI AKTIVAN:** Piši u glavnom chatu, koristi bot komande, skupljaj poene i otključaj custom uloge i fensi boje za ime!\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🏟️ × **Uživaj u boravku i budi spreman za sve što dolazi!**"
    )

    # Pravimo Embed karticu (koristimo tvoju zelenu boju 0x7ED321)
    embed = discord.Embed(
        description=opis_poruke,
        color=0x7ED321
    )
    
    # Postavljanje naslova/autora na vrh kartice sa ikonicom servera
    if member.guild.icon:
        embed.set_author(name="NEXT LEVEL COMMUNITY — DOBRODOŠLICA", icon_url=member.guild.icon.url)
        embed.set_footer(text=f"Ti si naš #{member_count} član.", icon_url=member.guild.icon.url)
    else:
        embed.set_author(name="NEXT LEVEL COMMUNITY — DOBRODOŠLICA")
        embed.set_footer(text=f"Ti si naš #{member_count} član.")

    # Ovde stavi direktan link do tvoje slike vikinga sa desne strane
    embed.set_thumbnail(url="https://i.imgur.com/TvojVikinzimaSlikaLink.png")

    # Bot prvo pinguje člana iznad kartice (kao Carl-bot), pa šalje embed
    await channel.send(content=member.mention, embed=embed)


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
