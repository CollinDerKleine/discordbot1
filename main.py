import discord
from discord.ext import commands
from discord import app_commands
from flask import Flask
from threading import Thread
import os
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


app = Flask(__name__)

@app.route('/')
def home():
    return "Der Webserver läuft!"

def run_webserver():
    app.run(host="0.0.0.0", port=8000)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.tree.command(name="create_task", description="create an task")
async def ping(interaction: discord.Interaction, task: str, points: int, Role_Needed: discord.Role):
    await interaction.response.send_message("Pong!")


@bot.event
async def on_ready():
    await bot.tree.sync() 
    print(f'{bot.user} hat sich erfolgreich eingeloggt.')


def start_bot():
    bot.run(TOKEN)


if __name__ == "__main__":
    
    web_thread = Thread(target=run_webserver)
    web_thread.start()

    
    start_bot()
