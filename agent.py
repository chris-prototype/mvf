# pip install google-genai
from google import genai
from google.genai import types
# looks for GEMINI_API_KEY
client = genai.Client(http_options=types.HttpOptions(timeout=10000))  # 10 seconds
response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents="Explain how AI works in a few words",
)
print(response.text)

# use to see which models are available
# 
# client = genai.Client()
# for m in client.models.list():
#     print(m.name)

# Attempted to use:

# slow
# gemini-3.8-flash

# not available
# gemini-2.5-flash-lite
