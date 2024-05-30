# https://newsapi.ai/documentation/sandbox?tab=searchArticles
# pip install eventregistry

from devtools import pprint
from dataclasses import dataclass, field
from pathlib import Path
import datetime
import os

from . import NewsItem

YOUR_API_KEY = os.environ.get("EVENT_REGISTRY_API_KEY")

from eventregistry import EventRegistry, QueryArticlesIter


er = EventRegistry(apiKey=YOUR_API_KEY)

# {
#     'uri': '8120429225',
#     'lang': 'eng',
#     'isDuplicate': False,
#     'date': '2024-05-10',
#     'time': '07:58:17',
#     'dateTime': '2024-05-10T07:58:17Z',
#     'dateTimePub': '2024-05-10T07:57:58Z',
#     'dataType': 'news',
#     'sim': 0.6901960968971252,
#     'url': (
#         'https://www.sciencetimes.com/articles/50095/20240510/chinas-change-6-moon-mission-appears-include-undisclosed'
#         '-mini-rover.htm'
#     ),
#     'title': "China's Chang'e 6 Moon Mission Appears to Include an Undisclosed Mini Rover [See Photos]",
#     'body': (
#         "China Academy of Space Technology (CAST ) released new photos of Chang'e. 6. However, many noticed that there"
#         ' seemed to be a baby rover affixed to the side of the lander, which had yet to be mentioned prior to the sigh'
#         'ting.\n'
#         '\n'
#         "China's National Space Administration gave an update about its newest moon mission, which launched last week "
#         "on a Long March 5 rocket. The agency said that it successfully entered the Moon's orbit. The spacecraft is ex"
#         'pected to land early next month.\n'
#         '\n'
#
#
#   'source': {
#       'uri': 'chinadaily.com.cn',
#       'dataType': 'news',
#       'title': 'China Daily',
#   },
#   'authors': [],
#   'image': 'http://img2.chinadaily.com.cn/images/202405/10/663e06c7a31082fc2b6dc037.png',
#   'eventUri': 'eng-9548670',
#   'sentiment': 0.05098039215686279,
#   'wgt': 26,
#   'relevance': 26,
# }


def _get_latest_news():
    def extract_article(article: dict) -> NewsItem:
        return NewsItem(
            uri=article["uri"],
            url=article["url"],
            title=article["title"],
            body=article["body"],
            dateTime=article["dateTime"],
        )

    # dateStart and dateEnd are inclusive 2024-05-06 for instance
    # start is 7 days ago
    dateEnd = datetime.datetime.now()  # .strftime("%Y-%m-%d")
    dateStart = dateEnd - datetime.timedelta(days=7)
    dateEnd = dateEnd.strftime("%Y-%m-%d")
    dateStart = dateStart.strftime("%Y-%m-%d")

    query = {
        "$query": {
            "$and": [
                {"conceptUri": "http://en.wikipedia.org/wiki/Chang'e_6"},
                {"dateStart": dateStart, "dateEnd": dateEnd, "lang": "eng"},
            ]
        }
    }
    q = QueryArticlesIter.initWithComplexQuery(query)
    return [extract_article(article) for article in q.execQuery(er, maxItems=10)]


def check_cache():
    cache_fp = Path(__file__).parents[3] / "cache" / "responses"
    cache_fps = list(cache_fp.glob("*.pickle"))

    if len(cache_fps) == 0:
        return None

    # extract the time from the filename
    cache_fps.sort(key=lambda x: x.name)

    # extract the time )(HHMMSS) from the latest file
    # format is YYYYMMDD-HHMMSS.pickle
    latest = cache_fps[-1]
    filename = latest.name
    time = filename.split(".")[0]
    # convert to datetime
    time = datetime.datetime.strptime(time, "%Y%m%d-%H%M%S")
    print(time)
    # get the current time
    now = datetime.datetime.now()
    # get the difference
    diff = now - time
    print(diff)
    # if the difference is less than 5 minutes
    if diff.total_seconds() < 300:
        print("recent, using cache")
        return rp(latest)

    return None


def get_latest_news():
    # YYYYMMDD-HHMMSS.pickle
    cache_fp = (
        Path(__file__).parents[3]
        / "cache"
        / "responses"
        / f'{datetime.datetime.now().strftime("%Y%m%d-%H%M%S")}.pickle'
    )
    cache_fp.parent.mkdir(parents=True, exist_ok=True)
    print(cache_fp)
    articles = check_cache()
    if not articles:
        articles = _get_latest_news()
        wp(articles, cache_fp)
    return articles[:10]


def main():
    articles = get_latest_news()
    for article in articles:
        print(article.dateTime, article.title)
        print(article.body)
        print()
    print(f"Found {len(articles)} articles")


if __name__ == "__main__":
    main()
