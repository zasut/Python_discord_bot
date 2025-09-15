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

load_dotenv()

API_KEY = os.getenv("KEY")
Admin_ID = int(os.getenv("ID"))

MY_GUILD = discord.Object(id=1407756705068224622)


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


# simple hello command
@client.tree.command()
async def hello(interaction: discord.Interaction):
    """Says hello!"""
    await interaction.response.send_message(f'Hi, {interaction.user.mention}')

# Simple repeat command
@client.tree.command()
@app_commands.describe(
    message='The message to repeat',
)
async def repeat(interaction: discord.Interaction, message: str):
    """"repeats a message."""
    await interaction.response.send_message(message)

# Simple Dice Roll command
@client.tree.command()
@app_commands.describe(
    sides="The number of sides on the dice"
)
async def dice(interaction: discord.Interaction, sides: int):
    """""rolls a dice."""
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

    datel = [f"\n__{dates}__"]
    for date in days:
        datel.append(f"  - {date}")

    await interactions.response.send_message("\n".join(datel), ephemeral=True)





class Class(Enum):
    all = "all"
    cdir = "cdir"
    tech = "tech essentials"
    citw = "Communications in the Workplace"
    software = "Software development fundementals"

# Due command
@client.tree.command()
@app_commands.describe(
        course="The class you want to check"
)
async def due(interactions: discord.Interaction, course: Class):
    """Says what's due for the current week."""

    if course == Class.all:
        message = []
        for subject, assignments in due_dates.items():
            message.append(f"\n **__{subject}__**")
            for assignment in assignments:
                message.append(f" - {assignment}")
        await interactions.response.send_message("\n".join(message), ephemeral=True)
                    
    else:
        key_map = {
            Class.cdir: "CDIR",
            Class.tech: "Tech Essentials",
            Class.citw: "Communication in the Workplace",
            Class.software: "Software Development Fundamentals"
        }

        subject = key_map[course]
        tasks = due_dates.get(subject, [])

        message = [f"\n**__{subject}__**"]
        for task in tasks:
            message.append(f"  - {task}")
        for update in due_dates["Last Updated"]:
            message.append(f"\n**__Last Updated:__** \n__{update}__")

        await interactions.response.send_message("\n".join(message), ephemeral=True)



client.run(API_KEY)




