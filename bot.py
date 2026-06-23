import os
import time
import discord
from discord.ext import commands
from google import genai

TOKEN = os.getenv("TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

print("TOKEN existe:", TOKEN is not None)
print("GEMINI existe:", GEMINI_API_KEY is not None)

client = genai.Client(api_key=GEMINI_API_KEY)

USUARIOS_OBJETIVO = [
    887786888839180288,
    316310136144658444,
    1164933082428743701,
    974297735559806986
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
            except Exception:
                pass

    if bot.user in message.mentions:
        pregunta = message.content.replace(f"<@{bot.user.id}>", "")
        pregunta = pregunta.replace(f"<@!{bot.user.id}>", "").strip()

        if pregunta:
            async with message.channel.typing():
                intentos = 3
                exito = False
                texto_respuesta = ""
                ultimo_error = ""

                for intento in range(intentos):
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
                        respuesta = client.models.generate_content(
                            model="gemini-2.5-flash",
                            contents=prompt
                        )
                        texto_respuesta = respuesta.text[:300]
                        exito = True
                        break
                        
                    except Exception as e:
                        ultimo_error = str(e)
                        if "503" in ultimo_error or "UNAVAILABLE" in ultimo_error:
                            time.sleep(3)
                        else:
                            break

                if exito:
                    await message.reply(texto_respuesta)
                else:
                    await message.reply(f"Error tras varios intentos: {ultimo_error}")

    await bot.process_commands(message)

bot.run(TOKEN)

```
