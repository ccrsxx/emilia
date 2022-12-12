from typing import TypedDict


class TrendingType(TypedDict):
    url: str
    name: str
    query: str
    tweet_volume: int
    promoted_content: str


class TrendingResponse(TypedDict):
    trends: list[TrendingType]
    location: str
