import click


@click.group()
def main():
    pass


@main.command()
@click.argument("app_name")
@click.argument("case", required=False, default=None)
def run(app_name, case):
    from .lats import run

    run(app_name, case)

@main.command()
@click.argument("name", required=False, default=None)
def print_cache(name):
    from .utils import print_cache

    print_cache(name)

@main.command()
@click.argument("case_number")
def case(case_number):
    from .apps.humaneval.lib import _get_case

    case = _get_case(case_number)
    from devtools import pprint
    pprint(case)

if __name__ == "__main__":
    main()
