import random
import time
import discord
import json
import os

WIN_STREAK_DE_FILE = "./data/winstreak_de.json"
WIN_STREAK_CASINO_FILE = "./data/winstreak_casino.json"

if os.path.exists(WIN_STREAK_DE_FILE):
    with open(WIN_STREAK_DE_FILE, "r") as f:
        win_streaks_de = json.load(f)
else:
    win_streaks_de = {}

if os.path.exists(WIN_STREAK_CASINO_FILE):
    with open(WIN_STREAK_CASINO_FILE, "r") as f:
        win_streaks_casino = json.load(f)
else:
    win_streaks_casino = {}  

async def spin_commands(ctx):
    emojis = ["🍒", "🍋", "🍊", "🍇", "🍓", "🍍"]
    player_id = str(ctx.author.id)
    if player_id not in win_streaks_casino:
        win_streaks_casino[ctx.author.id] = {"wins": 0,"double": 0, "plays": 0}
    win_streaks_casino[player_id]['plays'] += 1
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
        win_streaks_casino[player_id]['win'] += 1
    elif reel1 == reel2 or reel2 == reel3 or reel3 == reel1:
        embed.set_field_at(0, name="Résultat", value="Double !!!")
        win_streaks_casino[player_id]['double'] += 1
    else:
        embed.set_field_at(0, name="Résultat", value="Vous avez perdu.")

    await message.edit(embed=embed)

    with open(WIN_STREAK_CASINO_FILE, "w") as f:
        json.dump(win_streaks_casino, f)

async def dé_commands(ctx):
    """Jeu de dé, faites un paire est c'est gagner !!!"""
    faces = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]
    dé_1 = random.randint(0, len(faces) - 1)
    dé_2 = random.randint(0, len(faces) - 1)

    player_id = str(ctx.author.id)
    if player_id not in win_streaks_de:
        win_streaks_de[ctx.author.id] = {"wins": 0, "plays": 0}

    win_streaks_de[player_id]["plays"] += 1

    if dé_1 == dé_2:
        embed = discord.Embed(title=f'Jeux de dé 🎲', color=0x00ff00)
        embed.add_field(name="Pair", value=f"{faces[dé_1]} = {faces[dé_2]}")
        win_streaks_de[player_id]["wins"] += 1
    else:
        embed = discord.Embed(title=f'Jeux de dé 🎲', color=0xffff00)
        embed.add_field(name='Dé numéro 1:', value=f"**{faces[dé_1]}**", inline=True)
        embed.add_field(name='Dé numéro 2:', value=f"**{faces[dé_2]}**", inline=True)

    await ctx.send(embed=embed)

    with open(WIN_STREAK_DE_FILE, "w") as f:
        json.dump(win_streaks_de, f)

async def coinflip_commands(ctx):
    possibilities = ['Pile', 'Face']
    await ctx.send(f"*Le bot lance une pièce*... C'est {random.choice(possibilities)} !")