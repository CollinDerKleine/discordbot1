import os
from dotenv import load_dotenv
from discord.ext import commands
from flask import Flask
import threading
import logging


load_dotenv()

logging.basicConfig(level=logging.INFO)

bot = commands.Bot(command_prefix="!")


@bot.event
async def on_ready():
    print(f'Bot ist eingeloggt als {bot.user}')


@bot.command()
async def hallo(ctx):
    await ctx.send("Hallo! Wie geht's?")


@bot.command()
async def hilfe(ctx):
    await ctx.send("Verfügbare Befehle: !hallo, !hilfe")


app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    app.run(host="0.0.0.0", port=5000)

flask_thread = threading.Thread(target=run_flask)
flask_thread.start()

bot.run(os.getenv('DISCORD_TOKEN'))
