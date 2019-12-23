from io import BytesIO

import discord
import requests
from PIL import Image, ImageFont, ImageDraw

from interfaces.Command import Command


class Img(Command):
    def __init__(self, client: discord.Client, config):
        super().__init__("img", client, config)
        self.dev_only = False

    async def run(self, message: discord.Message, args: []):
        msg = await message.channel.send("Generating Image...\nhttps://tenor.com/wYgV.gif")
        res = requests.get(message.author.avatar_url)

        img = Image.new("RGBA", (500, 500), "lightblue")
        pfp = Image.open(BytesIO(res.content))

        pfp = pfp.resize((100, 100))
        img.alpha_composite(pfp)

        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("./assets/fonts/Aller_Rg.ttf", size=20)

        draw.text((pfp.height + 2, pfp.width / 2), f"This is a test by {message.author}", font=font)

        byte = BytesIO()
        img.save(byte, format="PNG")
        byte.seek(0)
        await msg.edit(content=f'Here is the image {message.author.mention}')
        await message.channel.send(file=discord.File(byte, filename="i.png"))
