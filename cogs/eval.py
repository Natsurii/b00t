import io
import textwrap
import traceback
import discord
import libneko
from contextlib import redirect_stdout
from discord.ext import commands

def owner(ctx):
	return ctx.message.author.id == 305998511894167552

class Eval(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self._last_result = None

	def cleanup_code(self, content):
		'Automatically removes code blocks from the code.'
		if content.startswith('```') and content.endswith('```'):
			return '\n'.join(content.split('\n')[1:(-1)])  # Remove ```py\n```

	@commands.command(hidden=True, name='eval', alias='ev')
	@commands.is_owner()	
	async def eval_a(self, ctx, *, body: str):
		'''(owner)Evaluate code''' 
		env = {
			'bot': self.bot,
			'ctx': ctx,
			'channel': ctx.channel,
			'author': ctx.author,
			'server': ctx.guild,
			'message': ctx.message,
			'_': self._last_result,
		}
		env.update(globals())
		body = self.cleanup_code(body)
		stdout = io.StringIO()
		to_compile = f'''async def func():
{textwrap.indent(body, '  ')}'''
		try:
			exec(to_compile, env)
		except Exception as e:
			return await ctx.send(f'''```py
{e.__class__.__name__}: {e}
```''')
		func = env['func']
		try:
			with redirect_stdout(stdout):
				ret = await func()
		except Exception as e:
			value = stdout.getvalue()
			await ctx.send(f'''```py
{value}{traceback.format_exc()}
```''')
		else:
			value = stdout.getvalue()
			try:
				await ctx.add_reaction('✅')
			except:
				pass
			if ret is None:
				if value:
					await ctx.send(f'''```py
{value}
```''')
			else:
				self._last_result = ret
				await ctx.send(f'''```py
{value}{ret}
```''')

			
def setup(bot):
	bot.add_cog(Eval(bot))
