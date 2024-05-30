from dataclasses import dataclass


@dataclass
class NewsItem:
    uri: str
    url: str
    title: str
    body: str
    dateTime: str


def get_latest_news(source="fake"):
    if source == "fake":
        from .fake_news_api import get_latest_news
    else:
        from .real_news_api import get_latest_news
    return get_latest_news()

