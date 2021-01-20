# imports #
import discord

from discord.ext import commands

import datetime

import pause

import json

import pyshorteners

import requests

import random

from PIL import Image, ImageFont, ImageDraw

import io

from bs4 import BeautifulSoup

from discord import Activity, ActivityType

from translate import Translator


# OWM ##
from pyowm import OWM
from pyowm.utils.config import get_default_config


client = commands.Bot( command_prefix = '.' )
client.remove_command( 'help' )

hello_words = ['Команды', 'команды сервера', 'а какие команды?', 'а, какие команды сервера?',
'а, какие команды?', 'а, какие команды у бота?', 'А какие команды у бота?',
'а какие команды у бота?', 'Привет, а, какие команды у бота?',
'Привет, а какие команды у бота?','команды','а какие команды']
										###### discord #######

# New = ['С новым годом!','Новым годом','Наступающим','наступающим','с новым годом','новым годом']

@client.event
async def on_member_join(member):
	channel = client.get_channel(668385032422948868)
	await channel.send( f'Юзер `{member.name}`, присоединился к нам!')
	await channel.send(f'Количество серверов, в которых он состоит: `{member.guilds}`')
	await channel.send(f"`{member.name}`, С Новым Годом!")
@client.event
async def on_ready():
	print( "Bot connect" )
	channel = client.get_channel(66838503242294886)
	# await client.change_presence(status = discord.Status.idle)
	await client.change_presence(status=discord.Status.idle,activity=Activity(name="2020 год.",type=ActivityType.listening))

# # # J S O N # # #
@client.event
async def on_message(message):
	await client.process_commands(message)
	if message.author == client.user:
		return
	else:
		msg = message.content.split()
		for word in msg:
			if word in hello_words:
				await message.channel.send(f'{message.author.name}, для получения списка команд, напиши в чате ".help"')

				# await client.add_reaction(member.message, "🎄")

	with open('E:\\Programs\\python\\lvl.json','r') as f:
		users = json.load(f)
	async def update_data(users,user):
		if not user in users:
			users[user] = {}
			users[user]['exp'] = 0
			users[user]['lvl'] = 1
	async def add_exp(users,user,exp):
		users[user]['exp'] += exp
	async def add_lvl(users,user):
		exp = users[user]['exp']
		lvl = users[user]['lvl']
		if exp > lvl:
			await message.channel.send('Чат "{}", поздравляет вас, {}, с повышенным рангом.'.format(message.channel.name,message.author.mention))
			users[user]['exp'] = 0
			users[user]['lvl'] = lvl + 1
	await update_data(users,str(message.author.id))

	await add_exp(users,str(message.author.id),0.1)

	await add_lvl(users,str(message.author.id))

	with open('E:\\Programs\\python\\lvl.json','w') as f:
		json.dump(users,f)


@client.event
async def on_command_error(ctx,error):
	pass
#RULES
@client.command(aliases = ['правила', 'рулес'])
async def rules(ctx, amount = 1):
	await ctx.channel.purge(limit = 1)
	author = ctx.message.author
	await ctx.send(f'Привет {author.mention}! Правила сервера очень просты!:\n1.`Не ругаться` на сервере!\n2.`Не обзывать` товарища по серверу, или по игре!\n3.Просто, уважайте друг,друга.')

# # #  J  S  O   N  # # #

@client.command(aliases = ['лвл','ранг','уровень','exp','опыт','ехп'])
async def rank(ctx, member: discord.Member):
	await ctx.channel.purge(limit = 1)

	with open('E:\\Programs\\python\\lvl.json','r') as f:
		money = json.load(f)

	emb = discord.Embed(title=f'`Уровень, и Exp`')
	emb.add_field( name = f"У {member}", value = f'{money[str(member.id)]["lvl"]} `лвл`', inline = False)

	emb.add_field( name = f"Exp", value = f'{round(money[str(member.id)]["exp"])} `Exp`', inline = False)
	emb.set_thumbnail(url = member.avatar_url)

	await ctx.send(embed = emb)


