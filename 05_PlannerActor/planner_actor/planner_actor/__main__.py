import click
from .systems.nested import Runner


@click.command()
@click.argument("prompt", required=False)
def main(prompt=None):
    prompt = prompt or "What is SZA's age squared?"
    prompt += " Make a plan and then execute it."
    runner = Runner(prompt)
    answer = runner.run()
    print(answer)


if __name__ == "__main__":
    main()
