import os
import random
from raal.llm import streaming_llm
from lats.cache import cache

model = os.environ.get("MODEL", None)


def call_llm(messages, temperature=0.0, check_cache: bool = True) -> str:
    if not check_cache:
        return streaming_llm(model=model, messages=messages)
    slug = (str(messages), temperature)
    if slug not in cache:
        result = streaming_llm(model=model, messages=messages)
        cache[slug] = result
    return cache[slug]

def sample_llm(messages, temperature=0.7, n=5):
    slug = (str(messages), temperature)
    values = cache.data.get(slug, [])
    print(f"cache has {len(values)} values")
    if len(values) < n:
        result = call_llm(messages, temperature=temperature, check_cache=False)
        cache[slug] = values
        return result
    else:
        return random.choice(values)


