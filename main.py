# /bin/env python3
# -*- coding: utf-8 -*-

'''
MIT LICENSE
Copyright 2018 Natsurii Labs
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''
import discord, os , sys, logging
from concurrent.futures import ThreadPoolExecutor
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext import commands
try:
    import asyncio
except ImportError:
    import trollius as asyncio

#enable Logging
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

def DiscordBot():
	prefixes = ['m++', 'Mika', 'Mika ']
	Desc = 'Welcome to Mika ver. 0.4.5 Framework. \nThis project is still in WORK IN PROGRESS.'
	bot = commands.Bot(command_prefix=prefixes, description=Desc, owner_id=305998511894167552)
	token = os.environ['TOKEN']


	@bot.event
	async def on_ready():
		print('Bot is Ready.')
		bot.remove_command('help');print('Discord Help Command removed.')

	with open('extension.txt') as xtenfile:
		xtenfile.read()

		for extension in xtenfile:
			try:
				bot.load_extension(extension)
				print(f'{extension} loaded successfully.')
			except Exception as e:
				print(f'Failed to load extension {extension}.', file=sys.stderr)
				traceback.print_exc()
	bot.run(token, bot=True, reconnect=True)

def facebookrun():
	p = Popen(['grep', 'f'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
	logging(p.decode())

	
def main():
	#scheduler = AsyncIOScheduler()
	DiscordBot()

	'''with ThreadPoolExecutor(max_workers=3) as executor:
		task1 = executor.submit(DiscordBot)'''

	#scheduler.add_job(tick, 'interval', seconds=3)
	#scheduler.start()
if __name__ == '__main__':
	main()