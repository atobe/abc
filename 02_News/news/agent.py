# outer loop is get a bunch of articles
# run inner loop

# take a step of the inner loop

# get bullet points from article wrt stuff we already know
# nothing new, ok
# publish the points to the stream
# any significant new event? -> make that the title
# reverse chronological order in the stream

from typing import List
from devtools import pprint
from pathlib import Path
import datetime
from pydantic import BaseModel, Field

from .news import get_latest_news
from .siso import Renderer
from .model import *
from .knowledge import load, save, print_existing_knowledge
from .llm import call_llm

prompt_fp = Path(__file__).parent / "prompt.txt"
prompt = prompt_fp.read_text()


class Request(BaseModel):
    prompt: str = Field(
        ..., alias="prompt", description="The prompt to use for the completion"
    )
    existing_knowledge: Knowledge = Field(
        ..., description="The knowledge we have about the news story so far"
    )
    article: NewsArticle = Field(..., description="The news article to process")


def step(existing_knowledge: Knowledge, article: NewsArticle) -> NewPoints:
    global prompt
    # get bullet points from article wrt stuff we already know
    # nothing new, ok
    # publish the points to the stream
    # any significant new event? -> make that the title
    # reverse chronological order in the stream

    request = Request(
        prompt=prompt,
        existing_knowledge=existing_knowledge,
        article=article,
    )

    # Flatten the request structure to a conventional string prompt (structure in)
    prompt = Renderer().render(request)

    # Call the LLM with the structured output type (structure out)
    result = call_llm(prompt, NewPoints)

    return result


def get_new_news():
    # get the latest news
    articles = get_latest_news()
    seen_urls_fp = Path(__file__).parents[1] / "news/cache/seen_urls.txt"
    try:
        seen_urls = seen_urls_fp.read_text().splitlines()
    except FileNotFoundError:
        seen_urls = []
    for article in articles:
        if article.url not in seen_urls:
            print(f"New article: {article.url}")
            seen_urls.append(article.url)
            text = "\n".join(seen_urls)
            seen_urls_fp.write_text(text)
            return NewsArticle.from_news_item(article)


def render_new_points(new_points: NewPoints):
    s = ""
    for point in new_points.points:
        s += point.body + "\n\n"
    return s


def render_new_points_to_file(new_points: NewPoints):
    knowledge_fp = Path(__file__).parents[1] / "news/cache/knowledge.txt"
    # append new points
    with open(knowledge_fp, "a") as f:
        f.write("-" * 80 + "\n")
        f.write(render_new_points(new_points))


def main():
    # Are there new news articles that we haven't seen before?
    article = get_new_news()

    if not article:
        print("No new news")
        print_existing_knowledge()
        return

    # We are going to compare with existing knowledge
    existing_knowledge = load()

    # Extract new points if there are any
    new_points = step(existing_knowledge, article)

    print(f"Extracted {len(new_points.points)} new points")
    print()

    for point in new_points.points:
        print(point.body)
        print()

    now_s = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    # Embellish the new points with the article URL and the capture datetime
    new_points = NewPoints(
        points=[
            BulletPointEx(**point.model_dump(), url=article.url, capture_datetime=now_s)
            for point in new_points.points
        ]
    )

    render_new_points_to_file(new_points)

    # Update out local knowledge with new information we have extracted
    existing_knowledge.points.extend(new_points.points)
    save(existing_knowledge)

    print_existing_knowledge()

    if len(new_points.points) == 0:
        return

    email = (
        "I have extracted the following new points from the latest news article on the Chang'e 6 mission to the moon. Please review and let me know if you need any further information. \n\n"
        + render_new_points(new_points)
    )

    # send email


if __name__ == "__main__":
    main()
