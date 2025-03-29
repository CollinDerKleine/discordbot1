import discord
from discord.ext import commands
from discord import app_commands
from flask import Flask
from threading import Thread
import os
from dotenv import load_dotenv

# Lade das Token aus der .env-Datei
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Flask Webserver Setup
app = Flask(__name__)

@app.route('/')
def home():
    return "Der Webserver läuft!"

def run_webserver():
    app.run(host="0.0.0.0", port=8000)

# Discord Bot Setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Slash Command mit einer Rolle als Argument
@bot.tree.command(name="create_task", description="Create a task")
@app_commands.describe(task="Task name", points="Points for the task", role="Role required for the task")
async def create_task(interaction: discord.Interaction, task: str, points: int, role: discord.Role):
    await interaction.response.send_message(f"Task '{task}' created with {points} points and role {role.name} required.")

# Der Bot registriert die Slash-Commands beim Start
@bot.event
async def on_ready():
    await bot.tree.sync()  # Synchronisiert die Slash-Commands mit Discord
    print(f'{bot.user} hat sich erfolgreich eingeloggt.')

# Bot Starten
def start_bot():
    bot.run(TOKEN)

# Beide Prozesse starten: Webserver und Bot
if __name__ == "__main__":
    # Webserver in einem separaten Thread starten
    web_thread = Thread(target=run_webserver)
    web_thread.start()

    # Bot starten
    start_bot()
