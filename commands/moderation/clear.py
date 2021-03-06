import asyncio
from typing import List

from discord import Client, Message, Embed

from interfaces.Command import Command
from utils.utils import CommandError


class Clear(Command):
    def __init__(self, client: Client, config):
        super().__init__("clear", client, config)
        self.delete_command = True

    async def run(self, message: Message, args: List[str]):
        if len(args) < 1:
            raise CommandError("wrong usage")

        limit = args[0]
        if not limit.isdigit():
            raise CommandError("argument must be a digit")

        await message.channel.purge(limit=int(limit))
        embed = Embed(description=f"{limit} people were PURGED!")
        msg = await message.channel.send(embed=embed)
        embed.description = f"{limit} messages were PURGED!"

        await asyncio.sleep(3)
        await msg.edit(embed=embed)
