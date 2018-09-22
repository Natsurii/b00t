import discord
import random
import time
from discord.ext import commands

class Placeholder():
	def __init__(self,bot):
		return

	'''@commands.command(name='uptime', alias='up')
	async def uptime(self, ctx):
		shows uptime
		total_seconds = time.monotonic() - self.bot.starttime
		mins, secs = divmod(total_seconds, 60)
		hours, mins = divmod(mins, 60)
		uptime = f"{int(hours)} Hours {int(mins)} Minutes {int(secs)} Seconds"
		await ctx.send(uptime)'''

	@commands.command(name='ping')
	async def ping(self, ctx):
		'''bot's latency'''
		start = time.monotonic()
		msg = await ctx.send(':ping_pong:Pong!')
		millis = (time.monotonic() - start) * 1000
		heartbeat = ctx.bot.latency * 1000
		embed=discord.Embed(title="Bot Latency", description="The bot received your latency request.", color=0xe7aeff)
		embed.set_thumbnail(url="https://emojipedia-us.s3.amazonaws.com/thumbs/320/apple/129/table-tennis-paddle-and-ball_1f3d3.png")
		embed.add_field(name='Heres the Ball!', value=str("%.2f" %millis) + ' ms', inline=False) 
		embed.add_field(name='Average Ping to all servers.', value=str("%.2f" %heartbeat) +'ms', inline=True) 
		embed.set_footer(text="Note: Latencies are different to other servers. ") 
		await msg.edit(embed=embed)

def setup(bot):
	bot.add_cog(Placeholder(bot))
