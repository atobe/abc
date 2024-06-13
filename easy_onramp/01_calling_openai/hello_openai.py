import openai

client = openai.OpenAI()

prompt = "What is the capital of Ubekistan?"

result = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": prompt},
    ],
)

print(result)
print()
print()
print(result.choices[0].message.content)