#CLEAR
@client.command(aliases = ['клеар','очистить','очистка'])
@commands.has_permissions(administrator = True)
async def clear(ctx, amount: int):
	author = ctx.message.author

	emb = discord.Embed(title=f' {author}, Очищенно!', colour = discord.Color.green())

	emb.set_author(name = client.user.name, icon_url = client.user.avatar_url)

	await ctx.channel.purge(limit = amount)

	await ctx.send( embed = emb)
	pause.seconds(5)
	await ctx.channel.purge(limit = 1)
	pause.seconds(0)
#KICK, BAN
@client.command(aliases = ['кик','кикнут','выгнать'])
@commands.has_permissions(administrator = True)
async def kick(ctx, member: discord.Member, *, reason = None):
	await ctx.channel.purge(limit = 1)

	await member.kick(reason = reason)
	await ctx.send(f'Пользователь {member.mention} был кикнут!')

# SECRET COMMAND
@client.command(aliases = ['хак','хакнуть'])
@commands.has_permissions(administrator = True)
async def hack( ctx, member: discord.Member):
	await ctx.channel.purge(limit = 1)
	i = 0
	while i < 20:
		await member.send(i*2)
		i += 1

#HELP
@client.command(aliases = ['время','тайм','дата'])
async def time( ctx ):
	await ctx.channel.purge(limit = 1)
	date = datetime.datetime.today()
	new_date  = date.strftime("%Y.%m.%d %H:%M:%S")

	emb = discord.Embed(title="Время, и сегодняшняя дата", colour = discord.Color.blue())

	emb.set_author(name = client.user.name, icon_url = client.user.avatar_url)


	emb.add_field(name = 'Время, и дата: ', value = "`{}`".format(new_date))

	await ctx.send( embed = emb)

@client.command(aliases =['хелп','помощь','Помощь'])
async def help(ctx, amount = 1):
	await ctx.channel.purge(limit = 1)
	emb = discord.Embed(title="<Команды сервера/>", colour = discord.Color.green())

	emb.set_author(name = client.user.name, icon_url = client.user.avatar_url)

	emb.add_field(name = '`{}кикнуть`'.format('.'), value = "<Кикнуть пользователя из сервера/>",inline = False)

	emb.add_field(name = '`{}очистить`'.format('.'), value = "<Очистка чата/>",inline = False)

	emb.add_field(name = '`{}правила`'.format('.'), value = "<Правила/>",inline = False)

	emb.add_field(name = '`{}помощь`'.format('.'), value = "Помощь по командам",inline = False)

	emb.add_field(name = '`{}время`'.format('.'), value = "Время",inline = False)

	emb.add_field(name = '`{}кот`'.format('.'), value = "Выведет в чат рандомного кота",inline = False)

	emb.add_field(name = '`{}лис`'.format('.'), value = "Выведет в чат рандомную лису",inline = False)

	emb.add_field(name = '`{}панда`'.format('.'), value = "***Выведет в чат КоПанду!***",inline = False)

	emb.add_field(name = '`{}мемы`'.format('.'), value = "Выведет в чат рандомый мем",inline = False)

	emb.add_field(name = '`{}курс`'.format('.'), value = "***Показывает текущий курс доллара***",inline = False)

	emb.add_field(name = '`{}погода☁`'.format('.'), value = "***☁Сегодняшняя, погода☁***",inline = False)

	emb.add_field(name = '`{}ковид`'.format('.'), value = "***Статистика КоВид***",inline = False)

	emb.add_field(name = '`{}факт`'.format('.'), value = "***Выведет в чат рандомный факт***",inline = False)

	emb.add_field(name = '`{}юзер`'.format('.'), value = "Виведет в чат информацию о пользователе",inline = False)

	emb.add_field(name = '`{}реши`'.format('.'), value = "Бот, решает любой пример, за тебя!",inline = False)

	emb.add_field(name = '`{}уровень/ранг`'.format('.'), value = "Посмотреть какой у вас уровень/опыт!",inline = False)

	emb.add_field(name = '`{}game`'.format('.'), value = "Выведет информацию об ***игре***",inline = False)

	emb.add_field(name = '`{}переведи`'.format('.'), value = "Бот переведет Английское слово на Русское",inline = False)

	emb.add_field(name = '`{}сократи`'.format('.'), value = "Бот сократит любую ссылку!",inline = False)

	emb.add_field(name = '***{}hack***'.format('.'), value = "♠Секретная команда, доступна только администраторам!♠",inline = False)

	await ctx.send( embed = emb)
