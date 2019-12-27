import re
from random import randint
from typing import List

valid = False


async def match(text: str, config, commands, message):
    global valid
    valid = False
    for res in config['ai-res']:
        out = re.search(res[0], text, flags=re.IGNORECASE)
        func = lambda first, second: execute(first, second, message, commands, out)

        if out:
            directions: List[str] = res[1].split(" | ")

            if directions[0] == "$each$":
                directions.pop(0)
                for i in range(len(directions)):
                    await func(res[0], directions[i])
            elif directions[0] == "$random$":
                directions.pop(0)
                await func(res[0], directions[randint(0, len(directions) - 1)])

    return valid


async def execute(first: str, second: str, message, commands, out):
    global valid
    if second.startswith('run'):
        response = re.search('run (.*)', second)
        cmd = response.groups()[0]
        await commands[cmd].run(message, None)
        valid = True
    elif first.startswith('say'):
        await message.channel.send(
            re.sub('\{\d+\}', out.groups()[re.match('\{\d+\}', second).start()], second)
        )
        valid = True
    else:
        await message.channel.send(second)
        valid = True
