import discord
import datetime

from discord.ext import commands


class Tools(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def echo(self, ctx, *, message) -> None:
        await ctx.message.delete()
        await ctx.send(message)

    @commands.command()
    async def ping(self, ctx) -> None:
        await ctx.send(f'🏓 {round(self.bot.latency * 1000)} ms.')

    @commands.command()
    async def get_info(self, ctx) -> None:
        embed = discord.Embed(
            title='Info',
            description='An info message using an embed!',
            colour=discord.Colour.blurple(),  # 0x7289da
            timestamp=datetime.datetime.utcnow(),
        )

        embed.set_footer(text=f'this bot is running on {len(self.bot.guilds)}')
        embed.add_field(name='Version', value='0.1', inline=True)
        embed.add_field(name='Language', value='Python 3.8', inline=True)
        embed.set_author(
            name='nect',
            url='https://gist.github.com/bynect',
            icon_url='http://tiny.cc/nect-user-pic',
        )

        await ctx.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Tools(bot))
