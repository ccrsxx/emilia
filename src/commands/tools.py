import ctypes
import datetime
from typing import Final

import discord
from discord.ext import commands


class Tools(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.start_time = datetime.datetime.utcnow()

    @commands.command()
    async def uptime(self, ctx: commands.Context) -> None:
        await ctx.message.add_reaction('🤡')

        now: Final = datetime.datetime.utcnow()
        delta: Final = now - self.start_time
        seconds = int(delta.total_seconds())

        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        message = '⏳ Uptime: '

        if days:
            message += f'{days} day(s), '

        message += f'{hours} hour(s), {minutes} minute(s), {seconds} second(s)'

        await ctx.send(message)

    @commands.command()
    async def system_uptime(self, ctx: commands.Context) -> None:
        # getting the library in which GetTickCount64() resides
        lib = ctypes.windll.kernel32
        
        # calling the function and storing the return value
        t = lib.GetTickCount64()
        
        # since the time is in milliseconds i.e. 1000 * seconds
        # therefore truncating the value
        t = int(str(t)[:-3])
        
        # extracting hours, minutes, seconds & days from t
        # variable (which stores total time in seconds)
        mins, sec = divmod(t, 60)
        hour, mins = divmod(mins, 60)
        days, hour = divmod(hour, 24)
        
        # formatting the time in readable form
        # (format = x days, HH:MM:SS)
        message = f"{days} days, {hour:02}:{mins:02}:{sec:02}"

        await ctx.send(message)

    @commands.command()
    async def echo(self, ctx: commands.Context, *, arg) -> None:
        await ctx.message.delete()
        await ctx.send(arg)

    @commands.command()
    async def ping(self, ctx: commands.Context) -> None:
        await ctx.send(f'🏓 {round(self.bot.latency * 1000)} ms.')

    @commands.command()
    async def get_info(self, ctx: commands.Context) -> None:
        embed = discord.Embed(
            title='Info',
            description='An info message using an embed!',
            colour=discord.Colour.blurple(),
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
