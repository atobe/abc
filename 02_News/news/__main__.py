import click
from pathlib import Path
from news.news import NewsItem

@click.group()
def cli():
    pass

@cli.command()
def update():
    from .agent import main
    main()

@cli.command()
def reset():
    from .news.fake_news_api import reset
    
    reset()

    files_to_delete_from_cache = [
        'knowledge.txt',
        'knowledge.pickle',
        'seen_urls.txt',
    ]
    
    cache_fp = Path(__file__).parents[1] / "news/cache"
    
    for file in files_to_delete_from_cache:
        (cache_fp / file).unlink()
    
def main():
    # this hideousness is just because I pickled a bunch of data from another module
    # construct fake module t2.chang_e.infra.news.NewsItem
    import sys
    from types import ModuleType
    
    # t2 is a package
    sys.modules['t2'] = ModuleType('t2')
    
    # chang_e is a module
    sys.modules['t2.chang_e'] = ModuleType('t2.chang_e')

    # news is a module
    sys.modules['t2.chang_e.infra'] = ModuleType('t2.chang_e.infra')
    
    # news is a module
    mod = sys.modules['t2.chang_e.infra.news'] = ModuleType('t2.chang_e.infra.news')
    
    # NewsItem is a class
    mod.NewsItem = NewsItem
    
    
    cli()

if __name__ == "__main__":
    main()
