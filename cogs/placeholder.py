import discord
import random
from discord.ext import commands

class Placeholder():
	def __init__(self,bot):
		return

	@commands.command(hidden='#bool', name='', alias='')
	async def function():
		pass

def setup(bot):
	bot.add_cog(Placeholder(bot))
