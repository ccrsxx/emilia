import os

from dotenv import dotenv_values
from typing import Final, cast


BOT_TOKEN: Final[str] = cast(
    str,
    os.getenv('BOT_TOKEN')
    or {
        **dotenv_values('.env.development'),
        **dotenv_values('.env.local'),
    }.get('BOT_TOKEN'),
)
