import httpx


def wikipedia(q):
    return httpx.get(
        "https://en.wikipedia.org/w/api.php",
        params={"action": "query", "list": "search", "srsearch": q, "format": "json"},
    ).json()["query"]["search"][0]["snippet"]


def simon_blog_search(q):
    results = httpx.get(
        "https://datasette.simonwillison.net/simonwillisonblog.json",
        params={
            "sql": """
        select
          blog_entry.title || ': ' || substr(html_strip_tags(blog_entry.body), 0, 1000) as text,
          blog_entry.created
        from
          blog_entry join blog_entry_fts on blog_entry.rowid = blog_entry_fts.rowid
        where
          blog_entry_fts match escape_fts(:q)
        order by
          blog_entry_fts.rank
        limit
          1""".strip(),
            "_shape": "array",
            "q": q,
        },
    ).json()
    return results[0]["text"]


def calculate(what):
    return eval(what)


def ask_for_help(what):
    print(f'Agent is asking for help: {what}')
    return input('> ')
    

known_actions = {
    "wikipedia": wikipedia,
    "calculate": calculate,
    "simon_blog_search": simon_blog_search,
    "ask_for_help": ask_for_help,
}
