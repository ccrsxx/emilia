import re

from io import StringIO
from discord.ext import commands
from contextlib import redirect_stdout
from typing import Final


class Dev(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def exec(self, ctx: commands.Context, *, arg: str) -> None:
        f = StringIO()

        if arg.startswith('```') and arg.endswith('```'):
            arg = re.sub(r'```(\w+)?', '', arg)

        with redirect_stdout(f):
            try:
                exec(arg)
            except Exception as e:
                await ctx.send(f'❌  **{type(e).__name__} - {e}**: `{arg}`')
                return

        command_output_value: Final[str] = f.getvalue()

        await ctx.send(
            command_output_value
            if command_output_value
            else f'✅ Command executed successfully'
        )

    @commands.command()
    @commands.is_owner()
    async def test(self, ctx: commands.Context) -> None:
        await ctx.send('test')


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Dev(bot))
