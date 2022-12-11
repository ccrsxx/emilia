from discord import Intents, Message
from discord.ext import commands
from discord.ext.commands import Context
from env import BOT_TOKEN


intents = Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.command()
@commands.is_owner()
async def test_admin(ctx: Context, arg: str):
    await ctx.send(arg)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.listen('on_message')
async def on_message(message: Message):
    pass


bot.run(BOT_TOKEN)
