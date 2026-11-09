# orchestrator
# orchestrator is implemented as langgraph, it can run locally with no API key
# pip install langgraph

from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# data
class State(TypedDict):
    status: str

# nodes
def load_spec(state: State):
    return {"status": "Spec Loaded"}

def build_app(state: State):
    return {"status": "Code Written"}

# assembly line
workflow = StateGraph(State)
workflow.add_node("load", load_spec)
workflow.add_node("build", build_app)
workflow.add_edge(START, "load")
workflow.add_edge("load", "build")
workflow.add_edge("build", END)
app = workflow.compile()

# run
print(app.invoke({"status": "Start"}))