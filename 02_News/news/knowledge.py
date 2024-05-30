from pathlib import Path

from .model import BulletPoint, Knowledge
from .utils import rp, wp

knowledge_fp = Path(__file__).parents[1] / "news/cache/knowledge.pickle"


def _load() -> Knowledge:
    # load the knowledge from the stream
    try:
        return rp(knowledge_fp)
    except FileNotFoundError:
        return Knowledge(points=[])


def load() -> Knowledge:
    k = _load()
    # turn any BulletPointEx into BulletPoint
    return Knowledge(points=[BulletPoint(**point.model_dump()) for point in k.points])


def save(knowledge: Knowledge):
    # save the knowledge to the stream
    wp(knowledge, knowledge_fp)


def print_existing_knowledge(existing_knowledge=None):
    existing_knowledge = existing_knowledge or load()
    print("=== existing knowledge ===")
    for point in existing_knowledge.points:
        print(point.body)
        print()
    print(f"{len(existing_knowledge.points)} points in total")