@client.command(aliases = ['число'])
async def number(ctx, num1:int, num2:int):
	number3 = random.randint(num1, num2)
	await ctx.send(f"Сгенерированное число - {number3}")

# @client.command(aliases = ['вибери'])
# async def users(ctx):
# # 	@Crampy-Mo, @🎃🐯OvechiyDrift👹💞 , @Quattro, @mORON @FanOrMan @𝖏𝖔𝖕𝖆_𝕾𝖌𝖔𝖗𝖊𝖑𝖆
# # @NICEL
# # @Ilia's_house
# 	user2= random.choice(users)
# 	await ctx.send(f'Победитель - {user2}')
# 	user2.remove()
# users = ['@🎃🐯OvechiyDrift👹💞','@Quattro','@𝖏𝖔𝖕𝖆_𝕾𝖌𝖔𝖗𝖊𝖑𝖆',"@Ilia's_house",'@PROGER']

@client.command(aliases = ['лиса','фокс','лис',])
async def fox(ctx):
    response = requests.get('https://some-random-api.ml/img/fox') # Get-запрос
    json_data = json.loads(response.text) # Извлекаем JSON

    await ctx.channel.purge(limit = 1)
    embed = discord.Embed(color = 0xff9900, title = 'Random Fox') # Создание Embed'a
    embed.set_image(url = json_data['link']) # Устанавливаем картинку Embed'a
    await ctx.send(embed = embed) # Отправляем Embed


@client.command(aliases = ['кот','кет'] )
async def cat(ctx):
    response = requests.get('https://some-random-api.ml/img/cat') # Get-запрос
    json_data = json.loads(response.text) # Извлекаем JSON
    await ctx.channel.purge(limit = 1)
    embed = discord.Embed(color = discord.Color.blue(), title = 'Random Cat') # Создание Embed'a
    embed.set_image(url = json_data['link']) # Устанавливаем картинку Embed'a
    await ctx.send(embed = embed) # Отправляем Embed
# https://some-random-api.ml/img/panda


@client.command(aliases = ['копанда','панда'] )
async def panda(ctx):
    response = requests.get('https://some-random-api.ml/img/panda') # Get-запрос

    json_data = json.loads(response.text) # Извлекаем JSON


    await ctx.channel.purge(limit = 1)
    embed = discord.Embed(color = discord.Color.green(), title = 'Panda') # Создание Embed'a

    embed.set_image(url = json_data['link']) # Устанавливаем картинку Embed'a

    await ctx.send(embed = embed) # Отправляем Embed

@client.command(aliases= ['мемы','мем'])
async def meme(ctx):
    response = requests.get('https://some-random-api.ml/meme') # Get-запрос
    json_data = json.loads(response.text) # Извлекаем JSON

    await ctx.channel.purge(limit = 1)
    embed = discord.Embed(color = discord.Color.green(), title = 'Random Meme!') # Создание Embed'a

    embed.set_image(url = json_data['image']) # Устанавливаем картинку Embed'a

    await ctx.send(embed = embed) # Отправляем Embed

@client.command( aliases = ['погода','погод'] )
async def weather(ctx, weat):
	await ctx.channel.purge(limit = 1)
	await ctx.send('`Подгружаем...`')


	owm = OWM('6133571e97e6e196f69c80d19035fc82')
	# city_words = ['Москва, Россия','Харьков, Украина','Гонконг','Бангкок, Таиланд']

	# city = random.choice(city_words)

	city = weat


	config_dict = get_default_config()
	config_dict['language'] = 'ru'  # your language here

	mgr = owm.weather_manager()
	observation = mgr.weather_at_place(city)

	w = observation.weather

	status_w = w.detailed_status

	temp = w.temperature('celsius')['temp']

	wind = w.wind()['speed']
	await ctx.channel.purge(limit = 1)
	emb = discord.Embed(title="Погода, и сегодняшняя температура", colour = discord.Color.blue())

	emb.set_author(name = client.user.name, icon_url = client.user.avatar_url)
	emb.add_field(name = 'В городе/стране, {}, сейчас температура: '.format(city), value = "***{}°C***".format(temp), inline = False)

	emb.add_field(name = 'Скорость ветра: ', value = "***{}, м/с***".format(wind), inline = False)

	emb.add_field(name = 'Статус: ', value = "***{}***".format(status_w), inline = False)

	await ctx.send( embed = emb)

