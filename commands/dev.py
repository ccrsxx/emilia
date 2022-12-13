import re

from io import StringIO
from discord import app_commands, Interaction
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

    @commands.command()
    @commands.is_owner()
    async def sync(self, ctx: commands.Context) -> None:
        self.bot.tree.clear_commands(guild=ctx.guild)
        cmds = await self.bot.tree.sync()
        await ctx.send(f'✅ Successfully synced {len(cmds)} commands')

    @app_commands.command(name='add', description='Adds two numbers together')
    @app_commands.describe(
        first_value='The first value you want to add something to',
        second_value='The value you want to add to the first value',
    )
    async def add(
        self, interaction: Interaction, first_value: int, second_value: int
    ) -> None:
        """Adds two numbers together."""
        await interaction.response.send_message(
            f'{first_value} + {second_value} = {first_value + second_value}'
        )

    @app_commands.command(name='color', description='color selector')
    @app_commands.describe(colors='Colors to choose from')
    @app_commands.choices(
        colors=[
            app_commands.Choice(name='Red', value=1),
            app_commands.Choice(name='Blue', value=2),
            app_commands.Choice(name='Green', value=3),
        ]
    )
    async def color(self, interaction: Interaction, colors: app_commands.Choice[int]):
        await interaction.response.send_message(
            f'You chose {colors.name} with the value {colors.value}'
        )

    @app_commands.command(name='ping', description='Pings the bot')
    async def ping(self, interaction: Interaction) -> None:
        await interaction.response.send_message('Pong!')


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Dev(bot))
