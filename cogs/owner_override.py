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
from discord.ext import commands

class Owner():
	def __init__(self,bot):
		return

	@commands.command(hidden=True, name='image_embed', alias='ie')
	@commands.is_owner()
	async def image_embed(self, ctx, id, *, img):
		'''Image Embed'''
		embed = discord.Embed(title='\N{ZERO WIDTH SPACE}', description='\N{ZERO WIDTH SPACE}', color=0x36393E)
		embed.set_image(url=img)
		await ctx.bot.get_channel(id).send(embed=embed)

	@commands.command(hidden=True, name='pokespoof', alias='poke')
	@commands.is_owner()
	async def image_embed(self, ctx, id, *, img):
		'''Image Embed'''
		embed = discord.Embed(title='A wild pokémon has appeared!', description='Guess the pokémon and type p!catch <pokémon> to catch it!', color=0x00AF87)
		embed.set_image(url=img)
		await ctx.bot.get_channel(id).send(embed=embed)

	@commands.command(hidden=True, name='echo', alias='ec')
	@commands.is_owner()
	async def echo(self, ctx, id, *, msg):
		'''echo powers'''
		await ctx.bot.get_channel(id).send(msg)

def setup(bot):
	bot.add_cog(Owner(bot))
