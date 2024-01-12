import asyncio
import os
from typing import Final, Literal, cast

import discord
from cogwatch import Watcher
from discord import Intents
from discord.ext import commands, tasks

from constants.status_list import RE_ZERO_CHARS
from constants.token import BOT_TOKEN

Prefixes = tuple[Literal['!'], Literal['$'], Literal['>']]


def get_prefix(
    bot: commands.Bot, message: discord.Message
) -> (Prefixes | Literal['?']):
    prefixes: Final[Prefixes] = ('!', '$', '>')

    if not message.guild:
        return '?'

    return cast(Prefixes, commands.when_mentioned_or(*prefixes)(bot, message))


intents: Final = Intents.default().all()

bot: Final = commands.Bot(
    command_prefix=get_prefix,
    description='Personal bot by ccrsxx',
    intents=intents,
)


@bot.event
async def on_ready() -> None:
    print(f'{bot.user} is online and ready!')

    change_status.start()

    watcher: Final = Watcher(bot, path='commands')

    await watcher.start()


@tasks.loop(minutes=5)
async def change_status() -> None:
    await bot.change_presence(activity=discord.Game(f'with {next(RE_ZERO_CHARS)}'))


async def load_commands() -> None:
    os.chdir('src')

    commands: Final = [
        f'commands.{command[:-3]}'
        for command in os.listdir('commands')
        if command.endswith('.py')
    ]

    for command in commands:
        await bot.load_extension(command)


async def main() -> None:
    if not BOT_TOKEN or BOT_TOKEN == 'YOUR_BOT_TOKEN':
        raise ValueError('BOT_TOKEN is not set')

    async with bot:
        await load_commands()
        await bot.start(BOT_TOKEN)


if __name__ == '__main__':
    asyncio.run(main())
