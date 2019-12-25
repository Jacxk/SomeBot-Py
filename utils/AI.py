import re


async def match(text: str, config, commands, message):
    for res in config['ai-res']:
        out = re.search(res[0], text, flags=re.IGNORECASE)

        if out:
            if res[1].startswith('run'):
                response = re.search('run (.*)', res[1])
                cmd = response.groups()[0]
                await commands[cmd].run(message, None)
                return True
            elif res[0].startswith('say'):
                await message.channel.send(re.sub('\{\d+\}', out.groups()[re.match('\{\d+\}', res[1]).start()], res[1]))
                return True
            else:
                await message.channel.send(res[1])
                return True

    return False
