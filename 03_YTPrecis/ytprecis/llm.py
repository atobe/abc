from openai import OpenAI
import instructor
import os
from devtools import pprint

MODEL = os.environ.get("MODEL", "gpt-4-0125-preview")

def call_llm(prompt: str, response_model: type):
    client = instructor.from_openai(OpenAI())
    response = client.chat.completions.create_partial(
        model=MODEL,
        response_model=response_model,
        messages=[
            {"role": "user", "content": prompt},
        ],
        stream=True,
    )
    for update in response:
        print(".", end="", flush=True)
    # reconstruct the response model
    data = update.model_dump()
    pprint(data)
    obj = response_model(**data)
    return obj
