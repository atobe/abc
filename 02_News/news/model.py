from pydantic import BaseModel, Field
from typing import List


class NewsArticle(BaseModel):
    title: str = Field(..., description="The title of the news article")
    body: str = Field(..., description="The body of the news article")
    dateTime: str = Field(
        ..., description="The date and time the article was published"
    )
    url: str = Field(..., description="The url of the news article")

    @classmethod
    def from_news_item(cls, item):
        return cls(
            title=item.title, body=item.body, dateTime=item.dateTime, url=item.url
        )


class BulletPoint(BaseModel):
    """A point extracted from a news article about an ongoing news story"""

    body: str = Field(..., description="The extracted point in your own words")
    datetime: str = Field(
        ..., description="When the event happened, if known otherise 'unknown'"
    )
    matching_segment: str = Field(
        ..., description="a short text segment which is likely to match the source text"
    )
    # this is optional


class BulletPointEx(BulletPoint):
    """A point extracted from a news article about an ongoing news story"""

    url: str = Field(..., description="The url of the news article")
    capture_datetime: str = Field(..., description="When the event was captured")


class Knowledge(BaseModel):
    """The knowledge we have about a news story so far"""

    points: List[BulletPoint] = Field(
        ..., description="Existing point we have collected about a story"
    )


class NewPoints(BaseModel):
    """New points we have discovered about a news story"""

    points: List[BulletPoint] = Field(
        ..., description="New point we have collected about this news story"
    )


