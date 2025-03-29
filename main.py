import os
from dotenv import load_dotenv
from discord.ext import commands
from discord import Intents
import logging
from flask import Flask
import threading

# Lade Umgebungsvariablen aus der .env-Datei
load_dotenv()

# Setze den Logger
logging.basicConfig(level=logging.INFO)

# Erstelle Intents-Objekt
intents = Intents.default()
intents.messages = True  # Aktiviert Nachrichteninhalte
intents.members = True   # Aktiviert Mitgliederereignisse (optional, falls du Mitgliederinformationen benötigst)

# Initialisiere den Bot mit dem Präfix und den Intents
bot = commands.Bot(command_prefix="!", intents=intents)

# Event, das ausgeführt wird, wenn der Bot erfolgreich eingeloggt ist
@bot.event
async def on_ready():
    print(f'Bot ist eingeloggt als {bot.user}')

# Beispiel für einen einfachen Befehl
@bot.command()
async def hallo(ctx):
    await ctx.send("Hallo! Wie geht's?")

# Ein Beispiel für ein weiteres Kommando
@bot.command()
async def hilfe(ctx):
    await ctx.send("Verfügbare Befehle: !hallo, !hilfe")

# Flask-Webserver einrichten
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    app.run(host="0.0.0.0", port=5000)

# Funktion für den Flask-Server in einem eigenen Thread
flask_thread = threading.Thread(target=run_flask)
flask_thread.start()

# Den Bot mit dem Token starten
bot.run(os.getenv('DISCORD_TOKEN'))
