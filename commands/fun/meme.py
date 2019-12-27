from typing import List

import requests
from discord import Client, Message, Embed
from requests import HTTPError

from interfaces.Command import Command
from utils.utils import CommandError


class Meme(Command):
    def __init__(self, client: Client, config):
        super().__init__("meme", client, config)
        self.url = "https://meme-api.herokuapp.com/gimme/"
        self.path = config['meme-source']

    async def run(self, message: Message, args: List[str]):
        msg = await message.channel.send("Constructing meme with Baby Yoda's help...")

        if args and len(args) > 0:
            self.path = args[0]

        try:
            res = requests.get(url=f'{self.url}{self.path}')
            res.raise_for_status()

            data = res.json()
            if 'status_code' in data and data['status_code'] == 500:
                raise CommandError("That subreddit doesn't exist or something went wrong!")

            embed = Embed(title=data['title'], url=data['postLink'])
            embed.set_image(url=data['url'])
            embed.set_footer(text=f'r/{data["subreddit"]}')

            await msg.edit(content=None, embed=embed)
        except (HTTPError, CommandError) as err:
            await msg.edit(content="Baby Yoda had a mental breakdown...")
            raise CommandError(err)
        except Exception as err:
            await msg.edit(content="Baby Yoda had a mental breakdown...")
            raise Exception(err)
