import discord
from discord.ext import commands
import os

TOKEN = os.getenv("TOKEN")

USUARIO_OBJETIVO = 123456789012345678

REACCIONES = ["🍅"]

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

@bot.event
async def on_message(message):
    if message.author.id == bot.user.id:
        return

    if message.author.id == 974297735559806986:
        for reaccion in REACCIONES:
            try:
                await message.add_reaction(reaccion)
            except Exception:
                pass

    await bot.process_commands(message)

bot.run(TOKEN)
