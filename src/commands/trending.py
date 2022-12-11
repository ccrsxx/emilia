from aiohttp import ClientSession
from discord.ext import commands, tasks
from typing import Final, TypedDict


class TrendingType(TypedDict):
    url: str
    name: str
    query: str
    tweet_volume: int
    promoted_content: str


class TrendingResponse(TypedDict):
    trends: list[TrendingType]
    location: str


class Trending(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.top_trends: list[TrendingType] = []
        self.refresh_trending.start()

    @tasks.loop(hours=1)
    async def refresh_trending(self) -> None:
        new_top_trends: Final[list[TrendingType] | None] = await self.get_trending()
        if new_top_trends:
            self.top_trends = new_top_trends

    async def get_trending(self) -> list[TrendingType] | None:
        async with ClientSession() as session:
            resp = await session.get(
                'https://twitter-clone-ccrsxx.vercel.app/api/trends/place/1?limit=10'
            )

            data: TrendingResponse = await resp.json()

            if resp.ok:
                top_trending = self.parse_trending(data)
                return top_trending

            return None

    @commands.command()
    async def trending(self, ctx: commands.Context) -> None:
        trending_list = '📈 **Top 10 Trending on Twitter**:\n'

        trending_list += '\n'.join(
            f'{i}.\t **{trend["name"]}** - {trend["tweet_volume"]}'
            for i, trend in enumerate(self.top_trends, 1)
        )

        await ctx.send(trending_list)

    def parse_trending(self, data: TrendingResponse) -> list[TrendingType]:
        trends = data['trends'][:10]

        for trend in trends:
            for key, value in trend.copy().items():
                if key == 'promoted_content':
                    trend.pop(key)
                elif key == 'tweet_volume':
                    trend[key] = f'{value:,} tweets'

        return trends


async def setup(bot) -> None:
    await bot.add_cog(Trending(bot))
