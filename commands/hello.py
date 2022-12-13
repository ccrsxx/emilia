from discord import app_commands
from discord.ext import commands


class Hello(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command()
    async def hello(self, ctx: commands.Context) -> None:
        await ctx.send('This is a hybrid command')

    @commands.hybrid_command()
    async def greet(self, ctx: commands.Context) -> None:
        await ctx.send(f'Hello {ctx.message.author.mention}!')


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Hello(bot))
