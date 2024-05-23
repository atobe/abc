import openai
from typing import List, Dict, Any, Union
from termcolor import colored, cprint

MessageType = Dict[str, str] # role, content


def turn(messages: List[MessageType]) -> str:
    client = openai.OpenAI()
    response = client.chat.completions.create(
        # model="gpt-3.5-turbo",
        model="gpt-4",
        temperature=0,
        messages=messages,
        stream=True
    )
    color = 'white'
    result = ''
    for chunk in response:
        chunk_text = chunk.choices[0].delta.content
        if chunk_text:
            result += chunk_text
            if chunk_text == 'Thought':
                color = 'red'
            elif chunk_text == 'Action':
                print()
                color = 'green'
            cprint(chunk_text, end='', flush=True, color=color)
            if chunk_text == ':':
                color = 'white'
    print()
    return result

