import importlib
import json
import os
import re
import traceback
from pathlib import Path

from discord import ChannelType, Embed, AutoShardedClient, Game, Status, Message, Color

from utils.utils import *

config = None
commands = {}
client = AutoShardedClient(
    activity=Game(name="IM BEING MADE IN PYTHON"),
    status=Status.do_not_disturb
)
Logger.log("Starting up client...")


@client.event
async def on_connect():
    Logger.log(f"{Colors.FAIL}{client.user}{Colors.ENDC} connected to Discord!")


@client.event
async def on_ready():
    try:
        await load_database()
        await load_commands()
        Logger.log(f"Started up as {Colors.FAIL}{client.user}{Colors.ENDC}!")
    except Exception as err:
        Logger.error(str(err))
        Logger.error(traceback.format_exc())
        quit(1)


@client.event
async def on_error(event):
    Logger.error(f"There was an error on {Colors.WARNING}{event}{Colors.ENDC} with the API")
    quit(1)


@client.event
async def on_message(message: Message):
    if message.author.bot:
        return

    channel = message.channel

    if 406944549647286272 in list(map(lambda u: u.id, message.mentions)):
        await channel.send(f'What do you want {message.author.mention}?')
        return

    if not message.content.startswith(config['prefix']):
        return

    cmd, *args = message.content[len(config['prefix']):].split(" ")

    if cmd in commands:
        command = commands.get(cmd)
        Logger.log(f'{Colors.OKBLUE}{message.author}({message.author.id}){Colors.ENDC}'
                   f' executed: {Colors.OKGREEN}{message.content}'
                   f'{Colors.ENDC}, on guild {Colors.OKBLUE}{message.guild.name}({message.guild.id}){Colors.ENDC}')
        try:
            if command.delete_command:
                await message.delete()
            if command.enabled:
                if command.dev_only and message.author.id not in config['developers']:
                    embed = Embed(description="Executing comm... wait a minute... who are you...?")
                    embed.set_image(url="https://tenor.com/LiHD.gif")
                    await channel.send(embed=embed)
                    return
                if command.guild_only and channel.type == ChannelType.private or channel.type == ChannelType.group:
                    embed = Embed(description="Where... Where am I? What is this place?")
                    embed.set_image(url="https://tenor.com/XPbB.gif")
                    await channel.send(embed=embed)
                    return
                await command.run(message, args)
        except Exception as err:
            Logger.error(f"There was an error while executing '{command.name}': {err}")
            Logger.error(traceback.format_exc())
            if type(err) is CommandError:
                embed = Embed(
                    description=f"There was an error while executing this command:\n**{err}**",
                    color=Color.red(),
                    title="?&^ERROR BEOP BOEP.!$#"
                )
                await channel.send(embed=embed)
                return
            await channel.send("There was an internal error, report it to the developer")


async def load_commands():
    Logger.log("Loading commands...")
    path_list = Path('./commands/').glob('**/*.py')
    c = []
    for path in path_list:
        match = re.search('(.*/.*).py', str(path)).groups()[0].replace("/", ".")
        c.append(match)

    importlib.invalidate_caches()
    modules = list(map(importlib.import_module, c))
    for module in modules:
        module_name = module.__name__.split(".")[-1]
        module_class = getattr(module, module_name.capitalize())
        command = module_class(client, config)
        commands[command.name] = command
        Logger.log(f"Command {Colors.OKBLUE}'{command.name}'{Colors.ENDC} loaded!")
    commands.get('help').commands = commands
    Logger.log("Commands loaded.")


async def load_database():
    Logger.log("Loading databases...")
    with open("./config.json") as file:
        global config
        config = json.load(file)
        Logger.log("Config File loaded!")
    Logger.log("Databases loaded!")


if __name__ == '__main__':
    client.run(os.environ.get('TOKEN'))
