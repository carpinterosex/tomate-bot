import os
import discord
from discord.ext import commands
from google import genai

TOKEN = os.getenv("TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

print("TOKEN existe:", TOKEN is not None)
print("GEMINI existe:", GEMINI_API_KEY is not None)

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

    # Reaccionar a usuarios específicos
    if message.author.id in USUARIOS_OBJETIVO:
        for reaccion in REACCIONES:
            try:
                await message.add_reaction(reaccion)
            except Exception:
                pass

    # Responder a menciones con Gemini
    if bot.user in message.mentions:
        pregunta = message.content.replace(f"<@{bot.user.id}>", "")
        pregunta = pregunta.replace(f"<@!{bot.user.id}>", "").strip()

        if pregunta:
            # 'async with' asegura que el bot deje de "escribir" si algo falla dentro
            async with message.channel.typing():
                try:
                    prompt = f"""
Eres un bot de Discord.

Reglas:
- Responde siempre en español.
- Máximo 30 palabras.
- No hagas listas.
- No des explicaciones largas.
- Sé directo y amigable.
- Si falta información, pide solo lo necesario.

Usuario: {pregunta}
"""
                    # Toda esta sección ahora está correctamente indentada dentro del try
                    respuesta = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt
                    )

                    texto = respuesta.text[:300]
                    await message.reply(texto)

                except Exception as e:
                    await message.reply(f"Error al procesar con Gemini: {e}")

    await bot.process_commands(message)

bot.run(TOKEN)
