import re
from typing import List

import maya
from discord import Client, Message, Embed, Color

from interfaces.Command import Command
from utils.utils import CommandError


class Giveaway(Command):
    def __init__(self, client: Client, config):
        super().__init__("giveaway", client, config)

    async def run(self, message: Message, args: List[str]):
        args = re.split(
            "(((title):\s*'(.*?)')\s*)|"
            "(((time):\s*'(.*?)')\s*)|"
            "(((desc):\s*'(.*?)')\s*)|"
            "((winners):\s*(\d+))"
            , message.content
        )

        if 'title' not in args:
            raise CommandError("You need to provide more arguments, "
                               "`title` missing or it's malformatted...\n"
                               "Format: `title: 'remember the quotes'`")

        if 'time' not in args:
            raise CommandError("You need to provide more arguments, "
                               "`time` missing or it's malformatted...\n"
                               "Format: `time: 'remember the quotes'`")

        title = args[args.index('title') + 1]
        time = args[args.index('time') + 1]
        winners = 1 if 'winners' not in args else args[args.index('winners') + 1]
        desc = None if 'desc' not in args else args[args.index('desc') + 1]

        ptime = maya.when(time, prefer_dates_from='future')

        embed = Embed(title=title.capitalize(), timestamp=ptime.datetime(), color=Color.blurple())
        embed.description = f"{desc if desc else ''}\n" \
                            f"Winners: {winners}\n" \
                            f"Ends {ptime.slang_time()}\n\n" \
                            f"*React with 🎊 to enter*"

        msg = await message.channel.send(embed=embed)
        await msg.add_reaction('🎊')
