# /bin/env python3.6
# -*- coding: utf-8 -*-

'''
MIT LICENSE
Copyright 2018 Natsurii Labs

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''
import os
import discord
from discord.ext import commands
import sys, traceback
import logging
import sys
import random
import libneko

# Variables
token = os.environ['TOKEN']
owner = [422393995642273792, 305998511894167552] 
Desc = 'Welcome to Mika ver. 0.4.5 Framework. \nThis project is still in WORK IN PROGRESS.'

initial_extensions = ['cogs.eval', 'cogs.fun', 'cogs.owner_override', 'cogs.utils',
                      'cogs.libneko.extras.superuser', 'cogs.image', 'cogs.st','jishaku']

# Logger Verbose
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Prefixes
prefixes = ['m++', 'Mika', 'Mika ']

bot = commands.Bot(command_prefix=prefixes, description=Desc, owner_id=305998511894167552)

@bot.event
async def on_ready():
    print('___  ___ _  _            _             _ ')
    print('|  \/  |(_)| |          | |           | |   ')
    print('| .  . | _ | | __  __ _ | |__    ___  | |_  ')
    print('| |\/| || || |/ / / _` || \'_ \  / _ \ | __|')
    print('| |  | || ||   < | (_| || |_) || (_) || |_ ')
    print('\_|  |_/|_||_|\_\ \__,_||_.__/  \___/  \__| \n \n')
    print('_   _                  _____       ___   ')
    print('| | | |                |  _  |     /   | ')
    print('| | | |  ___  _ __     | |/\' |    / /| |')
    print('| | | | / _ \| \'__|    |  /| |   / /_| |')
    print('\ \_/ /|  __/| |    _  \ |_/ / _ \___  | ')
    print(' \___/  \___||_|   (_)  \___/ (_)    |_/')
    print('                                        ')
    print('==========================================')

    print(f'Python Version {sys.version}')
    print(f'Discord Version {discord.__version__}')
    print(f'currently in {[str(len(bot.guilds))]} servers')

# Here we load our extensions(cogs) listed above in [initial_extensions]
for extension in initial_extensions:
    try:
        bot.load_extension(extension)
        print(f'{extension[5:]} loaded successfully.')
    except Exception as e:
        print(f'Failed to load extension {extension[5:]}.', file=sys.stderr)
        traceback.print_exc()

bot.remove_command('help')

@bot.command()
async def help(ctx):
    '''Disables the help command'''
    m = '''Help is currently disabled due to bugs.
    Help me to grow this bot!
    suggest a new command by using the command:
    `m++suggest <suggestion>`
    Thank you for contributing the bot!'''
    await ctx.send(m)


bot.run(token, bot=True, reconnect=True)
