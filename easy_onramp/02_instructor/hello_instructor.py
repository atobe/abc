import instructor
from openai import OpenAI
from pydantic import BaseModel
from pprint import pprint
import os

model = os.environ.get("MODEL", "gpt-4")

# Patch the OpenAI client with Instructor
client = instructor.from_openai(
    OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
        base_url=os.environ.get("OPENAI_API_BASE"),
    )
)


class UserDetail(BaseModel):
    name: str
    age: int


# Function to extract user details
def extract_user(text) -> UserDetail:
    user = client.chat.completions.create(
        model=model,
        response_model=UserDetail,
        messages=[
            {"role": "user", "content": text},
        ],
    )
    return user


def main():
    text = "Extract Jason is 25 years old"
    user = extract_user(text)
    pprint(user)


if __name__ == "__main__":
    main()

# type
# python hello_instructor.py

# you should see this:
# UserDetail(name='Jason', age=25)
