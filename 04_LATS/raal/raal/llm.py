import os
import random
from typing import List, Dict

import openai

from lats.cache import Cache

model = os.environ.get("MODEL", None)

cache = Cache("raal")

Message = Dict[str, str]


def streaming_llm(
    messages: List[Message],
    model=None,
    stop=None,
    callback=None,
    end_callback=None,
    without_dots=False,
    track=False,
    **kwargs,
) -> str:

    if model is None:
        raise Exception("model is required")

    if "temperature" not in kwargs:
        kwargs["temperature"] = 0

    if "top_p" not in kwargs:
        kwargs["top_p"] = 0

    base_url = os.environ.get("OPENAI_API_BASE")

    client_kwargs = dict(base_url=base_url) if base_url else {}
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"), **client_kwargs)

    if model:
        kwargs["model"] = model

    response = client.chat.completions.create(
        messages=messages, stop=stop, stream=True, **kwargs
    )

    tokens = []
    text = ""
    for chunk in response:
        try:
            if not without_dots:
                print(".", end="", flush=True)
            token = chunk.choices[0].delta.content
            if token:
                text += token
                if callback:
                    callback(token)
                continue
            elif chunk.choices[0].finish_reason == "stop":
                break
        except KeyboardInterrupt:
            raise
        except:
            print("-" * 80)
            import traceback

            traceback.print_exc()
            print("-" * 80)
            print(chunk)
            print("-" * 80)
    if not without_dots:
        print()

    if end_callback:
        end_callback(text)

    return text


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
