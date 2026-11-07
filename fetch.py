import os
import requests

query = """
query {
  issue(id: "TES-5") {
    title
    description
    state { name }
    project { name }
  }
}
"""

response = requests.post(
    "https://api.linear.app/graphql",
    headers={
        "Authorization": os.environ["LINEAR"],
        "Content-Type": "application/json"
    },
    json={"query": query}
)

print(response.json())