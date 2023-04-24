import discord
from discord.ext import commands
import logging
import sqlite3
import random

con = sqlite3.connect("../pythonProject1/DotaHelper.db")
cur = con.cursor()
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
global random_hero
bot = commands.Bot(command_prefix='>', intents=intents)


@bot.command()
async def info(ctx, *, text):
    x = 'SELECT info FROM Heroes WHERE hero like "%' + text + '%"'
    result = cur.execute(x).fetchall()
    await ctx.send(str(*result)[2:-3].replace(r'\r\n', '\r\n'))


@bot.command()
async def conterpick(ctx, *, text):
    x = 'SELECT conterpick FROM Heroes WHERE hero like "%' + text + '%"'
    result = cur.execute(x).fetchall()
    await ctx.send(str(*result)[2:-3].replace(r'\r\n', '\r\n'))


@bot.command()
async def builds(ctx, *, text):
    x = 'SELECT builds FROM Heroes WHERE hero like "%' + text + '%"'
    result = cur.execute(x).fetchall()
    result = str(*result)[2:-3]
    await ctx.send(result.replace(r'\r\n', '\r\n'))


@bot.command()
async def story(ctx, *, text):
    x = 'SELECT story FROM Heroes WHERE hero like "%' + text + '%"'
    result = cur.execute(x).fetchall()
    await ctx.send(str(*result)[2:-3].replace(r'\r\n', '\r\n'))


@bot.command()
async def spells(ctx, *, text):
    x = 'SELECT spells FROM Heroes WHERE hero like "%' + text + '%"'
    result = cur.execute(x).fetchall()
    await ctx.send(str(*result)[2:len(str(*result)) // 2].replace(r'\r\n', '\r\n'))
    await ctx.send(str(*result)[len(str(*result)) // 2:-2].replace(r'\r\n', '\r\n'))


@bot.command()
async def item(ctx, *, text):
    x = 'SELECT description FROM Items WHERE name like "%' + text + '%"'
    result = cur.execute(x).fetchall()
    await ctx.send(str(*result)[2:-3].replace(r'\r\n', '\r\n'))


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
    await ctx.send(
        "Мидер - герой который силен в середине и конце игры.Помогает в начале другим линиям, а далее ходит вместе с командой.")
    await ctx.send(
        "Керри - герой способный зарабатывать много золота, из-за чего ближе к концу игры становиться главным звеном команды")


@bot.command()
async def Quiz(ctx):
    global random_hero
    await ctx.send("угодайте персонажа на картинке")
    await ctx.send('запишите ответ с помошью команду >answer(пробел имя героя)')
    imgs = {'pudge': "https://virtus-img.cdnvideo.ru/images/og/plain/6c/6cb3e58326702d500847f61e932317b2.jpg",
            'Alchemist': 'https://dota2guru.ru/wp-content/uploads/2019/11/https-wallpaperspeople-com-wp-content-uploads-20.jpeg',
            'Axe': 'https://dota2ok.ru/wp-content/uploads/2017/05/Axe.jpg',
            'Bristleback': 'https://static.wikia.nocookie.net/dota2_gamepedia/images/e/e4/Bristleback_splash.jpg/revision/latest/scale-to-width-down/1200?cb=20130331022441',
            'Centaur Warrunner': 'https://dota2ok.ru/wp-content/uploads/2021/03/dota-2-centaur-warrunner.jpg',
            'Chaos Knight': 'https://1mvvi2mtud.a.trbcdn.net/img-dotaguide/2016/02/%D0%93%D0%B0%D0%B9%D0%B4-%D0%BD%D0%B0-%D1%85%D0%B0%D0%BE%D1%81-%D0%BA%D0%BD%D0%B0%D0%B9%D1%82%D0%B0.jpg',
            'Dawnbreaker': 'https://dota.gallery/images/arts/023615_dota.gallery_Dawnbreaker_1_Hero_Half-body_Digital_Art_View_straight_Pose_stand.jpg',
            'Doom': 'https://cdna.artstation.com/p/assets/images/images/017/931/856/large/cuong-le-manh-ls5.jpg?1557894344',
            'Dragon Knight': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ1FkXDFb8Bc9SQRw-KVyVUkKFHOcrOjCJXag&usqp=CAU',
            'Earth Spirit': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSV5zv85U7G5vT5Gw0jB8x0YUfci_4vaIJGQWMWPwpqOJZ4Iww-HDqQp4FPKEr4Lt_Pg9I&usqp=CAU'}
    hero = ['pudge', 'Alchemist', 'Axe', 'Bristleback', 'Centaur Warrunner', 'Chaos Knight', 'Dawnbreaker', 'Doom',
            'Dragon Knight', 'Earth Spirit']
    random_hero = random.choice(hero)
    await ctx.send(imgs[random_hero])
    print(random_hero)


@bot.command()
async def answer(ctx, *, text):
    global random_hero
    if text == random_hero:
        await ctx.send("Ты угадал героя!")
        print(random_hero)
    elif text != random_hero:
        await ctx.send("Ты не угадал героя!")
        await ctx.send(f'это был: {random_hero}')


@bot.command()
async def game_bones(ctx, *, text):
    await ctx.send("Игра - Угодай сумму костей!")
    await ctx.send("Напишите сумму подбрашенных игральных костей:")
    bones = random.randint(1, 12)
    if ctx.author == bot.user:
        return
    if text == (str(bones)):
        await ctx.channel.send(bones)
        await ctx.channel.send("Вы угодали поздрабляю!")
        await ctx.channel.send(
            "https://kartinkof.club/uploads/posts/2022-06/1654977511_1-kartinkof-club-p-kartinki-pozdravleniya-s-nagradoi-1.jpg")
    else:
        await ctx.channel.send(bones)
        await ctx.channel.send("Вы не угадали!")
        await ctx.channel.send(
            'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRhdDbF7v5HKqcKlrP-ideH6XwD3SIqUmjV1Q&usqp=CAU')


bot.run('MTA4OTE0MDM3MjAxMTIyOTIzNQ.GrudAm.3VgUTMmS6HV1w9_D2F3klQ0SNHJ_sGT5F3-Ibw')
