import os
from dotenv import load_dotenv
from discord.ext import commands
from discord import Intents
from flask import Flask
import threading
import logging

# Lade Umgebungsvariablen aus der .env-Datei
load_dotenv()

# Setze den Logger
logging.basicConfig(level=logging.INFO)

# Erstelle Intents-Objekt (z.B. für das Überwachen von Nachrichten)
intents = Intents.default()
intents.messages = True  # Aktiviert das Nachrichten-Ereignis
intents.members = True   # Aktiviert das Mitglieder-Ereignis (falls benötigt)

# Initialisiere den Bot mit einem Präfix und den Intents
bot = commands.Bot(command_prefix="!", intents=intents)

# Event, das ausgeführt wird, wenn der Bot erfolgreich eingeloggt ist
@bot.event
async def on_ready():
    print(f'Bot ist eingeloggt als {bot.user}')
    # Hier kannst du weitere Initialisierungen hinzufügen, falls notwendig.

# Beispiel für einen einfachen Befehl
@bot.command()
async def hallo(ctx):
    await ctx.send("Hallo! Wie geht's?")

# Ein Beispiel für ein weiteres Kommando
@bot.command()
async def hilfe(ctx):
    await ctx.send("Verfügbare Befehle: !hallo, !hilfe")

# Überprüfe, ob der Bot Nachrichten korrekt verarbeitet
@bot.event
async def on_message(message):
    # Verhindern, dass der Bot auf seine eigenen Nachrichten reagiert
    if message.author == bot.user:
        return

    # Ausgabe, um zu sehen, ob Nachrichten empfangen werden
    print(f'Nachricht empfangen: {message.content}')

    # Verarbeitung von Befehlen sicherstellen
    await bot.process_commands(message)

# Flask-Webserver einrichten (falls du dies benötigst)
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
