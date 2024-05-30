import discord
from discord.ext import commands
from PIL import Image
import io
import requests
import random
from config import TOKEN,API_TOKEN
from translate import Translator
from langdetect import detect
import re
import json
import os
import time

WIN_STREAK_DE_FILE = "./data/winstreak_de.json"
WIN_STREAK_CASINO_FILE = "./data/winstreak_casino.json"

if os.path.exists(WIN_STREAK_DE_FILE):
    with open(WIN_STREAK_DE_FILE, "r") as f:
        win_streaks_de = json.load(f)
else:
    win_streaks_de = {"user":[]}

if os.path.exists(WIN_STREAK_CASINO_FILE):
    with open(WIN_STREAK_CASINO_FILE, "r") as f:
        win_streaks_casino = json.load(f)
else:
    win_streaks_casino = {"user":[]}  

def save_win_streaks_de():
    with open(WIN_STREAK_DE_FILE, "w") as f:
        json.dump(win_streaks_de, f)

def save_win_streaks_de():
    with open(WIN_STREAK_CASINO_FILE, "w") as f:
        json.dump(win_streaks_casino, f)

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True  
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} est prêt !')

def contains_link(message):
    link_patterns = [r'youtube.com\/\S*',r'x.com\/\S*',r'facebook.com\/\S*',r'google.com\/\S*',r'https?://\S+']
    for pattern in link_patterns:
        if re.search(pattern, message.content):
            return True, pattern
    return False, None

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    link = contains_link(message)
    if link[0] != False:
        print(link)
        match link[1]:
            case r'youtube.com\/\S*': 
                destination_channel = bot.get_channel(1245776198907330651)
            case r'x.com\/\S*' | r'facebook.com\/\S*':
                destination_channel = bot.get_channel(1245776170599841842)
            case r'google.com\/\S*' | r'https?://\S+':
                destination_channel = bot.get_channel(1245771119370436708)
        message_content = message.content
        try:
            await destination_channel.send(content=f"{message.author.mention} : {message_content}")
        except discord.HTTPException as e:
            print(f"Erreur lors de l'envoi du message : {e}")
        
        await message.delete()
    await bot.process_commands(message)

@bot.command()
async def img2pdf(ctx):
    """Envoyer une image, Boti vous enverra le pdf"""
    if not ctx.message.attachments:
        await ctx.send("Veuillez joindre une image à votre message.")
        return
    attachment = ctx.message.attachments[0]
    if not attachment.filename.endswith((".jpg", ".jpeg", ".png")):
        await ctx.send("Le fichier joint n'est pas une image valide.")
        return
    try:
        image_bytes = await attachment.read()
        image = Image.open(io.BytesIO(image_bytes))
        pdf_bytes = io.BytesIO()
        image.save(pdf_bytes, format="PDF")
        pdf_bytes.seek(0)
        pdf_file = discord.File(pdf_bytes, filename=f"{attachment.filename.split('.')[0]}.pdf")
        await ctx.send(file=pdf_file)
    except Exception as e:
        await ctx.send(f"Une erreur s'est produite lors de la conversion : {e}")

@bot.command()       
async def weather(ctx, *, city: str):
    """Commande pour afficher la météo d'une ville"""
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_TOKEN}&units=metric&lang=fr'
    response = requests.get(url)
    data = response.json()
    if data['cod'] == 200:
        city_name = data['name']
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        embed = discord.Embed(title=f'Météo pour {city_name}', color=0x00ff00)
        embed.add_field(name='Description', value=weather_description, inline=False)
        embed.add_field(name='Température', value=f'{temperature}°C', inline=True)
        embed.add_field(name='Humidité', value=f'{humidity}%', inline=True)
        embed.add_field(name='Vitesse du vent', value=f'{wind_speed} m/s', inline=True)
        await ctx.send(embed=embed)
    else:
        error_message = data['message']
        await ctx.send(f'Erreur : {error_message}')
