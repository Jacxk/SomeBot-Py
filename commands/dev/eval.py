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

        text = ' '.join(args).split('\n')
        text[-1] = 'return ' + text[-1]
        text = '\n  '.join(text)

        fun = {
            'message': message,
            'Embed': Embed
        }
        _in = f"async def func():\n  {text}"

        try:
            exec(_in, fun)
            out = await fun['func']()
        except Exception as err:
            out = str(err)

        embed = Embed(
            title="Here you go chief.",
            description="Input:\n```py\n"
                        f"{_in}```\n\n"
                        "Output:\n```\n"
                        f"{out}```"
        )

        await message.channel.send(embed=embed)
