import requests
from config import API_TOKEN
import discord
from PIL import Image
import io
from translate import Translator
from langdetect import detect

async def weather_commands(ctx, city: str):
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

async def img2pdf_commands(ctx):
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

async def poll_commands(ctx, question, *options):
    if len(options) < 2:
        await ctx.send("Vous devez fournir au moins deux options de vote.")
        return
    embed = discord.Embed(title=question, color=discord.Color.blue())
    for emoji, option in zip(["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"], options):
        embed.add_field(name=emoji, value=option, inline=False)
    poll_message = await ctx.send(embed=embed)
    for emoji in ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"][:len(options)]:
        await poll_message.add_reaction(emoji)
    instructions = "Réagissez avec les émojis correspondants pour voter !"
    await ctx.send(instructions)

async def translate_commands(ctx, *, message: str):
    to_lang = ctx.message.content.split()[1]
    trad = Translator(to_lang=to_lang, from_lang=detect(message))
    #bug retourne non 
    print(detect(message))
    await ctx.send(trad.translate(' '.join(message.split()[1:])))

async def translate_message_commands(ctx, to_lang: str):
    message_reference = ctx.message.reference
    if message_reference:
        message_à_traduire = await ctx.channel.fetch_message(message_reference.message_id)
        traduction = Translator(to_lang=to_lang,from_lang=detect(message_à_traduire.content))
        await ctx.send(f"Traduction {detect(message_à_traduire.content)} -> {to_lang} : {traduction.translate(message_à_traduire.content)}")
    else:
        await ctx.send("Vous devez répondre à un message pour utiliser cette commande.")

# FUN COMMAND 

async def meme_commands(ctx):
    content = requests.get("https://meme-api.com/gimme").json()
    meme = content["url"]
    await ctx.send(meme)

async def chuck_norris_commands(ctx):
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