@client.command(aliases = ['курс','доллар','курсдоллара','долар','курсдолара'])
async def dollar(ctx):
	await ctx.channel.purge(limit = 1)
	# BS4 # BeautifulSoup #
	await ctx.send('`Подгружаем...`')
	DOLLAR_RUB = 'https://www.google.com/search?q=%D0%BA%D1%83%D1%80%D1%81+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D0%B0&oq=rehc&aqs=chrome.1.69i57j0l7.2098j0j7&sourceid=chrome&ie=UTF-8'

	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'}
	full_page = requests.get(DOLLAR_RUB, headers=headers)

	soup = BeautifulSoup(full_page.content, 'html.parser')

	convert = soup.findAll('span', {'data-precision':2})

	convert = convert[0].text

	await ctx.channel.purge(limit = 1)

	emb = discord.Embed(title="Один доллар США равен", colour = discord.Color.green())

	emb.set_author(name = client.user.name, icon_url = client.user.avatar_url)

	emb.add_field(name='⠀', value='`{}`, Украинских гривен'.format(convert))

	await ctx.send( embed = emb )




@client.command(aliases = ['замутить','замютить','мют','мут'])
@commands.has_permissions(administrator = True)
async def user_mute(ctx, member: discord.Member, time:int, reason):
	await ctx.channel.purge( limit = 1)

	role = discord.utils.get(ctx.guild.roles,id = 745244237657800857)

	await member.add_roles(role)
	emb = discord.Embed(title="Мут",color= discord.Color.red())

	emb.add_field(name='Модератор',value=ctx.message.author.mention,inline=False)

	emb.add_field(name='Нарушитель',value=member.mention,inline=False)

	emb.add_field(name='Причина',value=reason,inline=False)

	emb.add_field(name="Время",value='{}, минут'.format(time),inline=False)

	emb.set_author(name = client.user.name, icon_url = client.user.avatar_url)

	await ctx.send(embed = emb)

	await asyncio.sleep(time * 60)

	await member.remove_roles(user_role)

@client.command(aliases = ['сервер'])
async def server(ctx):
	await ctx.channel.purge( limit = 1)
	emb = discord.Embed(title='Server', color = discord.Color.blue())
	emb.add_field(name = "Owner", value =ctx.guild.owner)
	emd.add_field(name = "Region", value =ctx.guild.region)
	# emd.add_field(name = "Members", value =f"{len(ctx.guild.members)}")
	# emd.add_field(name = "Roles", value =f"{len(ctx.guild.roles)}")
	await ctx.send(embed = emb)

@client.command(aliases = ['инфо','юзер','пользователь'])
async def info(ctx, member: discord.Member):


	late = Translator(from_lang="en", to_lang="ru")

	text = str(member.status)

	text2 = late.translate(text)


	emb = discord.Embed(title='Информация о `Пользователе`', color = discord.Color.blue())

	emb.add_field(name = "Когда присоединился ", value = member.joined_at, inline = False)

	emb.add_field(name = "Имя ", value = member.display_name, inline = False)

	emb.add_field(name = "Статус ", value = text, inline = False)

	# emb.add_field(name = "Роли  ", value = member.roles, inline = False)

	emb.set_thumbnail(url = member.avatar_url)

	emb.add_field(name = "Айди", value = member.id, inline = False)

	emb.add_field(name = "Аккаунт был создан: ", value = member.created_at.strftime("%a,%#d %B %Y, %I:%M %p UTC"), inline = False)
	await ctx.send( embed = emb)


@client.command(aliases = ['переведи','перевод'])
async def translate(ctx, text):
	late = Translator(from_lang="en", to_lang="ru")

	text2 = late.translate(text)

	emb = discord.Embed(title="Перевод слова '{}'".format(text), colour = discord.Color.green())

	emb.add_field(name='Перевод ', value='`{}`'.format(text2))

	await ctx.send(embed = emb)



