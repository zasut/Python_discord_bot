import discord 
import os
from dotenv import load_dotenv
from discord import app_commands

load_dotenv()

API_KEY = os.getenv("KEY")

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

@client.tree.command()
async def hello(interaction: discord.Interaction):
    """Says hello!"""
    await interaction.response.send_message(f'Hi, {interaction.user.mention}')

@client.tree.command()
@app_commands.describe(
    message='The message to repeat',
)
async def repeat(interactions: discord.Interaction, message: str):
    """"repeats a message."""
    await interactions.response.send_message(message)





client.run(API_KEY)




