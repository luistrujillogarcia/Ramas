import discord
from discord.ext import commands
import requests
import pyttsx3

def talk(text):
    engine = pyttsx3.init()  # object creation
    rate = engine.getProperty("rate")  # getting details of current speaking rate
    engine.setProperty("rate", 100)  # setting up new voice rat
    volume = engine.getProperty("volume")  # getting to know current volume level (min=0 and max=1)
    engine.setProperty("volume", 1.0)  # setting up volume level  between 0 and 
    voices = engine.getProperty("voices")  # getting details of current voice
    engine.setProperty("voice", voices[1].id)  # changing index, changes voices. 1 for female
    pitch = engine.getProperty("pitch")  # Get current pitch value
    engine.setProperty("pitch", 75)  # Set the pitch (default 50) to 75 out of 100
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
    await ctx.send("Hola, soy tu ingenioso asistente virtual de voz, Llámame Norbot")
    talk("Hola, soy tu ingenioso asistente virtual de voz, Llámame Norbot")

def obtener_clima(ciudad: str) -> str:
    url = "https://wttr.in/{ciudad}?format=%C+%t&lang=es"
    respuesta = requests.get(url)

    if respuesta.status_code == 200:
        return respuesta.text.strip()
    else:
        return "No se conecto a la API"
    
@bot.command()
async def clima(ctx, *, ciudad:str):
    prediccion = obtener_clima(ciudad)
    await ctx.send(f"El clima en {ciudad} es: {prediccion}")
    talk(f"El clima en {ciudad} es: {prediccion}")

# correr el bot
bot.run("TOKEN")
