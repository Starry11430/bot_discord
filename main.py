import discord
from discord.ext import commands
from config import TOKEN
import re
import play
import utility


intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True  
bot = commands.Bot(command_prefix='!', intents=intents)

# ------- EVENT -------

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

# ------- COMMAND -------

@bot.command()
async def img2pdf(ctx):
    """Envoyer une image, Boti vous enverra le pdf"""
    await utility.img2pdf_commands(ctx)

@bot.command()       
async def weather(ctx, *, city: str):
    """Commande pour afficher la météo d'une ville"""
    await utility.weather_commands(ctx, city)
    

@bot.command()
async def poll(ctx, question, *options):
    """Crée un sondage avec des réactions en émoji pour voter."""
    await utility.poll_commands(ctx, question, *options)

@bot.command()
async def spin(ctx):
    await play.spin_commands(ctx)

@bot.command()
async def dé(ctx):
    """Jeu de dé, faites un paire est c'est gagner !!!"""
    await play.dé_commands(ctx)

@bot.command()
async def coinflip(ctx):
    await play.coinflip_commands(ctx)

@bot.command()
async def chuck_norris(ctx):
    """Commande pour afficher une citation aléatoire de Chuck Norris"""
    await utility.chuck_norris_commands(ctx)

@bot.command()
async def meme(ctx):
    await utility.meme_commands(ctx)

@bot.command()
async def translate(ctx, *, message: str):
    """Commande pour Traduire du francais en une autre langue ['fr', 'en', 'es', 'de', 'it', 'pt', 'ru', 'zh', 'ja', 'ko', 'ar', 'hi', 'tr', 'nl', 'sv', 'pl', 'ro', 'hu', 'cs', 'da', 'fi', 'el', 'he', 'id', 'ms', 'no', 'th', 'vi']"""
    if message is None:
        await ctx.send("Veuillez fournir un message à traduire.")
        return
    await utility.translate_commands(ctx, message=message)

@bot.command()
async def translate_message(ctx, to_lang: str):
    """Traduit le message auquel l'utilisateur répond dans la langue cible spécifiée"""
    await utility.translate_message_commands(ctx, to_lang)

bot.run(TOKEN)