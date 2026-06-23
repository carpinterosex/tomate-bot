import os
import time
import discord
from discord.ext import commands
from google import genai
from datetime import datetime

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
                
                # --- NUEVA LÓGICA: OBTENER EL HISTORIAL RECIENTE ---
                historial_texto = ""
                try:
                    # Lee los últimos 200 mensajes del canal donde se hizo la pregunta
                    async for msg in message.channel.history(limit=300, before=message):
                        # Evitamos meter comandos u otras menciones al bot para no confundir a Gemini
                        if msg.content and not msg.content.startswith("!"):
                            historial_texto += f"{msg.author.display_name}: {msg.content}\n"
                except Exception as e:
                    print(f"No se pudo leer el historial: {e}")
                # --------------------------------------------------

                intentos = 3
                exito = False
                texto_respuesta = ""
                ultimo_error = ""

                for intento in range(intentos):
                    try:
                        fecha_actual = datetime.now().strftime("%A, %d de %B de %Y - %H:%M")
                        
                        prompt = f"""
Eres un bot de Discord con acceso al historial de mensajes recientes del canal.
La fecha y hora actual real es: {fecha_actual}

Historial reciente del canal (para tu contexto):
{historial_texto if historial_texto else "No hay mensajes previos disponibles."}

Reglas:
- Responde a la pregunta del usuario basándote en el historial provisto arriba si es relevante.
- Responde siempre en español.
- Máximo 40 palabras (se extendió un poco para que puedas dar mejores resúmenes).
- No hagas listas.
- Sé directo y amigable.

Usuario: {pregunta}
"""
                        respuesta = client.models.generate_content(
                            model="gemini-2.5-flash",
                            contents=prompt
                        )
                        texto_respuesta = respuesta.text[:400]
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