@client.command(aliases = ['корона','коронастатистика','ковид','ковид-19'])
async def coronavirus(ctx):
	await ctx.channel.purge(limit=1)
	# CORONA VI .. #
	await ctx.send('`Подгружаем...`')

	emb = discord.Embed(title="Статистика `КоВид-19` в Украине", colour = discord.Color.green())

	emb.set_author(name = client.user.name, icon_url = client.user.avatar_url)
	Corona_Stats = 'https://www.google.com/search?q=%D0%BA%D0%BE%D1%80%D0%BE%D0%BD%D0%B0%D0%B2%D0%B8%D1%80%D1%83%D1%81+%D1%81%D1%82%D0%B0%D1%82%D0%B8%D1%81%D1%82%D0%B8%D0%BA%D0%B0&oq=%D0%BA%D0%BE%D1%80%D0%BE%D0%BD%D0%B0%D0%B2%D0%B8%D1%80%D1%83%D1%81+%D1%81%D1%82%D0%B0%D1%82&aqs=chrome.0.0j69i57j0l6.8134j0j7&sourceid=chrome&ie=UTF-8'
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'}
	full_stats = requests.get(Corona_Stats, headers=headers)

	stats = BeautifulSoup(full_stats.content, 'html.parser')
	cor = stats.findAll('div', {'jsname':'fUyIqc'})

	cor = cor[0].text
	live = stats.findAll('div', {'jsname':'fUyIqc'})
	live = live[2].text
	await ctx.channel.purge(limit=1)
	emb.add_field(name='Заболевших: ', value='`{}`'.format(cor))
	emb.add_field(name='Выздровевших: ', value='`{}`'.format(live))

	await ctx.send( embed = emb )



@client.command(aliases = ['карта','я'])
async def card(ctx):
	await ctx.channel.purge(limit = 1)

	img = Image.new('RGBA', (400, 130), '#36393f')

	url = str(ctx.author.avatar_url)[:-10]

	response = requests.get(url, stream = True)

	response = Image.open(io.BytesIO(response.content))

	response = response.convert('RGBA')

	response = response.resize((100,100), Image.ANTIALIAS)

	img.paste(response, (15,15,115,115))
	idraw = ImageDraw.Draw(img)

	name = ctx.author.name

	tag = ctx.author.discriminator
	headline = ImageFont.truetype('arial.ttf', size = 20)

	undertext = ImageFont.truetype('arial.ttf', size = 12)

	idraw.text((145,15), f'{name}#{tag}', font = headline)

	idraw.text((145,50), f'ID: {ctx.author.id}', font = undertext)

	img.save('user.png')

	await ctx.send(file = discord.File(fp = 'user.png'))



@client.command(aliases = ['сслыка','сократи','сылка'])
async def urll(ctx, urls: str):

	s = pyshorteners.Shortener()

	ur = s.tinyurl.short(urls)

	await ctx.send('Вот сокращенная ссылка: {}'.format(ur))

@client.command(aliases = ['факт','случайнныйфакт'])
async def fact(ctx):
	fact = "https://randstuff.ru/fact/"
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'}
	full_fact = requests.get(fact, headers=headers)

	soup_fact = BeautifulSoup(full_fact.content, 'html.parser')

	factname = soup_fact.findAll('td')

	factname = factname[0].text

	emb = discord.Embed(title="Случайнный `Факт`", colour = discord.Color.green())

	emb.set_author(name = client.user.name, icon_url = client.user.avatar_url)

	emb.add_field(name = '⠀', value='`{}`'.format(factname))

	await ctx.send(embed = emb)


@rank.error
async def rank_error(ctx,error):
	if isinstance(error, commands.MissingRequiredArgument ):
		await ctx.send(f'{ctx.author.name}, напишите имя пользователя, у которого вы хотите узнать, статистику. Пример .rank @Name')
@user_mute.error
async def mute_error(ctx,error):
	if isinstance(error, commands.MissingRequiredArgument ):
		await ctx.send(f'{ctx.author.name}, напишите имя пользователя которого хотите замьючить, время, а так-же причину.')

