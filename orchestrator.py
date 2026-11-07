# orchestrator is implemented as langgraph
# can run locally with no API key

from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# 1. The shared factory data
class State(TypedDict):
    status: str

# 2. The factory steps (Nodes)
def load_spec(state: State):
    return {"status": "Spec Loaded"}

def build_app(state: State):
    return {"status": "Code Written"}

# 3. The assembly line (Orchestrator)
workflow = StateGraph(State)
workflow.add_node("load", load_spec)
workflow.add_node("build", build_app)

workflow.add_edge(START, "load")
workflow.add_edge("load", "build")
workflow.add_edge("build", END)

app = workflow.compile()

# 4. Run it
print(app.invoke({"status": "Start"}))