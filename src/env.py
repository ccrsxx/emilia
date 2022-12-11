from dotenv import dotenv_values
from typing import cast


BOT_TOKEN = cast(
    str,
    {
        **dotenv_values('../.env.development'),
        **dotenv_values('../.env.local'),
    }.get('BOT_TOKEN'),
)


if not BOT_TOKEN or BOT_TOKEN == 'YOUR_BOT_TOKEN':
    raise ValueError('BOT_TOKEN is not set')