@bot.command()
async def spin(ctx):
    emojis = ["🍒", "🍋", "🍊", "🍇", "🍓", "🍍"]
    embed = discord.Embed(title="Machine à sous")
    reel1, reel2, reel3 = random.sample(emojis, 3)
    embed.add_field(name="", value=f"{reel1} | {reel2} | {reel3}")
    message = await ctx.send(embed=embed)

    for _ in range(10):
        reel1, reel2, reel3 = random.sample(emojis, 3)
        embed.set_field_at(0, name="", value=f"{reel1} | {reel2} | {reel3}")
        await message.edit(embed=embed)
        time.sleep(0.5)

    if reel1 == reel2 == reel3:
        embed.set_field_at(0, name="Résultat", value="Vous avez gagné !")
    elif reel1 == reel2 or reel2 == reel3 or reel3 == reel1:
        embed.set_field_at(0, name="Résultat", value="Double !!!")
    else:
        embed.set_field_at(0, name="Résultat", value="Vous avez perdu.")

    await message.edit(embed=embed)
@bot.command()
async def dé(ctx):
    """Jeu de dé, faites un paire est c'est gagner !!!"""
    faces = ["⚀","⚁","⚂","⚃","⚄","⚅"]
    dé_1 = random.randint(0,len(faces))
    dé_2 = random.randint(0,len(faces))
    if dé_1 == dé_2:
        embed = discord.Embed(title=f'Jeux de dé 🎲', color=0x00ff00)
        embed.add_field(name="Pair", value=f"{faces[dé_1]} = {faces[dé_2]}")
        if len(win_streaks_de['user']) == 0:
            tab_win = {
                    'id':ctx.author.id,
                    'win':1
                }
            win_streaks_de['user'].append(tab_win)
        else:
            for user in win_streaks_de['user']:
                if user['id'] != ctx.author.id:
                    tab_win = {
                        'id':ctx.author.id,
                        'win':1
                    }
                    win_streaks_de['user'].append(tab_win)
                elif user['id'] == ctx.author.id:
                    user['win'] += 1 
                    break
    else:
        embed = discord.Embed(title=f'Jeux de dé 🎲', color=0xffff00)
        embed.add_field(name='Dé numéro 1:', value=f"**{faces[dé_1]}**", inline=True)
        embed.add_field(name='Dé numéro 2:', value=f"**{faces[dé_2]}**", inline=True) 
    await ctx.send(embed=embed)
    bot.loop.call_soon(save_win_streaks_de)

@bot.command()
async def coinflip(ctx):
    possibilities = ['Pile', 'Face']
    await ctx.send(f"*Le bot lance une pièce*... C'est {random.choice(possibilities)} !")

@bot.command()
async def chuck_norris(ctx):
    """Commande pour afficher une citation aléatoire de Chuck Norris"""
    response = requests.get('https://api.chucknorris.io/jokes/random')
    data = response.json()
    translator = Translator(to_lang="fr")
    if response.status_code == 200:
        quote = data['value']
        french_quote = translator.translate(quote)
        embed = discord.Embed(title='Citation de Chuck Norris', description=french_quote, color=0xffa500)
        await ctx.send(embed=embed)
    else:
        error_message = data['message']
        await ctx.send(f'Erreur : {error_message}')
@bot.command()
async def meme(ctx):
    content = requests.get("https://meme-api.com/gimme").json()
    meme = content["url"]
    await ctx.send(meme)

@bot.command()
async def translate(ctx, *, message: str):
    """Commande pour Traduire du francais en une autre langue ['fr', 'en', 'es', 'de', 'it', 'pt', 'ru', 'zh', 'ja', 'ko', 'ar', 'hi', 'tr', 'nl', 'sv', 'pl', 'ro', 'hu', 'cs', 'da', 'fi', 'el', 'he', 'id', 'ms', 'no', 'th', 'vi']"""
    to_lang = ctx.message.content.split()[1]
    trad = Translator(to_lang=to_lang, from_lang=detect(message))
    print(detect(message))
    await ctx.send(trad.translate(' '.join(message.split()[1:])))

@bot.command()
async def translate_message(ctx, to_lang: str):
    """Traduit le message auquel l'utilisateur répond dans la langue cible spécifiée"""
    message_reference = ctx.message.reference
    if message_reference:
        message_à_traduire = await ctx.channel.fetch_message(message_reference.message_id)
        traduction = Translator(to_lang=to_lang,from_lang=detect(message_à_traduire.content))
        await ctx.send(f"Traduction {detect(message_à_traduire.content)} en {to_lang} : {traduction.translate(message_à_traduire.content)}")
    else:
        await ctx.send("Vous devez répondre à un message pour utiliser cette commande.")

bot.run(TOKEN)