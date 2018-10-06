# basic dependencies
import discord
from discord.ext import commands

# aiohttp should be installed if discord.py is
import aiohttp

# PIL can be installed through
# `pip install -U Pillow`
from PIL import Image, ImageDraw

# partial lets us prepare a new function with args for run_in_executor
from functools import partial

# BytesIO allows us to convert bytes into a file-like byte stream.
from io import BytesIO

# this just allows for nice function annotation, and stops my IDE from complaining.
from typing import Union

dummy = 'https://cdn.discordapp.com/attachments/490068620903448577/491394502053855268/ST_design.png'

class Servertest:
    def __init__(self, bot: commands.Bot):
        # we need to include a reference to the bot here so we can access its loop later.
        self.bot = bot

        # create a ClientSession to be used for downloading avatars
        self.session = aiohttp.ClientSession(loop=bot.loop)

    async def get_avatar(self, user: Union[discord.User, discord.Member]) -> bytes:
        # generally an avatar will be 1024x1024, but we shouldn't rely on this
        avatar_url = user.avatar_url_as(format="png")

        async with self.session.get(avatar_url) as response:
            # this gives us our response object, and now we can read the bytes from it.
            avatar_bytes = await response.read()

        async with self.session.get(dummy) as r:
            frame_bytes = await r.read()

        return frame_bytes
        return avatar_bytes


    @staticmethod
    def processing(avatar_bytes: bytes) -> BytesIO:
        # we must use BytesIO to load the image here as PIL expects a stream instead of
        # just raw bytes.
        with Image.open(BytesIO(avatar_bytes)) as im:
            im.resize((1024, 1024))
            rgb_avatar = im.convert("RGB")
            with Image.open(BytesIO(frame_bytes)) as frame:
                frame.resize((1024, 1024))
                frame.paste(rgb_avatar, (0, 0))

                # prepare the stream to save this image into
                final_buffer = BytesIO()

                # save into the stream, using png format.
                frame.save(final_buffer, "png")

        # seek back to the start of the stream
        final_buffer.seek(0)

        return final_buffer

    @commands.command()
    async def stframe(self, ctx, *, member: discord.Member = None):
        """Display the user's avatar on their colour."""

        # this means that if the user does not supply a member, it will default to the
        # author of the message.
        member = member or ctx.author

        async with ctx.typing():
            # this means the bot will type while it is processing and uploading the image

            # grab the user's avatar as bytes
            avatar_bytes = await self.get_avatar(member)

            # create partial function so we don't have to stack the args in run_in_executor
            fn = partial(self.processing, avatar_bytes)

            # this runs our processing in an executor, stopping it from blocking the thread loop.
            # as we already seeked back the buffer in the other thread, we're good to go
            final_buffer = await self.bot.loop.run_in_executor(None, fn)

            # prepare the file
            file = discord.File(filename="servertest.png", fp=final_buffer)

            # send it
            await ctx.send(file=file)


# setup function so this can be loaded as an extension
def setup(bot: commands.Bot):
    bot.add_cog(Servertest(bot))
