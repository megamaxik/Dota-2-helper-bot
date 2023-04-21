import discord
from discord.ext import commands
import logging
import sqlite3

con = sqlite3.connect("../Dota-2-helper-bot/DotaHelper.db")
cur = con.cursor()
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='>', intents=intents)

@bot.command()
async def info(ctx, *, text):
    x = 'SELECT info FROM Heroes WHERE hero like "%' + text + '%"'
    result = cur.execute(x).fetchall()
    await ctx.send(str(*result)[2:-3].replace(r'\r\n','\r\n'))

@bot.command()
async def conterpick(ctx, *, text):
    x = 'SELECT conterpick FROM Heroes WHERE hero like "%' + text + '%"'
    result = cur.execute(x).fetchall()
    await ctx.send(str(*result)[2:-3].replace(r'\r\n','\r\n'))

@bot.command()
async def builds(ctx, *, text):
    x = 'SELECT builds FROM Heroes WHERE hero like "%' + text + '%"'
    result = cur.execute(x).fetchall()
    result = str(*result)[2:-3]
    await ctx.send(result.replace(r'\r\n','\r\n'))

@bot.command()
async def story(ctx, *, text):
    x = 'SELECT story FROM Heroes WHERE hero like "%' + text + '%"'
    result = cur.execute(x).fetchall()
    await ctx.send(str(*result)[2:-3].replace(r'\r\n','\r\n'))

@bot.command()
async def spells(ctx, *, text):
    x = 'SELECT spells FROM Heroes WHERE hero like "%' + text + '%"'
    result = cur.execute(x).fetchall()
    await ctx.send(str(*result)[2:len(str(*result)) // 2].replace(r'\r\n','\r\n'))
    await ctx.send(str(*result)[len(str(*result)) // 2:-2].replace(r'\r\n','\r\n'))

@bot.command()
async def item(ctx, *, text):
    x = 'SELECT description FROM Items WHERE name like "%' + text + '%"'
    result = cur.execute(x).fetchall()
    await ctx.send(str(*result)[2:-3].replace(r'\r\n','\r\n'))

@bot.command()
async def commands(ctx):
    await ctx.send(">info (имя героя) - информация о герое")
    await ctx.send(">counterpick (имя героя) - контрпик героя")
    await ctx.send(">builds (имя героя) - предметы на героя")
    await ctx.send(">story (имя героя) - история героя")
    await ctx.send(">spells (имя героя) - способности героя")
    await ctx.send(">description (имя героя) - информация о герое")
    await ctx.send(">item (название предмета) - информация о предмете")
    await ctx.send(">guide_lines - информация о линиях в доте")
    await ctx.send(">guide_main - общая информация о доте")


@bot.command()
async def guide_lines(ctx):
    await ctx.send("В доте есть 3 линии: легкая, ценртальная, тяжелая")
    await ctx.send("На легкой и тяжелой линии стоит по два игрока, а на центральной один игрок")
    await ctx.send("На легкой стоит полная поддержка(пятая позиция) и керри(первая позиция).")
    await ctx.send("На тяжелой стоит частичная поддержка(четвертая позиция) и офлейнер(третья позиция).")
    await ctx.send("На миду - мидер(вторая позиция).")

@bot.command()
async def guide_main(ctx):
    await ctx.send("В доте матчи проходят 5 на 5")
    await ctx.send("Полная поддержка - сильный герой в начале, который помогает своему керри развиться.")
    await ctx.send("Частичная поддержка - герой сильный в начале, середине игры.Она помогает всем линиям.")
    await ctx.send("Офлейнер - герой который зачастую начинает драки, сильный в середине или конце игры.")
    await ctx.send("Мидер - герой который силен в середине и конце игры.Помогает в начале другим линиям, а далее ходит вместе с командой.")
    await ctx.send("Керри - герой способный зарабатывать много золота, из-за чего ближе к концу игры становиться главным звеном команды")


bot.run('MTA4OTE0MDM3MjAxMTIyOTIzNQ.GpfhRa.E28ifF5M8KIN3z0ovfVIR2ukXv8cc3iDpiyOM0')
