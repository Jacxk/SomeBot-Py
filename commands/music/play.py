from typing import List

import discord

from interfaces.Command import Command
from utils.utils import CommandError


class Play(Command):
    def __init__(self, client: discord.Client, config):
        super().__init__("play", client, config)

    async def run(self, message: discord.Message, args: List[str]):
        voice = message.author.voice

        if not voice:
            raise CommandError("You're not in a voice channel")

        voice_channel = voice.channel
        await voice_channel.connect()

        await message.channel.send("Connected!")
