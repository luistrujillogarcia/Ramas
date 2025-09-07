import discord
from discord.ext import commands
import requests
import pyttsx3
from googletrans import Translator

# Función para vocalizar texto
def talk(text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 140)   # velocidad natural
    engine.setProperty("volume", 0.9) # volumen
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[0].id)  # 0 = masculino, 1 = femenino
    engine.say(text)
    engine.runAndWait()

# Función para traducir de inglés a español
def traducir_a_es(texto_en_ingles):
    traductor = Translator()
    traduccion = traductor.translate(texto_en_ingles, src='en', dest='es')
    return traduccion.text

# Función para obtener clima
def obtener_clima(ciudad: str) -> str:
    url = f"https://wttr.in/{ciudad}?format=%C+%t&lang=es"
    respuesta = requests.get(url)

    if respuesta.status_code == 200:
        clima = respuesta.text.strip()
        # Comentarios divertidos según el clima
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

# Función para obtener un hecho interesante
def obtener_hecho_interesante() -> str:
    url = "https://uselessfacts.jsph.pl/random.json?language=en"
    try:
        respuesta = requests.get(url)
        if respuesta.status_code == 200:
            data = respuesta.json()
            hecho = data.get("text", "No encontré un hecho interesante.")
            return hecho
        else:
            return "No pude obtener un hecho en este momento."
    except Exception as e:
        return f"Ocurrió un error: {e}"

# Permisos y creación del bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)

# Comando de saludo
@bot.command()
async def hello(ctx):
    saludo = "Hola, soy tu ingenioso asistente virtual, Llámame Norbot"
    await ctx.send(saludo)
    talk(saludo)

# Comando de clima + hecho curioso traducido
@bot.command()
async def clima(ctx, *, ciudad:str):
    prediccion = obtener_clima(ciudad)
    await ctx.send(f"El clima en {ciudad} es: {prediccion}")
    talk(f"El clima en {ciudad} es: {prediccion}")
    
    hecho_ingles = obtener_hecho_interesante()
    hecho_es = traducir_a_es(hecho_ingles)
    await ctx.send(f"Y aquí tienes un hecho curioso: {hecho_es}")
    talk(f"Y aquí tienes un hecho curioso: {hecho_es}")

# Comando independiente para hecho curioso
@bot.command()
async def hecho(ctx):
    hecho_ingles = obtener_hecho_interesante()
    hecho_es = traducir_a_es(hecho_ingles)
    await ctx.send(hecho_es)
    talk(hecho_es)

# Ejecutar el bot
bot.run("TOKEN")
