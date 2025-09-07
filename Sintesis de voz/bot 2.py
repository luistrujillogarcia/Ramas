import discord
from discord.ext import commands
import requests
import pyttsx3
from googletrans import Translator

# --- Configuración de voz ---
def talk(text, voz_id=0):
    engine = pyttsx3.init()
    engine.setProperty("rate", 140)
    engine.setProperty("volume", 0.9)
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[voz_id].id)  # 0 = masculino, 1 = femenino
    engine.say(text)
    engine.runAndWait()

# --- Bot de Discord ---
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)

# Guardar voz actual (por defecto masculina)
bot.voz_actual = 0

# --- Comandos básicos ---
@bot.command()
async def hello(ctx):
    await ctx.send("Hola, soy tu ingenioso asistente virtual, Llámame Norbot 🤖")
    talk("Hola, soy tu ingenioso asistente virtual, Llámame Norbot", bot.voz_actual)

def obtener_clima(ciudad: str) -> str:
    url = f"https://wttr.in/{ciudad}?format=%C+%t&lang=es"
    respuesta = requests.get(url)

    if respuesta.status_code == 200:
        clima = respuesta.text.strip()
        if "lluvia" in clima.lower():
            clima += " ☔ No olvides tu paraguas."
        elif "soleado" in clima.lower():
            clima += " 😎 Ponte tus gafas de sol."
        elif "nieve" in clima.lower():
            clima += " ❄️ Hora de hacer un muñeco de nieve."
        elif "nublado" in clima.lower():
            clima += " 🌥️ Parece que el sol se escondió."
        return clima
    else:
        return "No se conectó a la API"

@bot.command()
async def clima(ctx, *, ciudad: str):
    prediccion = obtener_clima(ciudad)
    await ctx.send(f"El clima en {ciudad} es: {prediccion}")
    talk(f"El clima en {ciudad} es: {prediccion}", bot.voz_actual)

# --- Comando para cambiar la voz ---
@bot.command()
async def voz(ctx, tipo: str):
    if tipo.lower() == "masculina":
        bot.voz_actual = 0
        await ctx.send("✅ Voz cambiada a masculina")
    elif tipo.lower() == "femenina":
        bot.voz_actual = 1
        await ctx.send("✅ Voz cambiada a femenina")
    else:
        await ctx.send("Por favor, elige 'masculina' o 'femenina'.")

# --- Obtener hechos ---
def obtener_hecho():
    url = "https://uselessfacts.jsph.pl/random.json?language=en"
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        return respuesta.json().get("text")
    else:
        return "No pude obtener un hecho curioso ahora mismo."

# --- Comandos de hechos curiosos por tema ---
@bot.command()
async def ciencia(ctx):
    hecho = obtener_hecho()
    traductor = Translator()
    hecho_traducido = traductor.translate(hecho, src="en", dest="es").text
    await ctx.send(f"🔬 Dato de ciencia: {hecho_traducido}")
    talk(hecho_traducido, bot.voz_actual)

@bot.command()
async def historia(ctx):
    hecho = obtener_hecho()
    traductor = Translator()
    hecho_traducido = traductor.translate(hecho, src="en", dest="es").text
    await ctx.send(f"📜 Dato de historia: {hecho_traducido}")
    talk(hecho_traducido, bot.voz_actual)

@bot.command()
async def espacio(ctx):
    hecho = obtener_hecho()
    traductor = Translator()
    hecho_traducido = traductor.translate(hecho, src="en", dest="es").text
    await ctx.send(f"🌌 Dato del espacio: {hecho_traducido}")
    talk(hecho_traducido, bot.voz_actual)

@bot.command()
async def animales(ctx):
    hecho = obtener_hecho()
    traductor = Translator()
    hecho_traducido = traductor.translate(hecho, src="en", dest="es").text
    await ctx.send(f"🐾 Dato de animales: {hecho_traducido}")
    talk(hecho_traducido, bot.voz_actual)

# Ejecutar el bot
bot.run("TOKEN")
