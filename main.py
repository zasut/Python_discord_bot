import discord 
import os
from dotenv import load_dotenv
from discord import app_commands
from enum import Enum
import json
import random

with open("due_dates.json", "r") as file:
    due_dates = json.load(file)

with open("important_dates.json", "r") as file:
    important_dates = json.load(file)

with open ("commands.json", "r") as file:
    commands_info = json.load(file)

load_dotenv()

API_KEY = os.getenv("KEY")
Admin_ID = os.getenv("ID")
Guild_ID = os.getenv("Guild_ID")

MY_GUILD = discord.Object(id=Guild_ID)


class MyClient(discord.Client):
    user: discord.ClientUser

    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


intents = discord.Intents.default()
client = MyClient(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


# simple command to reply back to the user
@client.tree.command()
async def ping(interaction: discord.Interaction):
    """reply with Pong!!"""
    await interaction.response.send_message(f'Pong! {interaction.user.mention}', ephemeral=True)

# Simple repeat command
@client.tree.command()
@app_commands.describe(
    message='The message to repeat',
)
async def repeat(interaction: discord.Interaction, message: str):
    """repeats a message."""
    await interaction.response.send_message(message)

# Simple Dice Roll command
@client.tree.command()
@app_commands.describe(
    sides="The number of sides on the dice"
)
async def dice(interaction: discord.Interaction, sides: int):
    """rolls a dice."""
    if sides < 1:
        await interaction.response.send_message("The number of sides must be at least 1.", ephemeral=True)
        return
    else:
        await interaction.response.send_message(f'{interaction.user.mention} roles a {sides}-sided dice...')
        roll = random.randint(1, sides)
        await interaction.followup.send(f'{interaction.user} rolled a {roll}')



class Months(Enum):
    january = "January"
    july = "July"
    august = "August"
    september = "September"
    october = "October"
    november = "November"
    december = "December"

# Important_dates command
@client.tree.command()
@app_commands.describe(
    month="The month you want details for"
)
async def important_date(interactions: discord.Interaction, month: Months):
    """Says important information about a month."""
    month_map = {
        Months.january: "January",
        Months.july: "July",
        Months.august: "August",
        Months.september: "September",
        Months.october: "October",
        Months.november: "November",
        Months.december: "December"
    }

    dates = month_map[month]
    days = important_dates.get(dates, [])

    datel = [f"\n# __{dates}__"]
    for date in days:
        datel.append(f"{date}")

    await interactions.response.send_message("\n".join(datel), ephemeral=True)


@client.tree.command()
async def data(interactions: discord.Interaction):
    """"Sends the data roadmap image."""
    await interactions.response.send_message(os.getenv("DATA_IMAGE"), ephemeral=True)

# Help command

class Commands(Enum):
    ping = "ping"
    repeat = "repeat"
    important_date = "important_date"
    dice = "dice"
    data = "data"
    due = "due"


@client.tree.command()
@app_commands.describe(
    command='the command you need help with'
)
async def help(interactions: discord.Interaction, command: Commands):
    """provides information on the selected command."""


    commands_map = {
        Commands.ping: "ping",
        Commands.repeat: "repeat",
        Commands.important_date: "important_date",
        Commands.dice: "dice",
        Commands.data: "data",
        Commands.due: "due",
    }

    command_name = commands_map[command]
    info = commands_info.get(command_name, [])

    command_info = [f"\n__{command_name}__"]
    for command_infos in info:
        command_info.append(f"  - {command_infos}")

    await interactions.response.send_message("\n".join(command_info), ephemeral=True)  



# class Class(Enum):
    # all = "all"
    # cdir = "CDIR"
    # data = "Data Academy"
    # citw = "Communications in the Workplace"

# Due command
@client.tree.command()
# @app_commands.describe(
#        course="The class you want to check"
# )
async def due(interactions: discord.Interaction):
    """Says what's due for the current week."""

    # """if course == Class.all:
    #    message = []
    #    for subject, assignments in due_dates.items():
    #       message.append(f"\n **__{subject}__**")
    #       for assignment in assignments:
    #          message.append(f" - {assignment}")
    #   await interactions.response.send_message("\n".join(message), ephemeral=True)
               
    #else: 
    #key_map = {
            # Class.cdir: "CDIR",
            #Class.data: "Data Academy",
            # Class.citw: "Communication in the Workplace",
    #}

    subject = "Data Academy"
    tasks = due_dates.get(subject, [])

    message = [f"\n**__{subject}__**"]
    for task in tasks:
        message.append(f"  - {task}")
    for update in due_dates["Last Updated"]:
        message.append(f"\n**__Last Updated:__** \n - __{update}__")

    await interactions.response.send_message("\n".join(message), ephemeral=True)



client.run(API_KEY)




