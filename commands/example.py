import discord

from interfaces.Command import Command


class Example(Command):
    def __init__(self, client: discord.Client, config):
        super().__init__("example", client, config)
        self.enabled = False

    async def run(self, message: discord.Message, args: []):
        return

