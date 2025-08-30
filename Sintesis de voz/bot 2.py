import discord
from discord.ext import commands
import requests
import pyttsx3

def talk(text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 140)   # más natural
    engine.setProperty("volume", 0.9)
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[0].id)  # 0 = masculino, 1 = femenino
    engine.say(text)
    engine.runAndWait()

# permisos
intents = discord.Intents.default()
intents.message_content = True
# crear bot
bot = commands.Bot(command_prefix= "$", intents=intents)

#crear un comando
@bot.command()
async def hello(ctx):
    await ctx.send("Hola, soy tu ingenioso asistente virtual del clima, Dime Norbot")
    talk("Hola, soy tu ingenioso asistente virtual del clima, Dime Norbot")

def obtener_clima(ciudad: str) -> str:
    url = f"https://wttr.in/{ciudad}?format=%C+%t&lang=es"
    respuesta = requests.get(url)

    if respuesta.status_code == 200:
        clima = respuesta.text.strip()
        # Añadimos humor según el clima
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
async def clima(ctx, *, ciudad:str):
    prediccion = obtener_clima(ciudad)
    await ctx.send(f"El clima en {ciudad} es: {prediccion}")
    talk(f"El clima en {ciudad} es: {prediccion}")

# correr el bot
bot.run("TOKEN")
