import os
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)

res = client.chat.completions.create(
    model="openrouter/auto",
    messages=[{"role": "user", "content": "Hi"}],
)
print("Model:", res.model)
print(res.choices[0].message.content)