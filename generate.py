from textgenrnn import textgenrnn

async def generate(no=1, prefixe=None, temp=0.5):
	async with textgenrnn(weights_path='models/OctoberModel_HL_weights.hdf5', vocab_path='models/OctoberModel_HL_vocab.json', config_path='models/OctoberModel_HL_config.json') as textgen:
		with textgen.generate(n=no, prefix=prefixe, temperature=temp, return_as_list=True) as generate_text:
			generated_text = statements
	return statements
