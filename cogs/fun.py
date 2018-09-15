#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

'''
MIT LICENSE
Copyright 2018 Natsurii Labs

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''
import discord
import random
from discord.ext import commands

class Fun():
	def __init__(self,bot):
		return

	@commands.command(name='truth')
	async def truth(self, ctx, *, msg):
		'''You gotta tell me a question and I will answer it if it is True or False.'''
		
		cha = random.choice(['Hinde', 
			'100% Sure', 
			'Hindi ko alam', 
			'malay ko', 
			'ewan ko ba', 
			'Di ko masasagot yan', 
			'pagiisapan ko pa', 
			'Oo na lang ako', 
			'Di ko sure',
			'anong klaseng tanong yan?', 
			'Tanong mo nalang kay Batman', 
			'Yes na yes', 
			'Uu', 
			'True pa sa dede mo',
			'Tama ka dyan',
			'I Absolutely Agree',
			'Tumpak ka dyan',
			'Mali ka dyan',
			'👍',
			'👎'])
	
		await ctx.send(f'Question: {msg} \n Answer: {cha}, {ctx.author.name}')

	@commands.command()
	async def flip(self, ctx):
		'''Just a Flipcoin command'''
		
		embed = discord.Embed(title='\N{ZERO WIDTH SPACE}', description='\N{ZERO WIDTH SPACE}', color=0x2C2F33)
		
		face = random.choice(['Heads', 'Tails'])
		
		if face == 'Heads':
			embed.set_image(url="https://cdn.discordapp.com/attachments/490643354779123733/490643408327540773/heads.png")
			embed.add_field(name=f'**{ctx.author.mention}**, The coin Lands on *Heads*!', value='\N{ZERO WIDTH SPACE}')
		
		else:
			embed.set_image(url="https://cdn.discordapp.com/attachments/490643354779123733/490643410471092224/tails.png")
			embed.add_field(name=f'**{ctx.author.mention}**, The coin Lands on *Tails*!', value='\N{ZERO WIDTH SPACE}')

		await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(Fun(bot))
