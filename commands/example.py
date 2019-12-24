from typing import List

from discord import Client, Message

from interfaces.Command import Command


class Example(Command):
    def __init__(self, client: Client, config):
        super().__init__("example", client, config)
        self.enabled = False

    async def run(self, message: Message, args: List[str]):
        return
