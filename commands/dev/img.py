import math
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
        pic_format = 'png'
        if message.author.is_avatar_animated():
            pic_format = 'gif'

        res = requests.get(message.author.avatar_url_as(static_format=pic_format))

        img = Image.new("RGBA", (1280, 650), "lightblue")
        pfp = Image.open(BytesIO(res.content))
        pfp = pfp.resize((500, 500))

        pic_mid = math.floor(img.height / 2)
        pfp_mid = math.floor(pfp.height / 2)

        img.alpha_composite(pfp, (40, pic_mid - pfp_mid))

        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("./assets/fonts/Aller_Rg.ttf", size=60)

        draw.text((pfp.height + 50, pic_mid - 10), f"This is a test by\n{message.author}", font=font, fill="black")

        img = img.convert('RGB')

        byte = BytesIO()
        img.save(byte, format="JPEG", quality=25)
        byte.seek(0)
        await msg.edit(content=f'Here is the image {message.author.mention}')
        await message.channel.send(file=discord.File(byte, filename="i.jpg"))
