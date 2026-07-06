import discord
from discord.ext import commands
import os
from threading import Thread
from flask import Flask

# --- 1. DEO: Flask Web Server (da bot radi 24/7 na Renderu) ---
app = Flask('')

@app.route('/')
def home():
    return "Glavni bot je ziv!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- 2. DEO: Konfiguracija Bota ---
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="t!", intents=intents)

@bot.event
async def on_ready():
    print(f'Ulogovan sam kao {bot.user}')
    # Ovde stoji tvoj custom status za server
    await bot.change_presence(activity=discord.Game(name="💚 Next Level Community 💚"))

# --- 3. DEO: Komande za slanje poruka preko bota ---

# Komanda za običnu poruku (t!say #kanal tekst)
@bot.command()
@commands.has_permissions(administrator=True)
async def say(ctx, channel: discord.TextChannel, *, poruka: str):
    await ctx.message.delete() # Briše tvoju t!say komandu iz četa da se ne vidi
    await channel.send(poruka)

# Komanda za lepu Embed poruku (t!say_embed #kanal Naslov | Tekst)
@bot.command()
@commands.has_permissions(administrator=True)
async def say_embed(ctx, channel: discord.TextChannel, *, tekst: str):
    await ctx.message.delete() # Briše tvoju komandu
    
    # Delimo naslov i tekst pomoću uspravne crte |
    if "|" in tekst:
        naslov, opis = tekst.split("|", 1)
    else:
        naslov = "Obaveštenje"
        opis = tekst
        
    embed = discord.Embed(
        title=naslov.strip(),
        description=opis.strip(),
        color=discord.Color.blue()
    )
    await channel.send(embed=embed)

# --- 4. DEO: Pokretanje ---
keep_alive()
token = os.environ.get("DISCORD_TOKEN")
bot.run(token)
