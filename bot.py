import os
import discord
from discord.ext import commands

TOKEN = os.getenv("TOKEN")

USUARIOS_OBJETIVO = [
    887786888839180288,  # Usuario 1
    316310136144658444,  # Usuario 2
    1164933082428743701,  # Usuario 3
    974297735559806986   # Usuario 4
]

REACCIONES = ["🍅"]

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

@bot.event
async def on_message(message):
    if message.author.id in USUARIOS_OBJETIVO:
        for reaccion in REACCIONES:
            try:
                await message.add_reaction(reaccion)
            except Exception as e:
                print(f"Error al reaccionar: {e}")

    await bot.process_commands(message)

bot.run(TOKEN)
