import os
import discord
from discord.ext import commands
from google import genai
TOKEN = os.getenv("TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)
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
async def on_message(message):

    if message.author == bot.user:
        return

    if message.author.id in USUARIOS_OBJETIVO:
        for reaccion in REACCIONES:
            try:
                await message.add_reaction(reaccion)
            except:
                pass

    if bot.user in message.mentions:

        pregunta = message.content.replace(f"<@{bot.user.id}>", "")
        pregunta = pregunta.replace(f"<@!{bot.user.id}>", "").strip()

        if pregunta:

            await message.channel.typing()

            try:
                respuesta = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=pregunta
                )

                texto = respuesta.text[:2000]

                await message.reply(texto)

            except Exception as e:
                await message.reply(f"Error: {e}")

    await bot.process_commands(message)


bot.run(TOKEN)
