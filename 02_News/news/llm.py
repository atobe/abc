from openai import OpenAI
import instructor


def call_llm(prompt: str, response_model: type):
    client = instructor.from_openai(OpenAI())
    print("sending request")
    response = client.chat.completions.create_partial(
        model="gpt-4",
        response_model=response_model,
        messages=[
            {"role": "user", "content": prompt},
        ],
        stream=True,
    )
    for update in response:
        print(".", end="", flush=True)
    print()
    return update
