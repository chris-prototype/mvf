from typing import Any, cast

from langgraph.graph import END, StateGraph
from nodes import *
from state import FactoryState

# returns the next state after checking .error and .current_state of Factory State
def should_block(state: FactoryState) -> str:
    if state.get("error") or state.get("current_state") == "Blocked":
        return "blocked_handler"
    return "continue"

# FactoryState is passed into StateGraph to create the graph
def build_graph() -> StateGraph:
    graph = StateGraph(FactoryState)  # ty: ignore[invalid-argument-type] - ty bug
    
    # nodes
    graph.add_node("pm_agent", pm_agent)
    graph.add_node("gate_1", gate_1)
    graph.add_node("architect_agent", architect_agent)
    graph.add_node("gate_2", gate_2)
    graph.add_node("dev_agent", dev_agent)
    graph.add_node("review_agent", review_agent)
    graph.add_node("test_agent", test_agent)
    graph.add_node("gate_3", gate_3)
    graph.add_node("deploy_agent", deploy_agent)
    graph.add_node("done_handler", done_handler)
    graph.add_node("blocked_handler", blocked_handler)

    # edges
    graph.set_entry_point("pm_agent")
    graph.add_conditional_edges( "pm_agent", should_block, {"blocked_handler": "blocked_handler", "continue": "gate_1"} )
    graph.add_edge("gate_1", "architect_agent")
    graph.add_conditional_edges( "architect_agent", should_block, {"blocked_handler": "blocked_handler", "continue": "gate_2"} )
    graph.add_edge("gate_2", "dev_agent")
    graph.add_edge("dev_agent", "review_agent")
    graph.add_edge("review_agent", "test_agent")
    graph.add_edge("test_agent", "gate_3")
    graph.add_edge("gate_3", "deploy_agent")
    graph.add_conditional_edges( "deploy_agent", should_block, {"blocked_handler": "blocked_handler", "continue": "done_handler"} )
    graph.add_edge("done_handler", END)
    graph.add_edge("blocked_handler", END)
    
    # done
    return graph
