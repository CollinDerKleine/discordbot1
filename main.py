import discord
from discord.ext import commands
from discord import app_commands
from flask import Flask
from threading import Thread
import os
from dotenv import load_dotenv
from tabulate import tabulate
from prettytable import PrettyTable

Tasks=[]

user_points={}

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

@bot.tree.command(name="create_task", description="Create a task")
@app_commands.describe(task="Task name", points="Points for the task", role="Role required for the task")
async def create_task(interaction: discord.Interaction, task: str, points: int, role: discord.Role):
    if any(role.name == "ADMIN" for role in interaction.user.roles):
        await interaction.response.send_message(f"Task '{task}' created with {points} points and role {role.name} required.")
        try:
            Id=Tasks[-1][3]+1
        except:
            Id=1
    else:
        await interaction.response.send_message("You can only do this as an Admin")    
    Tasks.append([task, points, role.name, Id, "Not Started"])
@bot.tree.command(name="show_tasks", description="Show All Tasks")
async def show_task(interaction: discord.Interaction):
    embed = discord.Embed(title="📋 Task List", color=discord.Color.blue())

    for task in Tasks:
        embed.add_field(
            name=f"📝 {task[0]} (ID: {task[4]})",
            value=f"**Points:** {task[1]}\n**Status:** {task[2]}\n**Role Required:** {task[3]}",
            inline=False
        )

    await interaction.response.send_message(embed=embed)
@bot.tree.command(name="delete_task", description="Delete an Task")
async def deltask(interaction: discord.Interaction, task_id:int):
    if any(role.name == "ADMIN" for role in interaction.user.roles):
        for index,y in enumerate(Tasks):
            if task_id==y[3]:
                Task_found=True
            if Task_found:
                del Tasks[index]
                await interaction.response.send_message(f"Task {Tasks[index]} has been deleted")
                Task_found=False
        else:
            await interaction.response.send_message("This Task Id does note exist. Please check with /show_tasks the id of your task")
    else:
        interaction.response.send_message("You have too be an admin to do this")



@bot.tree.command(name="help_task", description="Contribute to an Task")
async def help_task(interaction: discord.Interaction, task_id:int):
    for index,y in enumerate(Tasks):
        if task_id==y[3]:
            Task_found=True
            Task_Help=index
        if Task_found:
            Tasks[Task_Help][4]=f"Contribute by: {interaction.user}"
            await interaction.response.send_message(f"Task {Tasks[Task_Help][0]} will be done by {interaction.user}")
            Task_found=False
        else:
            await interaction.response.send_message("This Task Id does note exist. Please check with /show_tasks the id of your task")
@bot.tree.command(name="done", description="Done with a Task")
async def done(interaction: discord.Interaction, task_id: int):
    task_found = False
    task_Help = None

    for index, y in enumerate(Tasks):
        if task_id == y[3]:
            task_found = True
            task_Help = index
            break  

    if task_found:
        if f"Contribute by: {interaction.user}" != Tasks[task_Help][4]:
            await interaction.response.send_message("You can't complete a task you haven't contributed to, please always mark to what task you are contributing!", ephemeral=True)
            return
        
        Tasks[task_Help][4] = f"Done by: {interaction.user}"
            
        if interaction.user.id in user_points:
            user_points[interaction.user.id] += Tasks[task_Help][1]
        else:
            user_points[interaction.user.id] = Tasks[task_Help][1]

        await interaction.response.send_message(
            f"Task {Tasks[task_Help][0]} has been done by {interaction.user}. "
            f"{Tasks[task_Help][1]} points have been added to the account of {interaction.user}, "
            f"who now has {user_points[interaction.user.id]} points."
        )
    else:
        await interaction.response.send_message(
            "This Task ID does not exist. Please check with /show_tasks the ID of your task."
        )
    
@bot.tree.command(name="get_points", description="Get Points of an User")
async def getpoints(interaction: discord.Interaction,user: discord.User):
    await interaction.response.send_message(f"This User has {user_points[user.id]} Points")

@bot.tree.command(name="set_points", description="Add Points to a user")
async def addpoints(interaction: discord.Interaction, points: int, user: discord.User):
    if any(role.name == "ADMIN" for role in interaction.user.roles):
        try:
            user_points[user.id] += points
        except:
            user_points[user.id]  = points
        await interaction.response.send_message("Done")    
    else:
        await interaction.response.send_message(f"You have to be an admin to do this.")

@bot.tree.command(name="pay_points", description="Transfer Points to an User")
async def paypoints(interaction: discord.Interaction, user:discord.User, points: int):
    if user_points[interaction.user.id] >= points:
        user_points[interaction.user.id] -= points
        user_points[user.id] += points
        await interaction.response.send_message(f"Trasnfered {points} from {interaction.user}, who now has {user_points[interaction.user.id]}, to {user}, who now has {user_points[user.id]}.")
    else:
        await interaction.response.send_message("You dont have enough Points for that")





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
