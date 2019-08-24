import discord
from discord.ext import commands
from textgenrnn import textgenrnn

class HeadlineGeneration(commands.Cog):
	def __init___(self, bot):
		return

	@commands.command()
	async def generate(self, ctx):
		async with textgenrnn(weights_path='models/OctoberModel_HL_weights.hdf5', vocab_path='models/OctoberModel_HL_vocab.json', config_path='models/OctoberModel_HL_config.json') as textgen:
			async with textgen.generate(n=1, temperature=0.5, return_as_list=False) as generate_text:
				generated_text = statements
		await ctx.send(str(statements))


def setup(bot):
    bot.add_cog(HeadlineGeneration(bot))