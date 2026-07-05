import discord
from discord.ext import commands
import os
from threading import Thread
from flask import Flask

# --- 1. DEO: Trikovi za 24/7 rad (Flask Web Server) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot je ziv i zdrav!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- 2. DEO: Discord Bot Podešavanja ---
intents = discord.Intents.default()
intents.message_content = True 

bot = commands.Bot(command_prefix="!", intents=intents)

# Custom Status kada se bot upali
@bot.event
async def on_ready():
    print(f'Ulogovan sam kao {bot.user}')
    # Ovde menjaš šta piše botu u statusu!
    await bot.change_presence(activity=discord.Game(name="Blejim na serveru 24/7"))

# --- 3. DEO: Komande ---
@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! 🏓 Latencija je {round(bot.latency * 1000)}ms")

@bot.command()
async def zdravo(ctx):
    await ctx.send(f"Gde si {ctx.author.mention}! Šta ima?")

# --- 4. DEO: Pokretanje ---
keep_alive() 
bot.run(os.getenv('DISCORD_TOKEN'))
