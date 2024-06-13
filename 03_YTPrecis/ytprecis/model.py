from pydantic import BaseModel, Field
from typing import List, Optional
from devtools import pprint

class YTSearchResult(BaseModel):
    title: str
    description: str
    videoid: str
    url: str


class YTTranscriptSegment(BaseModel):
    start_seconds: float
    duration_seconds: float
    text: str


class YTTranscript(BaseModel):
    video_id: str
    segments: List[YTTranscriptSegment]

    def __siso__(self) -> str:
        return "\n".join(
            [
                f"{segment.start_seconds:.2f} - {segment.duration_seconds:.2f}: {segment.text}"
                for segment in self.segments
            ]
        )


class BulletPoint(BaseModel):
    text: str
    start: float
    duration: float

class BulletPointEx(BulletPoint):
    video_id: Optional[str]

class BulletPoints(BaseModel):
    points: List[BulletPoint]

class BulletPointsEx(BaseModel):
    points: List[BulletPointEx]

class ExtractPointsRequest(BaseModel):
    prompt: str
    transcript: YTTranscript
    
    
class OrganizeBulletPointsRequest(BaseModel):
    prompt: str
    bullet_points: BulletPointsEx
    
class OrganizedBulletPoints(BaseModel):
    introductory_points: List[BulletPointEx]
    themes: List[str] = Field(..., description="List of up to 3 major themes")
    theme1_points: Optional[BulletPointsEx]
    theme2_points: Optional[BulletPointsEx]
    theme3_points: Optional[BulletPointsEx]
    closing_points: List[BulletPointEx]

class VideoEdit(BaseModel):
    points: List[BulletPointEx]

class VideoEditRequest(BaseModel):
    prompt: str
    organized_points: OrganizedBulletPoints

def main():
    from instructor.dsl.partial import Partial

    PartialBulletPoints = Partial[BulletPoints]

    pbps = PartialBulletPoints(points=[])
    
    data = pbps.model_dump()
    
    # reconstruct BulletPoints object
    bps = BulletPoints(**data)
    pprint(bps)
    
    
if __name__ == "__main__":
    main()
    