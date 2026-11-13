# record
# record is implemented as linear
# a linear ticket is created online and accessed via an API key here

import os
import requests
import json
from rich.console import Console
from rich.markdown import Markdown

# select the properties we wish to request from the issue
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

# response.json accepts json and creates a dictionary
issue = response.json()["data"]["issue"]

print(f"Title:   {issue['title']}")
print(f"State:   {issue['state']['name']}")
print(f"Project: {issue['project']['name']}")
print(f"\n{issue['description']}")
Console().print(Markdown(issue["description"]))
