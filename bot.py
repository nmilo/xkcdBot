import discord
from discord.ext import commands

import requests
import random as randomGen

import re

TOKEN = 'your-token'

description = '''xkcdBot Discord '''

bot = commands.Bot(command_prefix='xkcd ', description=description)
bot.remove_command('help')

latest_num = requests.get(url='https://xkcd.com/info.0.json').json()['num']

RE = re.compile(r"""\[\[(File|Category):[\s\S]+\]\]|
        \[\[[^|^\]]+\||
        \[\[|
        \]\]|
        \'{2,5}|
        (<s>|<!--)[\s\S]+(</s>|-->)|
        {{[\s\S\n]+?}}|
        <ref>[\s\S]+</ref>|
        ={1,6}""", re.VERBOSE)

def unwiki(wiki, compress_spaces=None):
	'''
	Parse a string to remove and replace all wiki markup tags
	'''
	result = RE.sub('', wiki)
	if compress_spaces:
		result = re.sub(r' +', ' ', result)
	return result


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def help(ctx):
	"""Help command"""
	embed = discord.Embed(
		title = 'xkcdBot Help',
		colour = discord.Colour.light_grey()	
	)
	embed.add_field(name='xkcd help', value='Show this help', inline=False)
	embed.add_field(name='xkcd random', value = 'Shows random xkcd comic', inline=False)
	embed.add_field(name='xkcd comic <number>', value='Shows comic with given number', inline=False)
	embed.add_field(name='xkcd latest', value='Shows the latest comic', inline=False)
	embed.add_field(name='xkcd explain <number>', value='Explains the given comic', inline=False)
	embed.add_field(name='xkcd search <title>', value='Search comic by title', inline=False)
	embed.add_field(name='Invite URL', value="[Click Here To Invite bot](https://discordapp.com/oauth2/authorize?client_id=511586762657628161&scope=bot&permissions=387136)", inline=False)
	embed.add_field(name='Support Server', value="[Click Here To Join Support Server](https://discord.gg/sz9xrgP)", inline=False)
		
	await ctx.send(embed=embed)



@bot.command()
async def comic(ctx, number : int):
	"""Fetches latest xkcd comic"""
	url = 'https://xkcd.com/{}/info.0.json'.format(number)
	r = requests.get(url=url).json()
	embed = discord.Embed(
		title = 'Latest xkcd Comic: #'+str(r['num']),
		colour = discord.Colour.light_grey()	
	)
	embed.set_image(url=r['img'])
	embed.add_field(name='Comic title', value=r['title'], inline=True)
	embed.add_field(name='Publish Date', value=	'{}-{}-{}'.format(r['year'], r['month'], r['day']), inline=True)
	embed.add_field(name='Comic Alt Text', value=r['alt'], inline=True)	
	await ctx.send(embed=embed)

@bot.command()
async def random(ctx):
	"""Gives random xkcd comic"""
	number = randomGen.randint(1, latest_num)
	url = 'https://xkcd.com/{}/info.0.json'.format(number)
	r = requests.get(url=url).json()
	embed = discord.Embed(
		title = 'xkcd Comic: #'+str(r['num']),
		colour = discord.Colour.light_grey()	
	)
	embed.set_image(url=r['img'])
	embed.add_field(name='Comic title', value=r['title'], inline=True)
	embed.add_field(name='Publish Date', value=	'{}-{}-{}'.format(r['year'], r['month'], r['day']), inline=True)
	embed.add_field(name='Comic Alt Text', value=r['alt'], inline=True)	
	await ctx.send(embed=embed)

@bot.command()
async def latest(ctx):
	"""Fetches latest xkcd comic"""
	r = requests.get(url='https://xkcd.com/info.0.json').json()
	embed = discord.Embed(
		title = 'Latest xkcd Comic: #'+str(r['num']),
		colour = discord.Colour.light_grey()	
	)
	embed.set_image(url=r['img'])
	embed.add_field(name='Comic title', value=r['title'], inline=True)
	embed.add_field(name='Publish Date', value=	'{}-{}-{}'.format(r['year'], r['month'], r['day']), inline=True)
	embed.add_field(name='Comic Alt Text', value=r['alt'], inline=True)	
	await ctx.send(embed=embed)

@bot.command()
async def search(ctx, query: str):
	"""Search xkcd comic by title"""

@bot.command()
async def explain(ctx, number : int):
	"""Gives explaination for a given xkcd"""
	url = 'https://xkcd.com/{}/info.0.json'.format(number)
	r = requests.get(url=url).json()

	
	explain_url = 'https://www.explainxkcd.com/wiki/api.php?action=parse&format=json&prop=wikitext&section=1&page='+str(r['num'])+':_'+r['title']
	explain_data = requests.get(url=explain_url).json()
	explain_data = explain_data['parse']['wikitext']['*']

	string  = explain_data
	for index,chunk in enumerate([string[i:i+1000] for i in range(0, len(string), 1000)]):
		embed = discord.Embed(
			title = 'xkcd Comic: #{} Explained (#{})'.format(str(r['num']), index+1),
			colour = discord.Colour.light_grey()	
		)
		if(index==0):
			embed.add_field(name='Comic title', value=r['title'], inline=False)
		embed.add_field(name='Explanation', value=unwiki(chunk,True), inline=False)
		await ctx.send(embed=embed)

bot.run(TOKEN)