import discord
from aiohttp import ClientSession
from discord.ext import commands, tasks
from typing import Final
from models.trending import TrendingType, TrendingResponse


class Trending(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.top_trends: list[TrendingType] | None = None
        self.refresh_trending.start()

    @tasks.loop(hours=1)
    async def refresh_trending(self) -> None:
        new_top_trends: Final = await self.get_trending()
        if new_top_trends:
            self.top_trends = new_top_trends

    async def get_trending(self) -> list[TrendingType] | None:
        async with ClientSession() as session:
            resp = await session.get(
                'https://twitter-clone-ccrsxx.vercel.app/api/trends/place/1?limit=10'
            )

            data: TrendingResponse = await resp.json()

            if resp.ok:
                return data['trends']

            return None

    @commands.command()
    async def trending(self, ctx: commands.Context) -> None:
        if not self.top_trends:
            await ctx.send('❌ **No trending available**')
            return

        embed: Final = discord.Embed(
            title='📈 **Top 10 Trending on Twitter**',
            color=discord.Color.blue(),
            timestamp=ctx.message.created_at,
        )

        for i, trend in enumerate(self.top_trends, 1):
            name, tweet_volume = trend['name'], trend['tweet_volume']
            embed.add_field(
                name=f'{i}. {name}', value=f'{tweet_volume:,} tweets', inline=False
            )

        await ctx.send(embed=embed)

    @commands.command()
    async def force_refresh_trending(self, ctx: commands.Context) -> None:
        new_top_trends: Final = await self.get_trending()
        if new_top_trends:
            self.top_trends = new_top_trends
            await ctx.send('🔄 **Trending refreshed**')
        else:
            await ctx.send('❌ **Failed to refresh trending**')


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Trending(bot))
