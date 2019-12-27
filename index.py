import atexit
import importlib
import json
import os
import re
import traceback
from pathlib import Path
from random import randint

from discord import ChannelType, Embed, AutoShardedClient, Game, Status, Message, Color

from utils import AI
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
async def on_disconnect():
    Logger.warning(f"{Colors.FAIL}{client.user}{Colors.ENDC} disconnected from Discord!")


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


@atexit.register
def stop():
    Logger.warning("Shutting down bot...")


@client.event
async def on_message(message: Message):
    if message.author.bot:
        return

    channel = message.channel
    cmd, *args = message.content[len(config['prefix']):].split(" ")

    if client.user.id in list(map(lambda u: u.id, message.mentions)):
        res = await AI.match(message.content, config, commands, message)
        if not res:
            if args and len(args) > 0:
                await channel.send(config['ai-res-not'][randint(0, len(config['ai-res-not']) - 1)])
            else:
                await channel.send(
                    config['ping-res'][randint(0, len(config['ping-res']) - 1)].replace(
                        '{user}', message.author.mention
                    )
                )
        return

    if not message.content.startswith(config['prefix']):
        return

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
                    await channel.send("Executing comm... wait a minute... who are you...?\nhttps://tenor.com/LiHD.gif")
                    return
                if command.guild_only and channel.type == ChannelType.private or channel.type == ChannelType.group:
                    await channel.send("Where... Where am I? What is this place?\nhttps://tenor.com/XPbB.gif")
                    return
                await command.run(message, args)
        except Exception as err:
            Logger.error(f"There was an error while executing '{command.name}': {err}")
            Logger.error(traceback.format_exc())
            if type(err) is CommandError:
                embed = Embed(
                    description=f"**{err}**",
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
