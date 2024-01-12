import os
from typing import Final, cast

from dotenv import dotenv_values

BOT_TOKEN: Final = cast(
    str,
    os.getenv('BOT_TOKEN')
    or {
        **dotenv_values('.env.development'),
        **dotenv_values('.env.local'),
    }.get('BOT_TOKEN'),
)