@client.command(aliases = ['подсчитай','калкулатор','считай','реши'])
async def calculator(ctx, num1:int,plus,num2:int):

	if plus == "+":
		prin = str(num1) + " + " + str(num2)
		result = num1 + num2
		emb = discord.Embed(title="Пример: `{}`".format(prin), colour = discord.Color.green())

		emb.set_author(name = client.user.name, icon_url = client.user.avatar_url)

		emb.add_field(name = 'Результат: ', value='`{}`'.format(result))

		await ctx.send(embed = emb)


	elif plus == "%":

		prin = str(num1) + " % " + str(num2)

		result = num1 % num2

		emb = discord.Embed(title="Пример: `{}`".format(prin), colour = discord.Color.green())

		emb.set_author(name = client.user.name, icon_url = client.user.avatar_url)

		emb.add_field(name = 'Результат: ', value='`{}`'.format(result))

		await ctx.send(embed = emb)


	elif plus == "**":

		prin = str(num1) + " ** " + str(num2)

		result = num1 ** num2

		emb = discord.Embed(title="Пример: `{}`".format(prin), colour = discord.Color.green())

		emb.set_author(name = client.user.name, icon_url = client.user.avatar_url)

		emb.add_field(name = 'Результат: ', value='`{}`'.format(result))

		await ctx.send(embed = emb)

	elif plus == "-":
		prin = str(num1) + " - " + str(num2)
		result = num1 - num2
		emb = discord.Embed(title="Пример: `{}`".format(prin), colour = discord.Color.green())

		emb.set_author(name = client.user.name, icon_url = client.user.avatar_url)

		emb.add_field(name = 'Результат: ', value='`{}`'.format(result))

		await ctx.send(embed = emb)
	elif plus == "/":
		if num2 == 0:
			await ctx.send("Делить на ноль нельзя.")
		else:
			prin = str(num1) + " / " + str(num2)
			result = num1 / num2
			emb = discord.Embed(title="Пример: `{}`".format(prin), colour = discord.Color.green())

			emb.set_author(name = client.user.name, icon_url = client.user.avatar_url)

			emb.add_field(name = 'Результат: ', value='`{}`'.format(result))
			await ctx.send(embed = emb)
	elif plus == "*":
		prin = str(num1) + " * " + str(num2)
		result = num1 * num2
		emb = discord.Embed(title="Пример: `{}`".format(prin), colour = discord.Color.green())

		emb.set_author(name = client.user.name, icon_url = client.user.avatar_url)

		emb.add_field(name = 'Результат: ', value='`{}`'.format(result))

		await ctx.send(embed = emb)

@client.command(aliases = ['игра'])
async def game_start(ctx, num1:int ):

	b = datetime.datetime.now()
	number = random.randint(6,50)

	nullnumber = random.randint(50,70)

	supernullnumber = random.randint(1,5000)
	print('{}'.format(number))
	if num1 == nullnumber:
		number = random.randint(25,30)
		await ctx.send('Шанс на получение пасхалки, увеличен.')
	elif num1 == number:
		number2 = random.randint(0,50)
		await ctx.send('Ты угадал моё число!\nПоздравляю!\nОтвет {} '.format(number))
		await ctx.send('Ты получил +{} exp.'.format(number2))
		with open('E:\\python\\lvl.json','r') as f:
			users = json.load(f)
		if b.hour == 9:
			async def add_lvl(users,user):
				exp = users[user]['exp']
				lvl = users[user]['lvl']
				users[user]['exp'] = exp + number2 * 2
				await add_lvl(users,str(ctx.author.id))
		elif b.hour == 16:

			async def add_lvl(users,user):
				exp = users[user]['exp']
				lvl = users[user]['lvl']
				users[user]['exp'] = exp + number2 * 4
				await add_lvl(users,str(ctx.author.id))
		elif b.hour == 23:
			async def add_lvl(users,user):
				exp = users[user]['exp']
				lvl = users[user]['lvl']
				users[user]['exp'] = exp + number2 * 6
				await add_lvl(users,str(ctx.author.id))
		else:
			async def add_lvl(users,user):
				exp = users[user]['exp']
				lvl = users[user]['lvl']
				users[user]['exp'] = exp + number2
			number -= nullnumber
			supernullnumber = supernullnumber / nullnumber
		await add_lvl(users,str(ctx.author.id))
		with open('E:\\python\\lvl.json','w') as f:
			json.dump(users,f)

	if num1 == supernullnumber:
		lvl_up = random.randint(10,15)
		await ctx.send('***Ты получил самую редкую пасхалку в этой игре!\nНаграда: {} lvl***'.format(lvl_up))
		with open('E:\\python\\lvl.json','r') as f:
			users = json.load(f)
		async def add_lvl(users,user):
			exp = users[user]['exp']
			lvl = users[user]['lvl']
			users[user]['lvl'] = lvl + lvl_up
		await add_lvl(users,str(ctx.author.id))

		with open('E:\\python\\lvl.json','w') as f:
			json.dump(users,f)
	if number == 28:
		if num1 == 28:
			number2 = random.randint(100,5000)

			await ctx.send('Ты получил пасхалку на Detroit, 28 ударов ножом! \nПоздравляю!')

			await ctx.send('Ты получил +{} exp.'.format(number2))

			with open('E:\\python\\lvl.json','r') as f:
				users = json.load(f)
			async def add_lvl(users,user):
				exp = users[user]['exp']
				lvl = users[user]['lvl']
				users[user]['exp'] = exp + number2
			await add_lvl(users,str(ctx.author.id))
			with open('E:\\python\\lvl.json','w') as f:
				json.dump(users,f)
			number = random.randint(1,50)
	elif num1 > number:
		await ctx.send('Много,\nпопробуй написать по меньше.')

	elif num1 < number:
		await ctx.send('Мало,\nпопробуй написать по больше.')


