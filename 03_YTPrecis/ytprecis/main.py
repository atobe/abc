import requests
import os
import sys
import math
from pathlib import Path
from devtools import pprint
from textwrap import dedent
from youtube_transcript_api import YouTubeTranscriptApi
from typing import List

from .cache import cache, cached_or_not
from .model import *
from .siso import Renderer
from .llm import call_llm
from .utils import phrase, hashstring

YT_API_KEY = os.environ.get("YT_API_KEY", None)
if YT_API_KEY is None:
    print("YT_API_KEY environment variable is not set")
    sys.exit(1)


def search(query) -> List[YTSearchResult]:
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "maxResults": 10,
        "type": "video",
        "key": YT_API_KEY,
    }
    response = requests.get(url, params=params)
    results = response.json()

    return [
        YTSearchResult(
            title=item["snippet"]["title"],
            description=item["snippet"]["description"],
            videoid=item["id"]["videoId"],
            url=f"https://www.youtube.com/watch?v={item['id']['videoId']}",
        )
        for item in results["items"]
    ]


def get_transcript_with_timestamps(video_id) -> YTTranscript:
    try:
        # Fetch the transcript for the given video ID
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        # Process and display the transcript with timestamps
        transcript_with_timestamps = YTTranscript(video_id=video_id, segments=[])
        for entry in transcript:
            start = float(entry["start"])
            duration = float(entry["duration"])
            text = entry["text"]
            transcript_with_timestamps.segments.append(
                YTTranscriptSegment(
                    start_seconds=start, duration_seconds=duration, text=text
                )
            )

        return transcript_with_timestamps
    except Exception as e:
        return str(e)


def resegmenter(transcript: YTTranscript, max_duration: float = 5.0) -> YTTranscript:
    # segment on a period at the end of the sentence (if text is > 5 chars)
    # or max_duration is exceeded
    new_segments = []
    text_accumulator = ""
    for segment in transcript.segments:
        text_accumulator += " " + segment.text
        if len(text_accumulator) > 5 and text_accumulator[-1] == ".":
            new_segments.append(
                YTTranscriptSegment(
                    start_seconds=segment.start_seconds,
                    duration_seconds=segment.duration_seconds,
                    text=text_accumulator.strip(),
                )
            )
            text_accumulator = ""
        elif segment.duration_seconds > max_duration:
            new_segments.append(
                YTTranscriptSegment(
                    start_seconds=segment.start_seconds,
                    duration_seconds=segment.duration_seconds,
                    text=text_accumulator.strip(),
                )
            )
            text_accumulator = ""
    if text_accumulator:
        new_segments.append(
            YTTranscriptSegment(
                start_seconds=segment.start_seconds,
                duration_seconds=segment.duration_seconds,
                text=text_accumulator,
            )
        )

    return YTTranscript(video_id=transcript.video_id, segments=new_segments)


def get_transcripts(search_results: List[YTSearchResult]) -> List[YTTranscript]:
    transcripts = []
    for result in search_results:
        video_id = result.videoid
        transcript = cached_or_not(video_id, get_transcript_with_timestamps, video_id)
        if not isinstance(transcript, YTTranscript):
            cache[video_id] = None
            continue
        resegmented_transcript = resegmenter(transcript)
        transcripts.append(resegmented_transcript)
        cache[video_id] = resegmented_transcript
    return transcripts


def show_transcripts_snippets(transcripts: List[YTTranscript]):
    for resegmented_transcript in transcripts:
        # print(f'title: {result.title}')
        # print(f'url: {result.url}')
        print(f"video_id: {resegmented_transcript.video_id}")
        # len of the segments
        print(f"number of segments: {len(resegmented_transcript.segments)}")
        # first 3 segments
        for segment in resegmented_transcript.segments[:3]:
            print(
                f"{segment.start_seconds:.2f} - {segment.duration_seconds:.2f}: {segment.text}"
            )
        print()


