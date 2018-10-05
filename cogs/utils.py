import discord
import random
import time
from discord.ext import commands

class Utils():
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

	@commands.cooldown(rate=1,per=120,type=commands.BucketType.user)
	@commands.command()
	async def suggest(self,ctx, *, msg):
		'''Suggest a command to the bot!'''
		#this one sends the content to the server
		await ctx.bot.get_channel(497330999521312779).send(f'__**New Suggestion by {ctx.author.name}:**__\n\n`{msg} `\n```md\nBrief Info: \n------------------\n[user:]({ctx.author})\n[user_id:]({ctx.author.id})\n[server:]({ctx.guild})\n[server_id:]({ctx.guild.id})\n[channel:](#{ctx.channel})\n[channel_id:]({ctx.channel.id})\n```')
		
		await ctx.send(f'{ctx.author.mention}, your suggestion received! You can suggest again in 120 seconds.')

def setup(bot):
	bot.add_cog(Utils(bot))