@client.command(aliases = ['миниигра','минигра','играть'])
async def game(ctx):
		await ctx.send('Правила игры: Я загадую число (от 1 до 50), твоя задача: \nугадать какое число я загадал, если ты будешь писать не правильный ответ, я буду тебе подсказывать,\nмало или много.\n Для того что-бы начать игру напиши в чате ".game_start" или ".игра"\nMAX Награда: от 100 до 500 lvl.')


@rank.error
async def rank_error(ctx,error):
	if isinstance(error, commands.MissingRequiredArgument ):
		await ctx.send(f"{ctx.author.name}, напишите, пользователя у когорого хотите узнать ранг. Пример .ранг @Name")
@weather.error
async def weat_error(ctx,error):
	if isinstance(error, commands.MissingRequiredArgument ):
		await ctx.send(f"{ctx.author.name}, напишите, в каком городе/стране,  вы хотите узнать погоду. Пример .погода Киев")
@urll.error
async def url_error(ctx,error):
	if isinstance(error, commands.MissingRequiredArgument ):
		await ctx.send(f"{ctx.author.name}, напишите, какую ссылку вы хотите сократить. Пример .сократить https:/google.com/search")

@calculator.error
async def calculator_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument ):
		await ctx.send(f"{ctx.author.name}, напишите диапазон чисел. Пример .calculator 30 - 12")



@hack.error
async def hack_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument ):
		await ctx.send(f'{ctx.author.name}, напишите, кого вы хотите хакнуть.')
		if isinstance(error, commands.MissingPermissions):
			await ctx.send(embed = discord.Embed(description = f'{ctx.author.name}, у вас не достаточно прав на выполнение этой команды.', colour = discord.Color.red()))
@clear.error
async def clear_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument ):
		await ctx.send(f'{ctx.author.name}, напишите, сколько вы хотите, очистить текста. Пример .clear 5')
	if isinstance(error, commands.MissingPermissions):
		await ctx.send(embed = discord.Embed(description = f'{ctx.author.name}, у вас не достаточно прав на выполнение этой команды.', colour = discord.Color.red()))
		if isinstance(error, commands.MissingPermissions):
			await ctx.send(embed = discord.Embed(description = f'{ctx.author.name}, у вас не достаточно прав на выполнение этой команды.', colour = discord.Color.red()))
@kick.error
async def kick_error(ctx, error):
	if isinstance(error, commands.MissingPermissions):
		await ctx.send(embed = discord.Embed(description = f'{ctx.author.name}, у вас не достаточно прав на выполнение этой команды.', colour = discord.Color.red()))
@client.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandNotFound ):
		await ctx.channel.purge(limit = 1)
		await ctx.send(embed = discord.Embed(description = f'{ctx.author.name}, такой команды не существует. Проверить список комманд можно написав .help, в чате', colour = discord.Color.red()))
token = open( "token.txt", 'r' ).readline()

client.run( token )
