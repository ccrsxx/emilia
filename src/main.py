import discord

from discord import Intents
from discord.ext import commands, tasks
from cogwatch import Watcher
from itertools import cycle
from utils.env import BOT_TOKEN
from typing import Final, Literal


def get_prefix(
    _: commands.Bot, message
) -> (tuple[Literal['!'], Literal['?'], Literal['>']] | Literal['!']):
    """This function returns a Prefix for our bot's commands.

    Args:
            bot (commands.Bot): The bot that is invoking this function.
            message (discord.Message): The message that is invoking.

    Returns:
            string or iterable containing strings: A string containing prefix or an iterable containing prefixes
    Notes:
            Through a database (or even a json) this function can be modified to returns per server prefixes.
            This function should returns only strings or iterable containing strings.
            This function shouldn't returns numeric values (int, float, complex).
            Empty strings as the prefix always matches, and should be avoided, at least in guilds.
    """

    if not isinstance(message.guild, discord.Guild):
        """Checks if the bot isn't inside of a guild.
        Returns a prefix string if true, otherwise passes.
        """
        return '!'

    return '!', '?', '>'


intents: Final[Intents] = Intents.default().all()

bot: Final[commands.Bot] = commands.Bot(
    command_prefix=get_prefix,
    description='Personal bot by ccrsxx',
    intents=intents,
)


@bot.event
async def on_ready() -> None:
    print(f'{bot.user} is online and ready!')
    change_status.start()

    watcher: Final[Watcher] = Watcher(bot, path='commands', preload=True)
    await watcher.start()


status_list = cycle(
    [
        'with Ami',
        'with Rem',
    ]
)


@tasks.loop(minutes=5)
async def change_status() -> None:
    await bot.change_presence(activity=discord.Game(next(status_list)))


bot.run(BOT_TOKEN)
