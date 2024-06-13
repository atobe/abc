import click


@click.group()
def main():
    pass


@main.command()
@click.argument("query_parts", nargs=-1)
def precis(query_parts):
    from .main import main as precis_main

    precis_main(query_parts)


# cache is a group of commands
@main.group()
def cache():
    pass


@cache.command()
@click.argument("key")
def delete(key):
    from .cache import cache

    del cache[key]


@cache.command()
def list():
    from .cache import cache

    for key in cache.keys():
        print(key)


@main.group()
def utils():
    pass


@utils.command()
@click.argument("parts", nargs=-1)
def hashtest(parts):
    from .utils import phrase, hashstring
    print(hashstring(phrase(parts)))

if __name__ == "__main__":
    main()