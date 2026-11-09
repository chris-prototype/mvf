# orchestrator
# orchestrator is implemented as langgraph
# it can run locally with no API key - pip install langgraph

from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# data
#
# class State inherits from TypeDict
class State(TypedDict):
    status: str

# nodes
#
# nodes are functions that take the current state and return an update to it
# state is a user defined name and State is a typehint
def load_spec(state: State):
    return {"status": "Spec Loaded"}

def build_app(state: State):
    return {"status": "Code Written"}

# assembly line
#
# START → load → build → END
workflow = StateGraph(State)

# add all nodes first
workflow.add_node("load", load_spec)
workflow.add_node("build", build_app)

# add all edges next connecting the nodes
workflow.add_edge(START, "load")
workflow.add_edge("load", "build")
workflow.add_edge("build", END)

# validate the graph and return an executable
app = workflow.compile()

# run the graph from START to END, set the intitial status to Start
print(app.invoke({"status": "Start"}))