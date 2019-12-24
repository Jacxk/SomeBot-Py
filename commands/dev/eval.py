from typing import List

from discord import Message, Client, Embed

from interfaces.Command import Command
from utils.utils import CommandError


class Eval(Command):
    def __init__(self, client: Client, config):
        super().__init__("eval", client, config)
        self.dev_only = True

    async def run(self, message: Message, args: List[str]):

        if len(args) < 1:
            raise CommandError("What do you want me to eval? I can't know what you're thinking...")

        embed = Embed(
            title="Here you go chief.",
            description=f"Input:\n```py\n"
                        f"{' '.join(args)}```\n\n"
                        f"Output:\n```\n"
                        f"{eval(' '.join(args))}```"
        )

        await message.channel.send(embed=embed)
