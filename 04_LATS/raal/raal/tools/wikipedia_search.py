import httpx

from ..model import Tool, Observation


class WikipediaSearch(Tool):
    """Search Wikipedia for the query and return the first snippet."""

    def __call__(self, query: str):
        try:
            result = httpx.get(
                "https://en.wikipedia.org/w/api.php",
                params={
                    "action": "query",
                    "list": "search",
                    "srsearch": query,
                    "format": "json",
                },
            ).json()["query"]["search"][0]["snippet"]
            return Observation(result)
        except:
            return Observation("no results found")
