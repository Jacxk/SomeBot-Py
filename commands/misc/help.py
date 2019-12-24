from typing import List

from discord import Message, Client

from interfaces.Command import Command


class Help(Command):
    def __init__(self, client: Client, config):
        super().__init__("help", client, config)
        self.commands = None

    async def run(self, message: Message, args: List[str]):
        if self.commands is None:
            raise Exception("commands list is empty")

        cmd_list = filter(lambda c: c.enabled, self.commands.values())
        cmd_list = list(map(lambda c: c.name, cmd_list))
        await message.channel.send("\n".join(cmd_list))
