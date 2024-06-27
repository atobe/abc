import tkinter as tk
import pygraphviz as pgv
import click
import pickle
from prettyprinter import pprint
from raal.agentlib import show_chunks_compact

def show_lats_tree(node, depth=0):
    indent = "   " * depth
    print(f"{indent}{str(node)[:100]}")
    for child in node.children:
        show_lats_tree(child, depth + 1)

def show_lats_plus_agent_tree(node, depth=0):
    indent = "   " * depth
    print(f"{indent}{str(node)[:100]} {str(node.state)[:100]}")
    show_chunks_compact(node.state)
    for child in node.children:
        show_lats_plus_agent_tree(child, depth + 1)


def load(filepath):
    with open(filepath, "rb") as f:
        lats_tree = pickle.load(f)
        return lats_tree


# def viz(filepath):
#     # pprint(lats_tree)
#     show_lats_tree(lats_tree)


@click.group()
def main():
    pass


@main.command()
@click.argument("filename")
def lats(filename):
    lats_tree = load(filename)
    show_lats_tree(lats_tree)


@main.command()
@click.argument("filename")
def agent(filename):
    lats_tree = load(filename)
    show_lats_plus_agent_tree(lats_tree)


if __name__ == "__main__":
    main()
