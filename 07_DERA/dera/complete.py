import os
from typing import Dict, List
import openai
from pprint import pprint

model = os.environ.get("MODEL")


Message = Dict[str, str]

count = 0


def streaming_llm(
    messages: List[Message],
    model=None,
    stop=None,
    callback=None,
    end_callback=None,
    without_dots=False,
    track=False,
    verbose=False,
    **kwargs,
) -> str:

    if model is None:
        raise Exception("model is required")

    if "temperature" not in kwargs:
        kwargs["temperature"] = 0.0

    if "top_p" not in kwargs:
        kwargs["top_p"] = 0.0001

    base_url = os.environ.get("OPENAI_API_BASE")

    client_kwargs = dict(base_url=base_url) if base_url else {}
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"), **client_kwargs)

    if model:
        kwargs["model"] = model

    if verbose:
        print(base_url, model)
        pprint(kwargs)

    response = client.chat.completions.create(
        messages=messages, stop=stop, stream=True, **kwargs
    )

    tokens = []
    text = ""
    last_chunk = None
    for chunk in response:
        last_chunk = chunk
        try:
            if not without_dots:
                print(".", end="", flush=True)
            token = chunk.choices[0].delta.content
            if token:
                text += token
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

    if verbose:
        pprint(last_chunk)

    return text


def complete(system_prompt: str, user_prompt: str) -> str:
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    return streaming_llm(model=model, messages=messages)