def extract_points(transcript: YTTranscript) -> BulletPoints:
    # extract bullet points from the transcript
    prompt = """
    Extract bullet points from the following transcript. 
    We are producing a video summary. We are looking for high quality points that capture the essence of the content.
    
    Example: subject "latest from nvidia"
    
    Good Examples:
    - nvidia has launched it's latest GPU; blackwell
    - the new GPU is has tensor cores that accelerate the training of AI models
    - the new GPU is 30% more efficient while being 20% faster
    
    Bad Examples:
    - nvidia had a launch party today
    - Jensen has a cold
    - the new GPU is green
    """
    request = ExtractPointsRequest(prompt=dedent(prompt), transcript=transcript)
    text = Renderer().render(request)
    response = call_llm(text, BulletPoints)
    return response


def exify(bullet_points: BulletPoints, video_id: str) -> BulletPointsEx:
    return BulletPointsEx(
        points=[
            BulletPointEx(video_id=video_id, **bp.model_dump())
            for bp in bullet_points.points
        ]
    )


def organize_points(all_points: BulletPointsEx) -> OrganizedBulletPoints:
    prompt = """
    Organize the following bullet points into an outline for a video summary.
    We are producing a video summary. 
    First we will introduce the topic, then we will present the main themes, and finally we will close with a summary.
    We can have up to 3 main themes.
    Pick at most 2 points for each section.
    """
    request = OrganizeBulletPointsRequest(
        prompt=dedent(prompt), bullet_points=all_points
    )
    text = Renderer().render(request)
    response = call_llm(text, OrganizedBulletPoints)
    return response


def create_the_edit(organized_points: OrganizedBulletPoints) -> VideoEdit:
    # create a linear video edit from the organized points
    prompt = """
    Create a linear video edit from the following organized bullet points.
    Aim for a 3-5 minute video summary.
    """
    request = VideoEditRequest(prompt=dedent(prompt), organized_points=organized_points)
    text = Renderer().render(request)
    response = call_llm(text, VideoEdit)
    return response


def render_template(edit: VideoEdit):
    # render a template for the video edit
    # {videoId: 'gGKsfXkSXv8', startSeconds: 826, endSeconds: 831}
    template_fp = Path(__file__).parent / "template.html"

    def format_segment(segment: BulletPointEx):
        start = int(segment.start)
        end = int(math.ceil(segment.start + segment.duration))
        return f"{{videoId: '{segment.video_id}', startSeconds: {start}, endSeconds: {end}}}"

    video_segments = [
        format_segment(segment)
        for segment in edit.points
        if segment.video_id is not None
    ]
    video_segments_s = ",\n".join(video_segments)

    segments = []
    for segment in edit.points:
        if segment.video_id is None:
            continue
        start = int(segment.start)
        end = int(segment.start + segment.duration)

        # segment should be a div containing video_id, start, end
        #
        segments.append(f'<div class="segment">{segment.video_id}, {start}:{end}</div>')
    segments_s = "\n".join(segments)

    template = template_fp.read_text()
    rendered = template.replace("VIDEO_SEGMENTS", video_segments_s).replace(
        "SEGMENTS", segments_s
    )
    output_fp = Path("output.html")
    output_fp.write_text(rendered)


def main(query_parts):
    query = phrase(query_parts)
    query_hash = hashstring(query)
    key = f"search_results.{query_hash}"
    print(query_parts)
    print(query)
    print(query_hash)
    print(key)
    search_results = cached_or_not(key, search, query)
    print(f'Found {len(search_results)} videos for "{query}"')

    # get and resegment the transcript for each video
    transcripts = get_transcripts(search_results)
    # show_transcripts_snippets(transcripts)

    # extract for each
    for transcript in transcripts:
        key = f"points.{transcript.video_id}"
        points = cached_or_not(key, extract_points, transcript)
        pprint(points)

    # fix up with video ids
    all_points_ex: BulletPointsEx = BulletPointsEx(points=[])
    for transcript in transcripts:
        key = f"points.{transcript.video_id}"
        points = cache[key]
        points_ex = exify(points, transcript.video_id)
        all_points_ex.points.extend(points_ex.points)
    pprint(all_points_ex)

    # organize
    organized_points = cached_or_not(
        f"organized_points.{query_hash}", organize_points, all_points_ex
    )
    pprint(organized_points)

    # produce the edit
    edit = cached_or_not(f"edit.{query_hash}", create_the_edit, organized_points)
    pprint(edit)

    # edit down

    # render the template
    render_template(edit)
