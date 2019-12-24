from typing import List

from discord import Client, Message

from utils.utils import Colors


class Command:
    def __init__(self, name: str, client: Client, config):
        self.name = name
        self.client = client
        self.delete_command = False
        self.usage = name
        self.guild_only = True
        self.enabled = True
        self.owner_only = False
        self.dev_only = False
        self.allowed_developers = config["developers"]

    async def run(self, message: Message, args: List[str]):
        raise Exception(f"The command named {Colors.WARNING}'{self.name}'{Colors.ENDC} has no run method.")
