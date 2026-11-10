# record
# record is implemented as linear
# a linear ticket is created online and accessed via an API key here

import os
import requests
import json

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

issue = response.json()["data"]["issue"]

# print(f"Title:   {issue['title']}")
# print(f"State:   {issue['state']['name']}")
# print(f"Project: {issue['project']['name']}")
# print(f"\n{issue['description']}")


#
# save for later - print markdown in the console
#

from rich.console import Console
from rich.markdown import Markdown

Console().print(Markdown(issue["description"]))


#
# save for later
#

# response.json accepts json and creates a dictionary
# object_dict = response.json()

# takes dictionary and creates a formatted json string 
# string_JSON = json.dumps(object_dict, indent=2)

# print(string_JSON)