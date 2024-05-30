from news.fake_news_api import FakeNewsAPI
from news import NewsItem
from devtools import pprint

fn_api = FakeNewsAPI()

seen_before = set()

key_attr = 'title'

count = 0
for response in fn_api:
    # each response a list of NewsItems
    for news_item in response:
        if getattr(news_item, key_attr) in seen_before:
            continue
        seen_before.add(getattr(news_item, key_attr))
        print(news_item.body[:100].replace("\n", "\\n"))
        
