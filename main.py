import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response
from flask import Flask
import threading

# Flask setup for health check
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!", 200

def run_flask():
    app.run(host="0.0.0.0", port=8000)

# Start Flask in a separate thread
threading.Thread(target=run_flask, daemon=True).start()

# Load token from .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Setup for the bot
intents = Intents.default()
intents.message_content = True
client = Client(intents=intents)

# Handle message responses
async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('(Message was empty)')
        return
    is_private = user_message[0] == '?'                                                 
    if is_private:
        user_message = user_message[1:]
    try:
        response = get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

# Event: Bot is ready
@client.event
async def on_ready():
    print(f'{client.user} is running!')

# Event: On message
@client.event
async def on_message(message: Message):
    if message.author == client.user:
        return
    user_message = str(message.content)
    print(f'[{message.channel}] {message.author}: "{user_message}"')
    await send_message(message, user_message)

# Run the bot
def main():
    client.run(TOKEN)

if __name__ == '__main__':
    main()
